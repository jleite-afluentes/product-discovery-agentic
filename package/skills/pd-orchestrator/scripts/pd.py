#!/usr/bin/env python3
"""Project-scoped discovery ledger and workflow. Standard library, Python >=3.9."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.4.0"
KINDS = {"source", "evidence", "hypothesis", "persona", "decision", "question", "risk", "experiment", "finding", "artifact", "review", "gate_request", "approval", "task", "handoff", "entity", "relation", "context_review", "context_feedback"}
ENTITY_TYPES = {"domain", "process", "rule", "requirement", "decision", "risk", "persona", "system", "data", "gate", "artifact", "concept"}
RELATION_TYPES = {"supports", "contradicts", "depends_on", "affects", "owned_by", "used_in", "produces", "blocks", "replaces", "revokes", "related_to"}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def sha(value):
    return hashlib.sha256(value if isinstance(value, bytes) else value.encode()).hexdigest()


def stamp():
    return datetime.now(timezone.utc).isoformat()


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def registry():
    return load(ROOT / "references/agents.json")


def policy():
    return load(ROOT / "references/gates.json")


class Error(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise Error(message)


class Project:
    def __init__(self, path):
        self.path = Path(path).resolve()
        self.home = self.path / ".pd"
        require((self.home / "project.json").is_file(), "Projeto não inicializado; use init.")
        self.meta = load(self.home / "project.json")
        self.db = sqlite3.connect(str(self.home / "ledger.sqlite"), isolation_level=None, timeout=30)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA foreign_keys=ON")

    @classmethod
    def init(cls, path, name, owner):
        path = Path(path).resolve()
        require(not (path / ".pd").exists(), "Projeto já existe; use status para retomar.")
        require(name.strip() and owner.strip(), "Nome e owner são obrigatórios.")
        (path / ".pd").mkdir(parents=True)
        meta = {"id": str(uuid.uuid4()), "name": name, "owner": owner, "package_version": VERSION, "created_at": stamp()}
        (path / ".pd/project.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n")
        db = sqlite3.connect(str(path / ".pd/ledger.sqlite"))
        db.executescript("""
        CREATE TABLE records (id TEXT NOT NULL, version INTEGER NOT NULL, kind TEXT NOT NULL,
          actor TEXT NOT NULL, body TEXT NOT NULL, hash TEXT NOT NULL, created TEXT NOT NULL,
          PRIMARY KEY(id,version));
        CREATE TABLE events (seq INTEGER PRIMARY KEY, body TEXT NOT NULL, previous TEXT NOT NULL, hash TEXT NOT NULL);
        """)
        db.close()
        project = cls(path)
        with project.transaction():
            project.event("project.initialized", owner, {"project": meta, "policy_hash": sha(canonical(policy())), "registry_hash": sha(canonical(registry()))})
        return project

    def transaction(self):
        from contextlib import contextmanager

        @contextmanager
        def tx():
            self.db.execute("BEGIN IMMEDIATE")
            try:
                yield
                self.db.execute("COMMIT")
            except BaseException:
                self.db.execute("ROLLBACK")
                raise
        return tx()

    def event(self, action, actor, data):
        last = self.db.execute("SELECT seq,hash FROM events ORDER BY seq DESC LIMIT 1").fetchone()
        previous = last["hash"] if last else "0" * 64
        seq = last["seq"] + 1 if last else 1
        body = canonical({"seq": seq, "project_id": self.meta["id"], "time": stamp(), "action": action, "actor": actor, "data": data})
        digest = sha(previous + body)
        self.db.execute("INSERT INTO events VALUES(?,?,?,?)", (seq, body, previous, digest))
        return digest

    def records(self, kind=None):
        rows = self.db.execute("SELECT r.* FROM records r JOIN (SELECT id,MAX(version) v FROM records GROUP BY id) x ON r.id=x.id AND r.version=x.v ORDER BY r.created,r.id")
        return [self.decode(r) for r in rows if kind is None or r["kind"] == kind]

    def get(self, ident, version=None):
        row = self.db.execute("SELECT * FROM records WHERE id=? " + ("AND version=?" if version is not None else "ORDER BY version DESC LIMIT 1"), (ident, version) if version is not None else (ident,)).fetchone()
        require(row is not None, "Referência ausente neste projeto: " + ident)
        return self.decode(row)

    @staticmethod
    def decode(row):
        data = dict(row)
        data["body"] = json.loads(data["body"])
        return data

    def save(self, kind, actor, body, ident=None):
        require(kind in KINDS, "Tipo de registro inválido.")
        require(bool(actor.strip()), "Actor obrigatório.")
        ident = ident or kind.upper() + "-" + uuid.uuid4().hex[:12]
        require(re.fullmatch(r"[A-Za-z0-9_-]{1,90}", ident), "ID inválido.")
        old = self.db.execute("SELECT MAX(version) FROM records WHERE id=?", (ident,)).fetchone()[0]
        if old:
            require(self.get(ident)["kind"] == kind, "Não é permitido mudar o tipo de um ID.")
            require(kind not in {"review", "gate_request", "approval", "source"}, "Este registro é imutável; crie outro ID.")
        refs = []
        for ref in body.get("refs", []):
            item = self.get(ref)
            refs.append({"id": item["id"], "version": item["version"], "hash": item["hash"]})
        value = {**body, "project_id": self.meta["id"], "pinned_refs": refs}
        version = (old or 0) + 1
        created = stamp()
        text = canonical(value)
        digest = sha(canonical({"id": ident, "version": version, "kind": kind, "actor": actor, "body": value, "created": created}))
        self.db.execute("INSERT INTO records VALUES(?,?,?,?,?,?,?)", (ident, version, kind, actor, text, digest, created))
        self.event("record.saved", actor, {"id": ident, "version": version, "kind": kind, "hash": digest})
        return self.get(ident)

    def record(self, kind, actor, body, ident=None):
        require(kind not in {"artifact", "review", "gate_request", "approval", "task", "handoff", "context_review", "context_feedback"}, "Use o comando específico para este tipo.")
        require(isinstance(body, dict) and body.get("title"), "Registro exige title.")
        if kind == "source":
            require(body.get("locator") and body.get("content") and body.get("source_type") in {"document", "web", "user_report", "fieldwork", "simulation"}, "Fonte exige locator, content e source_type válidos.")
            body = {**body, "content_sha256": sha(body["content"]), "captured_at": stamp()}
        if kind == "evidence":
            require(body.get("refs") and body.get("observation") and body.get("limitations"), "Evidência exige refs, observation e limitations.")
            sources = [self.get(r) for r in body["refs"]]
            require(any(s["kind"] == "source" for s in sources), "Evidência exige uma fonte original.")
            require(all(s["body"].get("source_type") != "simulation" for s in sources), "Simulação não pode ser promovida a evidência; use hypothesis.")
        if kind == "persona":
            require(body.get("persona_type") in {"stakeholder_proxy", "synthetic_customer"}, "persona_type obrigatório.")
            require(body.get("refs") and isinstance(body.get("unknowns"), list), "Persona exige refs e unknowns.")
        if kind == "decision":
            require(body.get("scope") == "low_complexity" and body.get("reversible") is True and body.get("external_commitment") is False, "Decisões delegadas devem ser reversíveis, internas e de baixa complexidade.")
            require(body.get("decision_type") in {"organize_evidence", "choose_template", "select_preapproved_method"}, "Tipo de decisão fora da alçada delegada.")
            require(body.get("rationale") and body.get("refs"), "Decisão exige justificativa e referências.")
        if kind == "question":
            require(body.get("status") in {"open", "resolved"} and body.get("blocking") in {True, False}, "Questão exige status e blocking.")
            if body["status"] == "resolved":
                require(body.get("refs"), "Resolução exige fonte de resposta.")
        if kind == "entity":
            require(body.get("entity_type") in ENTITY_TYPES, "Entidade exige entity_type conhecido.")
            require(body.get("refs") and isinstance(body.get("aliases", []), list), "Entidade exige refs e aliases em lista.")
            require(all(isinstance(x, str) and x.strip() for x in body.get("aliases", [])), "Aliases devem ser textos não vazios.")
            require(any(self.get(r)["kind"] in {"source", "evidence"} for r in body["refs"]), "Entidade exige fonte ou evidência de origem.")
            require(body.get("knowledge_status", "proposed") == "proposed", "Conhecimento só pode ser aceito por context-accept.")
            body["knowledge_status"] = "proposed"
        if kind == "relation":
            require(body.get("predicate") in RELATION_TYPES, "Relação exige predicate conhecido.")
            require(body.get("certainty") in {"confirmed", "possible"}, "Relação deve distinguir confirmed de possible.")
            require(body.get("subject") and body.get("object") and body["subject"] != body["object"], "Relação exige subject e object distintos.")
            require(body.get("refs") and body.get("rationale"), "Relação exige refs e rationale.")
            require(self.get(body["subject"])["kind"] == "entity" and self.get(body["object"])["kind"] == "entity", "Extremos da relação devem ser entidades do projeto.")
            require(any(self.get(r)["kind"] in {"source", "evidence"} for r in body["refs"]), "Relação exige fonte original ou evidência rastreável.")
            if body["predicate"] in {"replaces", "revokes"}:
                require(body.get("target_relation") and self.get(body["target_relation"])["kind"] == "relation", "replaces/revokes exige target_relation existente.")
                require(body["certainty"] == "confirmed", "Substituição ou revogação exige decisão confirmada e rastreável.")
                body["refs"] = list(dict.fromkeys(body.get("refs", []) + [body["target_relation"]]))
            require(body.get("knowledge_status", "proposed") == "proposed", "Conhecimento só pode ser aceito por context-accept.")
            body["knowledge_status"] = "proposed"
        with self.transaction():
            return self.save(kind, actor, body, ident)

    def stale(self, record, visited=None):
        visited = set() if visited is None else visited
        key = (record["id"], record["version"])
        if key in visited:
            return False
        visited.add(key)
        for ref in record["body"].get("pinned_refs", []):
            current = self.get(ref["id"])
            if current["hash"] != ref["hash"] or self.stale(current, visited):
                return True
        return False

    def artifact(self, actor, ident, file, refs, tags, claims):
        require(actor in registry()["agents"], "Autor deve ser um agente do registro.")
        require(refs, "Artefato precisa declarar referências; use uma fonte de demanda inicial.")
        path = Path(file).resolve()
        require(path.is_file(), "Arquivo de entrada não encontrado.")
        raw = path.read_bytes()
        require(len(raw) <= 20 * 1024 * 1024, "Arquivo excede 20 MiB.")
        for claim in claims:
            require(claim.get("statement") and claim.get("status") in {"supported", "hypothesis"} and claim.get("refs"), "Afirmação exige statement, status e refs.")
            require(set(claim["refs"]) <= set(refs), "Referência da afirmação deve constar nas refs do artefato.")
            if claim["status"] == "supported":
                require(any(self.get(r)["kind"] == "evidence" for r in claim["refs"]), "Afirmação suportada exige registro de evidência.")
        blob = sha(raw)
        suffix = path.suffix.lower()
        require(re.fullmatch(r"\.[a-z0-9]{1,10}", suffix), "Extensão de arquivo inválida.")
        storage = self.home / "blobs" / (blob + suffix)
        storage.parent.mkdir(exist_ok=True)
        storage.write_bytes(raw)
        with self.transaction():
            return self.save("artifact", actor, {"title": path.name, "refs": refs, "tags": tags, "claims": claims, "blob": str(storage.relative_to(self.home)), "sha256": blob, "bytes": len(raw)}, ident)

    def review(self, actor, target, verdict, findings):
        require(actor == "reviewer", "Parecer de gate exige o papel reviewer.")
        with self.transaction():
            record = self.get(target)
            require(record["kind"] == "artifact", "Revisão deve apontar para artefato.")
            require(record["actor"] != actor, "Autoaprovação proibida.")
            require(verdict in {"pass", "rework", "blocked"}, "Parecer inválido.")
            require(isinstance(findings, list), "Findings deve ser lista.")
            if verdict == "pass":
                require(not findings, "Parecer pass não pode esconder findings; resolva-os primeiro.")
                require(not self.stale(record), "Artefato depende de uma versão superada.")
            return self.save("review", actor, {"title": "Revisão de " + target, "refs": [target], "verdict": verdict, "findings": findings})

    def artifact_passed(self, record):
        matches = [r for r in self.records("review") if r["body"]["pinned_refs"][0]["hash"] == record["hash"]]
        return bool(matches) and matches[-1]["body"]["verdict"] == "pass"

    def gate_valid(self, request):
        body = request["body"]
        if self.stale(request) or body["policy_hash"] != sha(canonical(policy())) or body["registry_hash"] != sha(canonical(registry())):
            return False
        gate = body["gate"]
        if any(q["body"]["blocking"] and q["body"]["status"] == "open" and gate in q["body"].get("gates", [gate]) for q in self.records("question")):
            return False
        return all(self.artifact_passed(self.get(ref)) for ref in body["artifacts"])

    def active_gates(self):
        active = []
        for gate in policy()["gates"]:
            approvals = [a for a in self.records("approval") if a["body"]["gate"] == gate["id"]]
            valid = [a for a in approvals if not self.stale(a) and self.gate_valid(self.get(a["body"]["refs"][0]))]
            if not valid:
                break
            active.append(gate["id"])
        return active

    def gate_request(self, gate, artifacts):
        with self.transaction():
            gates = policy()["gates"]
            spec = next((g for g in gates if g["id"] == gate), None)
            require(spec is not None, "Gate desconhecido.")
            index = [g["id"] for g in gates].index(gate)
            active = self.active_gates()
            require(index == len(active), "Gate fora de sequência; consulte status.")
            require(artifacts and len(set(artifacts)) == len(artifacts), "Informe artefatos sem duplicatas.")
            records = [self.get(a) for a in artifacts]
            require(all(r["kind"] == "artifact" and self.artifact_passed(r) and not self.stale(r) for r in records), "Todos os artefatos precisam de revisão independente atual e referências válidas.")
            tags = {t for r in records for t in r["body"]["tags"]}
            require(set(spec["required_tags"]) <= tags, "Tags obrigatórias ausentes: " + str(set(spec["required_tags"]) - tags))
            blockers = [q["id"] for q in self.records("question") if q["body"]["blocking"] and q["body"]["status"] == "open" and gate in q["body"].get("gates", [gate])]
            require(not blockers, "Perguntas bloqueadoras: " + str(blockers))
            if gate == "G6":
                require(self.records("handoff"), "Prepare o handoff após G5 antes de solicitar G6.")
            refs = artifacts + [r["id"] for r in self.records("question") if gate in r["body"].get("gates", [gate]) and r["body"]["blocking"]]
            if index:
                previous = [a for a in self.records("approval") if a["body"]["gate"] == gates[index-1]["id"] and not self.stale(a)][-1]
                refs.append(previous["id"])
            if gate == "G6":
                refs += [h["id"] for h in self.records("handoff")]
            return self.save("gate_request", "orchestrator", {"title": spec["title"], "gate": gate, "artifacts": artifacts, "refs": refs, "criteria": spec["criteria"], "policy_hash": sha(canonical(policy())), "registry_hash": sha(canonical(registry()))})

    def approve_interactive(self, request, actor):
        require(actor == "human:" + self.meta["owner"], "Somente o owner humano registrado pode aprovar gates.")
        require(sys.stdin.isatty(), "Aprovação requer terminal interativo do responsável humano; agentes devem apresentar a solicitação.")
        candidate = self.get(request)
        require(candidate["kind"] == "gate_request", "ID não é solicitação de gate.")
        challenge = "APROVAR " + request + " " + candidate["hash"][:12]
        print(canonical({"project": self.meta["name"], "request": candidate}), file=sys.stderr)
        response = input("Confirme pessoalmente digitando: " + challenge + "\n")
        require(response == challenge, "Aprovação não confirmada.")
        with self.transaction():
            candidate = self.get(request)
            require(self.gate_valid(candidate), "Contexto, revisão ou bloqueios mudaram; prepare uma nova solicitação.")
            require(candidate["body"]["policy_hash"] == sha(canonical(policy())) and candidate["body"]["registry_hash"] == sha(canonical(registry())), "Política ou registro mudou; solicite nova revisão.")
            gate = candidate["body"]["gate"]
            require(gate == "G" + str(len(self.active_gates())), "Gate já aprovado ou fora de sequência.")
            return self.save("approval", actor, {"title": "Aprovação humana " + gate, "gate": gate, "refs": [request], "policy_hash": candidate["body"]["policy_hash"], "confirmation": response, "channel": "interactive_terminal_attestation"})

    def handoff(self, actor, recipient, refs, pending):
        require(actor == "rfp" and "G5" in self.active_gates(), "Handoff final exige G5 aprovado e papel rfp.")
        require(recipient.strip() and refs, "Handoff exige destinatário e referências.")
        with self.transaction():
            return self.save("handoff", actor, {"title": "Handoff para " + recipient, "recipient": recipient, "refs": refs, "pending": pending, "acceptance": "pending_human_G6"})

    def human_decision(self, actor, body):
        require(actor == "human:" + self.meta["owner"], "Decisão humana exige o owner registrado.")
        require(sys.stdin.isatty(), "Decisão humana exige confirmação pessoal em terminal interativo.")
        require(body.get("title") and body.get("rationale") and body.get("refs") and body.get("decision_type"), "Decisão exige title, rationale, refs e decision_type.")
        initial = [self.get(r)["hash"] for r in body["refs"]]
        fingerprint = sha(canonical(body) + canonical(initial))[:12]
        challenge = "DECIDIR " + fingerprint
        print(json.dumps(body, ensure_ascii=False, indent=2), file=sys.stderr)
        require(input("Confirme pessoalmente digitando: " + challenge + "\n") == challenge, "Decisão não confirmada.")
        with self.transaction():
            require(initial == [self.get(r)["hash"] for r in body["refs"]], "Referências mudaram durante a confirmação.")
            return self.save("decision", actor, {**body, "authority": "human", "confirmation": challenge, "channel": "interactive_terminal_attestation"})

    def dispatch(self, task, agent, refs, reason):
        require(agent in registry()["agents"] and agent != "orchestrator", "Agente de destino desconhecido.")
        require(refs and reason, "Dispatch exige refs e justificativa; fallback é uma decisão do System 2.")
        with self.transaction():
            if task:
                item = self.get(task)
                require(item["kind"] == "task" and (item["body"]["state"] in {"awaiting_system2", "awaiting_dispatch"} or (item["body"]["state"] == "ready" and self.stale(item))), "Tarefa não aguarda dispatch nem está desatualizada.")
                return self.save("task", "orchestrator", {**item["body"], "state": "ready", "agent": agent, "dispatch_reason": reason, "refs": list(dict.fromkeys(item["body"].get("refs", []) + refs))}, task)
            return self.save("task", "orchestrator", {"title": reason, "state": "ready", "agent": agent, "refs": refs, "dispatch_reason": reason})

    def finish_task(self, task, actor, outputs):
        with self.transaction():
            item = self.get(task)
            require(item["kind"] == "task" and item["body"]["state"] == "ready" and item["body"]["agent"] == actor, "Tarefa não está disponível para este agente.")
            require(not self.stale(item), "Entradas da tarefa mudaram; solicite novo dispatch com contexto atual.")
            require(outputs and all(self.get(r)["kind"] == "artifact" and self.get(r)["actor"] == actor and not self.stale(self.get(r)) for r in outputs), "Conclusão exige artefatos atuais do agente responsável.")
            inputs = set(item["body"]["refs"])
            def ancestry(record, visited=None):
                visited = set() if visited is None else visited
                if record["id"] in visited:
                    return visited
                visited.add(record["id"])
                for ref in record["body"].get("refs", []):
                    ancestry(self.get(ref), visited)
                return visited
            require(all(inputs.intersection(ancestry(self.get(r))) for r in outputs), "Saída não se vincula às entradas da tarefa.")
            return self.save("task", actor, {**item["body"], "state": "completed", "outputs": outputs, "refs": list(dict.fromkeys(item["body"]["refs"] + outputs))}, task)

    def route(self, text, python, model_path=None, timeout=120, action=None, expected_artifact=None, gate=None, max_context_chars=None):
        config = load(ROOT / "references/routing.json")
        budget = min(int(max_context_chars or config.get("max_context_chars", 6000)), int(config.get("max_context_chars", 6000)))
        envelope = {"request": text, "action": action, "expected_artifact": expected_artifact, "current_gate": gate}
        context_chars = len(canonical(envelope))
        if context_chars > budget:
            with self.transaction():
                return self.save("task", "orchestrator", {"title": text, "state": "awaiting_system2", "agent": None, "candidate": None, "reason": "context_budget_exceeded", "context_chars": context_chars, "context_budget_chars": budget, "routing_config_hash": sha(canonical(config)), "refs": []})
        started = time.monotonic()
        payload = {"text": text, "action": action, "expected_artifact": expected_artifact, "current_gate": gate, "routes": config["routes"], "model_path": model_path}
        try:
            result = subprocess.run([str(python), str(ROOT / "scripts/laya_worker.py")], input=canonical(payload), text=True, capture_output=True, timeout=timeout)
            require(result.returncode == 0, "laya_worker_failed: " + result.stderr[-600:])
            answer = json.loads(result.stdout)
            chosen, score = answer["choice"], answer["confidence"]
            require(chosen in config["routes"] and isinstance(score, (int, float)) and not isinstance(score, bool) and math.isfinite(score) and 0 <= score <= 1, "Resposta Laya inválida.")
            probabilities = answer.get("probabilities")
            if probabilities is not None:
                require(isinstance(probabilities, dict) and all(k in config["routes"] and isinstance(v, (int, float)) and math.isfinite(v) and 0 <= v <= 1 for k, v in probabilities.items()), "Probabilidades Laya inválidas.")
            ranked = sorted((probabilities or {}).items(), key=lambda pair: pair[1], reverse=True)
            margin = round(ranked[0][1] - ranked[1][1], 6) if len(ranked) > 1 else None
            context_complete = bool(action and expected_artifact and gate)
            reason = "candidate_requires_system2_confirmation"
            if chosen == "abstain" or score < config["min_confidence"]:
                reason = "abstention_or_low_confidence"
            elif not context_complete:
                reason = "structured_context_incomplete"
            state = "awaiting_system2"
            agent = None
            if context_complete and chosen != "abstain" and score >= config["min_confidence"] and config["automatic_dispatch"] and config.get("calibration_report"):
                state, agent, reason = "ready", config["routes"][chosen]["agent"], "evaluated_route"
            usage = answer.get("usage")
            laya_tokens = {key: usage[key] for key in ("input_tokens", "output_tokens", "state_tokens", "state_tokens_dropped") if isinstance(usage, dict) and key in usage}
            token_usage = answer.get("token_usage") or ({"source": "laya_usage", **laya_tokens} if laya_tokens else {"status": "not_reported_by_harness"})
            data = {"title": text, "state": state, "agent": agent, "candidate": chosen, "score": score, "probabilities": probabilities, "top_candidates": ranked[:3], "top_margin": margin, "reason": reason, "model": answer.get("model"), "model_revision": answer.get("revision"), "runtime": answer.get("runtime"), "usage": usage, "token_usage": token_usage, "context": {"action": action, "expected_artifact": expected_artifact, "current_gate": gate, "complete": context_complete, "characters": context_chars, "budget_chars": budget}, "attempts": 1, "attempt_budget": int(config.get("attempt_budget", 1)), "routing_config_hash": sha(canonical(config)), "refs": []}
        except (Error, OSError, subprocess.TimeoutExpired, ValueError, KeyError, TypeError) as exc:
            data = {"title": text, "state": "awaiting_system2", "agent": None, "candidate": None, "reason": "laya_unavailable_or_invalid", "error": str(exc), "routing_config_hash": sha(canonical(config)), "refs": []}
        data["latency_ms"] = round((time.monotonic() - started) * 1000)
        with self.transaction():
            return self.save("task", "orchestrator", data)

    def audit(self):
        previous = "0" * 64
        count = 0
        recorded = set()
        for event in self.db.execute("SELECT * FROM events ORDER BY seq"):
            count += 1
            body = json.loads(event["body"])
            require(event["seq"] == count and body["seq"] == count and body["project_id"] == self.meta["id"], "Sequência ou projeto de auditoria inválido.")
            require(event["previous"] == previous and sha(previous + event["body"]) == event["hash"], "Cadeia de auditoria alterada.")
            previous = event["hash"]
            if body["action"] == "project.initialized":
                require(body["data"]["project"] == self.meta, "Metadados de projeto alterados fora do ledger.")
            if body["action"] == "record.saved":
                d = body["data"]
                require(self.db.execute("SELECT 1 FROM records WHERE id=? AND version=? AND hash=?", (d["id"], d["version"], d["hash"])).fetchone() is not None, "Evento aponta para versão removida.")
                recorded.add((d["id"], d["version"], d["hash"]))
        for row in self.db.execute("SELECT * FROM records"):
            r = self.decode(row)
            expected = sha(canonical({"id": r["id"], "version": r["version"], "kind": r["kind"], "actor": r["actor"], "body": r["body"], "created": r["created"]}))
            require(expected == r["hash"] and (r["id"], r["version"], r["hash"]) in recorded, "Registro sem integridade: " + r["id"])
            require(r["body"]["project_id"] == self.meta["id"], "Registro pertence a outro projeto.")
            if r["kind"] == "artifact":
                path = (self.home / r["body"]["blob"]).resolve()
                require(path.is_relative_to(self.home) if hasattr(path, "is_relative_to") else str(path).startswith(str(self.home) + os.sep), "Blob fora do projeto.")
                require(path.is_file() and sha(path.read_bytes()) == r["body"]["sha256"], "Conteúdo do artefato alterado: " + r["id"])
        return {"ok": True, "events": count, "head": previous, "project_id": self.meta["id"], "limits": "Hash chain detects local changes against its current head; it is not a signature or external identity verification."}

    def status(self):
        self.audit()
        records = self.records()
        return {"project": self.meta, "approved_gates": self.active_gates(), "tasks": [r for r in records if r["kind"] == "task" and r["body"]["state"] != "completed"], "open_questions": [r for r in records if r["kind"] == "question" and r["body"]["status"] == "open"], "stale_artifacts": [r["id"] for r in records if r["kind"] == "artifact" and self.stale(r)], "records": len(records)}

    @staticmethod
    def _terms(text):
        import unicodedata
        value = unicodedata.normalize("NFKD", str(text).lower())
        value = "".join(c for c in value if not unicodedata.combining(c))
        return set(re.findall(r"[a-z0-9_]{2,}", value))

    def _active_relations(self):
        relations = [r for r in self.records("relation") if r["body"].get("knowledge_status") == "accepted" and not self.stale(r)]
        superseded = {r["body"].get("target_relation") for r in relations if r["body"].get("predicate") in {"replaces", "revokes"}}
        return [r for r in relations if r["id"] not in superseded and r["body"].get("predicate") not in {"replaces", "revokes"}]

    def graph_search(self, query, limit=10):
        require(query.strip() and 1 <= limit <= 100, "Informe busca e limite entre 1 e 100.")
        terms = self._terms(query)
        ranked = []
        relation_map = self._active_relations()
        for record in self.records():
            if record["kind"] in {"approval", "gate_request", "review", "task", "handoff", "context_review", "context_feedback"}:
                continue
            if record["kind"] in {"entity", "relation"} and record["body"].get("knowledge_status") != "accepted": continue
            if self.stale(record): continue
            body = record["body"]
            fields = [body.get("title", ""), body.get("content", ""), body.get("observation", ""), body.get("statement", ""), body.get("rationale", ""), body.get("entity_type", ""), body.get("predicate", "")]
            if record["kind"] == "entity": fields.extend(body.get("aliases", []))
            if record["kind"] == "relation": fields.extend([body.get("subject", ""), body.get("object", ""), body.get("certainty", "")])
            searchable = self._terms(" ".join(map(str, fields)))
            overlap = terms & searchable
            if not overlap: continue
            score = len(overlap) / max(1, len(terms))
            score += 0.25 if record["kind"] == "entity" else 0
            if record["kind"] == "relation" and record not in relation_map: score *= 0.5
            ranked.append((score, record["created"], record))
        ranked.sort(key=lambda x: (-x[0], x[1], x[2]["id"]))
        return [{"score": round(score, 4), "record": self._compact_record(record)} for score, _, record in ranked[:limit]]

    @staticmethod
    def _compact_record(record):
        body = record["body"]
        keep = {k: body[k] for k in ("title", "entity_type", "aliases", "predicate", "subject", "object", "certainty", "content", "observation", "statement", "rationale", "locator", "source_type", "refs", "pinned_refs", "status", "blocking", "limitations", "unknowns") if k in body}
        if isinstance(keep.get("content"), str) and len(keep["content"]) > 3000:
            keep["content"] = keep["content"][:3000] + "…[conteúdo reduzido; consulte show para o registro original]"
        return {"id": record["id"], "version": record["version"], "kind": record["kind"], "hash": record["hash"], "actor": record["actor"], "created": record["created"], "stale": False, "body": keep}

    def graph_neighbors(self, ident, depth=1, include_possible=True):
        require(self.get(ident)["kind"] == "entity" and self.get(ident)["body"].get("knowledge_status") == "accepted", "neighbors requer ID de entidade aceita.")
        require(1 <= depth <= 4, "depth deve estar entre 1 e 4.")
        relations = self._active_relations()
        adjacency = {}
        for relation in relations:
            b = relation["body"]
            adjacency.setdefault(b["subject"], []).append((relation, b["object"]))
            adjacency.setdefault(b["object"], []).append((relation, b["subject"]))
        seen, frontier, edges = {ident}, {ident}, []
        for level in range(1, depth + 1):
            next_frontier = set()
            for current in frontier:
              for rel, other in adjacency.get(current, []):
                b = rel["body"]
                if not include_possible and b["certainty"] != "confirmed": continue
                edges.append({"depth": level, "relation": self._compact_record(rel), "neighbor": self._compact_record(self.get(other))})
                if other not in seen: next_frontier.add(other)
            seen |= next_frontier; frontier = next_frontier
            if not frontier: break
        return {"root": self._compact_record(self.get(ident)), "depth": depth, "edges": edges}

    def graph_impact(self, ident, include_possible=True):
        """Return sourced outgoing impacts and explicit possible impacts, with paths."""
        require(self.get(ident)["kind"] == "entity" and self.get(ident)["body"].get("knowledge_status") == "accepted", "impact requer ID de entidade aceita.")
        relations = self._active_relations()
        outgoing = {}
        for relation in relations: outgoing.setdefault(relation["body"]["subject"], []).append(relation)
        result = {"root": self._compact_record(self.get(ident)), "confirmed": [], "possible": []}
        queue = [(ident, [])]; best_depth = {ident: 0}; seen_edges = set()
        while queue:
            current, path = queue.pop(0)
            for rel in outgoing.get(current, []):
                b = rel["body"]
                if not include_possible and b["certainty"] != "confirmed": continue
                edge_key = (rel["id"], tuple(x["relation"]["id"] for x in path))
                if edge_key in seen_edges: continue
                seen_edges.add(edge_key)
                node = self.get(b["object"])
                item = {"path": [x["relation"]["id"] for x in path] + [rel["id"]], "depth": len(path) + 1, "relation": self._compact_record(rel), "target": self._compact_record(node)}
                path_is_possible = b["certainty"] == "possible" or any(x["relation"]["body"]["certainty"] == "possible" for x in path)
                result["possible" if path_is_possible else "confirmed"].append(item)
                if len(path) < 6 and best_depth.get(node["id"], 99) > len(path) + 1:
                    best_depth[node["id"]] = len(path) + 1; queue.append((node["id"], path + [item]))
        return result

    def context_packet(self, query, refs=None, max_chars=12000, limit=12):
        started = time.perf_counter()
        require(500 <= max_chars <= 100000, "max_chars deve estar entre 500 e 100000.")
        selected = []
        seen = set()
        for ident in refs or []:
            record = self.get(ident)
            require(not self.stale(record), "Referência desatualizada não pode entrar no contexto: " + ident)
            require(record["kind"] not in {"entity", "relation"} or record["body"].get("knowledge_status") == "accepted", "Proposta de conhecimento precisa de context-accept antes de uso.")
            if record["id"] not in seen: selected.append({"score": 1.0, "record": self._compact_record(record)}); seen.add(record["id"])
        matches = self.graph_search(query, limit)
        for item in matches:
            if item["record"]["id"] not in seen: selected.append(item); seen.add(item["record"]["id"])
        matched_entities = {x["record"]["id"] for x in matches if x["record"]["kind"] == "entity"}
        for item in matches:
            if item["record"]["kind"] == "relation":
                for ref in item["record"]["body"].get("refs", []):
                    origin = self.get(ref)
                    if origin["kind"] in {"source", "evidence"} and origin["id"] not in seen:
                        selected.append({"score": 0.4, "record": self._compact_record(origin)}); seen.add(origin["id"])
        for rel in self._active_relations():
            b = rel["body"]
            if b["subject"] in matched_entities or b["object"] in matched_entities:
                if rel["id"] not in seen: selected.append({"score": 0.5, "record": self._compact_record(rel)}); seen.add(rel["id"])
                for ref in b.get("refs", []):
                    origin = self.get(ref)
                    if origin["kind"] in {"source", "evidence", "hypothesis", "decision", "question"} and origin["id"] not in seen:
                        selected.append({"score": 0.4, "record": self._compact_record(origin)}); seen.add(origin["id"])
        used, records = 0, []
        for item in selected:
            content = item.get("record", {}).get("body", {}).get("content")
            if isinstance(content, str) and len(content) > 3000:
                item["record"]["body"]["content"] = content[:3000] + "…[conteúdo reduzido; consulte o registro original]"
            encoded = canonical(item)
            if used + len(encoded) > max_chars: continue
            records.append(item); used += len(encoded)
        latency_ms = round((time.perf_counter() - started) * 1000, 3)
        telemetry = {"query_sha256": sha(query), "record_versions": [{"id": x["record"]["id"], "version": x["record"]["version"], "hash": x["record"]["hash"]} for x in records], "record_count": len(records), "context_chars": used, "max_chars": max_chars, "truncated": len(records) < len(selected), "retrieval_latency_ms": latency_ms, "token_count": None}
        with self.transaction():
            event_hash = self.event("context.retrieved", "orchestrator", telemetry)
            event_seq = self.db.execute("SELECT seq FROM events WHERE hash=?", (event_hash,)).fetchone()[0]
        return {"project_id": self.meta["id"], "query": query, "records": records, "record_count": len(records), "context_chars": used, "max_chars": max_chars, "truncated": len(records) < len(selected), "retrieval_latency_ms": latency_ms, "token_count": None, "token_count_note": "Token count is not inferred from characters; obtain it from the executing harness.", "graph_revision": max((r["created"] for r in self.records()), default=None), "audit_event_seq": event_seq, "audit_event_hash": event_hash}

    def context_feedback(self, actor, event_seq, relevant_refs, retrieved_relevant, omitted_relevant, irrelevant, harness_tokens=None, reviewed_response_ms=None, rating=None):
        event = self.db.execute("SELECT * FROM events WHERE seq=?", (event_seq,)).fetchone()
        require(event is not None, "Evento de recuperação inexistente.")
        event_body = json.loads(event["body"])
        require(event_body["action"] == "context.retrieved", "Evento não é uma recuperação de contexto.")
        require(not any(r["body"].get("context_event_seq") == event_seq for r in self.records("context_feedback")), "Esta recuperação já recebeu feedback; use um novo evento para uma nova avaliação.")
        retrieved = {x["id"] for x in event_body["data"]["record_versions"]}
        for snapshot in event_body["data"]["record_versions"]:
            require(self.get(snapshot["id"])["hash"] == snapshot["hash"], "O contexto mudou desde a recuperação; gere pacote novo antes de avaliar.")
        relevant, selected, omitted, irrelevant_set = set(relevant_refs), set(retrieved_relevant), set(omitted_relevant), set(irrelevant)
        require(relevant == selected | omitted and not selected & omitted, "relevant_refs deve ser retrieved_relevant + omitted_relevant, sem sobreposição.")
        require(selected <= retrieved and irrelevant_set <= retrieved and not selected & irrelevant_set, "Refs relevantes selecionadas e irrelevantes devem pertencer ao contexto e não se sobrepor.")
        require(selected | irrelevant_set == retrieved, "Rotule todos os registros recuperados como relevantes ou irrelevantes para medir precisão.")
        require(not omitted & retrieved, "Uma referência omitida não pode estar no pacote recuperado.")
        for ident in relevant | irrelevant_set: self.get(ident)
        require(harness_tokens is None or (isinstance(harness_tokens, int) and harness_tokens >= 0), "harness_tokens deve ser inteiro não negativo ou null.")
        require(reviewed_response_ms is None or (isinstance(reviewed_response_ms, int) and reviewed_response_ms >= 0), "reviewed_response_ms deve ser inteiro não negativo ou null.")
        require(rating is None or (isinstance(rating, int) and 1 <= rating <= 5), "rating deve estar entre 1 e 5.")
        precision = len(selected) / len(retrieved) if retrieved else None
        recall = len(selected) / len(relevant) if relevant else None
        body = {"title": f"Feedback de contexto seq {event_seq}", "context_event_seq": event_seq, "relevant_refs": sorted(relevant), "retrieved_relevant": sorted(selected), "omitted_relevant": sorted(omitted), "irrelevant_refs": sorted(irrelevant_set), "precision": round(precision, 4) if precision is not None else None, "recall": round(recall, 4) if recall is not None else None, "harness_tokens": harness_tokens, "reviewed_response_ms": reviewed_response_ms, "rating": rating, "refs": sorted(relevant | irrelevant_set)}
        with self.transaction(): return self.save("context_feedback", actor, body)

    def context_accept(self, actor, ids, rationale):
        require(actor == "reviewer" or actor == "human:" + self.meta["owner"], "Aceitação do contexto exige reviewer independente ou owner humano.")
        require(ids and rationale.strip() and len(ids) == len(set(ids)), "Informe IDs únicos e racional da revisão.")
        proposals = [self.get(ident) for ident in ids]
        require(all(r["kind"] in {"entity", "relation"} and r["body"].get("knowledge_status") == "proposed" and not self.stale(r) for r in proposals), "Somente propostas atuais de entidade/relação podem ser aceitas.")
        if actor == "reviewer": require(all(r["actor"] != actor for r in proposals), "Revisor não pode aceitar proposta própria.")
        versions = [{"id": r["id"], "version": r["version"], "hash": r["hash"]} for r in proposals]
        entity_ids = {r["id"] for r in proposals if r["kind"] == "entity"}
        with self.transaction():
            review = self.save("context_review", actor, {"title": "Revisão e aceite de conhecimento", "verdict": "accepted", "rationale": rationale, "proposed_versions": versions})
            accepted = []
            for old in [r for r in proposals if r["kind"] == "entity"]:
                body = dict(old["body"]); body["knowledge_status"] = "accepted"; body["accepted_by"] = actor; body["refs"] = list(dict.fromkeys(body.get("refs", []) + [review["id"]]))
                accepted.append(self.save("entity", actor, body, old["id"]))
            for old in [r for r in proposals if r["kind"] == "relation"]:
                body = dict(old["body"])
                for endpoint in (body["subject"], body["object"]):
                    endpoint_record = self.get(endpoint)
                    require(endpoint_record["body"].get("knowledge_status") == "accepted" or endpoint in entity_ids, "Aceite da relação também exige aceitar as entidades propostas nas pontas.")
                body["knowledge_status"] = "accepted"; body["accepted_by"] = actor; body["refs"] = list(dict.fromkeys(body.get("refs", []) + [review["id"]]))
                accepted.append(self.save("relation", actor, body, old["id"]))
        return {"review": self.get(review["id"]), "accepted": [self.get(r["id"]) for r in accepted], "source_of_truth": "ledger"}

    def context_metrics(self):
        events = [json.loads(r["body"]) for r in self.db.execute("SELECT body FROM events ORDER BY seq") if json.loads(r["body"])["action"] == "context.retrieved"]
        feedback = self.records("context_feedback")
        def mean(values): return round(sum(values) / len(values), 3) if values else None
        by_seq = {r["body"]["context_event_seq"]: r["body"] for r in feedback}
        latencies = [e["data"]["retrieval_latency_ms"] for e in events]
        chars = [e["data"]["context_chars"] for e in events]
        tokens = [by_seq[e["seq"]]["harness_tokens"] for e in events if e["seq"] in by_seq and by_seq[e["seq"]].get("harness_tokens") is not None]
        review_times = [r["body"]["reviewed_response_ms"] for r in feedback if r["body"].get("reviewed_response_ms") is not None]
        precisions = [r["body"]["precision"] for r in feedback if r["body"].get("precision") is not None]
        recalls = [r["body"]["recall"] for r in feedback if r["body"].get("recall") is not None]
        return {"retrievals": len(events), "labeled_retrievals": len(feedback), "feedback_coverage": round(len(feedback) / len(events), 4) if events else None, "mean_precision": mean(precisions), "mean_recall": mean(recalls), "mean_retrieval_latency_ms": mean(latencies), "mean_context_chars": mean(chars), "mean_harness_tokens": mean(tokens), "mean_reviewed_response_ms": mean(review_times), "token_measurements": len(tokens), "quality_metrics_require_complete_human_labels": True, "targets_configured": False}

    def export_graph(self, directory):
        """Export a project-local Markdown graph suitable for Obsidian or any editor."""
        target = Path(directory).resolve()
        target.mkdir(parents=True, exist_ok=True)
        entities = [r for r in self.records("entity") if r["body"].get("knowledge_status") == "accepted" and not self.stale(r)]
        active = self._active_relations()
        exported = []
        source_ids = set()
        adjacency = {}
        for rel in active:
            b = rel["body"]
            adjacency.setdefault(b["subject"], []).append(rel)
            adjacency.setdefault(b["object"], []).append(rel)
            for ref in b.get("refs", []):
                if self.get(ref)["kind"] in {"source", "evidence"}: source_ids.add(ref)
        for entity in entities:
            for ref in entity["body"].get("refs", []):
                if self.get(ref)["kind"] in {"source", "evidence"}: source_ids.add(ref)
        source_queue = list(source_ids)
        while source_queue:
            item = self.get(source_queue.pop())
            if item["kind"] == "evidence":
                for ref in item["body"].get("refs", []):
                    if self.get(ref)["kind"] == "source" and ref not in source_ids:
                        source_ids.add(ref); source_queue.append(ref)
        for entity in entities:
            ident, body = entity["id"], entity["body"]
            relation_links = [f"- [[{rel['id']}|{rel['body']['certainty']} {rel['body']['predicate']}]]" for rel in adjacency.get(ident, [])]
            source_links = [f"- [[{ref}|{self.get(ref)['body']['title']}]]" for ref in body.get("refs", []) if self.get(ref)["kind"] in {"source", "evidence"}]
            text = [f"# {body['title']}", "", f"- ID: `{ident}`", f"- Tipo: `{body['entity_type']}`", f"- Versão/hash: `{entity['version']}` / `{entity['hash']}`", f"- Aliases: {', '.join(body.get('aliases', [])) or '—'}", "", "## Relações", *(relation_links or ["- Nenhuma relação ativa registrada."]), "", "## Origem", *(source_links or ["- Nenhuma origem direta registrada."]), ""]
            (target / f"{ident}.md").write_text("\n".join(text), encoding="utf-8")
            exported.append(ident)
        for rel in active:
            b = rel["body"]
            subject, obj = self.get(b["subject"]), self.get(b["object"])
            lines = [f"# {b['title']}", "", f"- ID: `{rel['id']}`", f"- Relation type: `{b['predicate']}`", f"- Certainty: `{b['certainty']}`", f"- Rationale: {b['rationale']}", f"- Hash: `{rel['hash']}`", "", "## Path", f"- [[{subject['id']}|{subject['body']['title']}]] → [[{obj['id']}|{obj['body']['title']}]]", "", "## Sources"]
            origins = [ref for ref in b.get("refs", []) if self.get(ref)["kind"] in {"source", "evidence"}]
            lines.extend([f"- [[{ref}|{self.get(ref)['body']['title']}]]" for ref in origins] or ["- None recorded."])
            (target / f"{rel['id']}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        for ident in sorted(source_ids):
            source = self.get(ident)
            body = source["body"]
            lines = [f"# {body['title']}", "", f"- ID: `{ident}`", f"- Type: `{source['kind']}`", f"- Version/hash: `{source['version']}` / `{source['hash']}`", f"- Locator: {body.get('locator', '—')}", f"- Source type: {body.get('source_type', '—')}", f"- Content SHA-256: `{body.get('content_sha256', '')}`", ""]
            if source["kind"] == "evidence": lines.extend(["## Observation", body.get("observation", ""), "", "## Limitations", body.get("limitations", ""), ""])
            original_sources = [ref for ref in body.get("refs", []) if self.get(ref)["kind"] == "source"]
            lines.extend(["## Original sources", *[f"- [[{ref}|{self.get(ref)['body']['title']}]]" for ref in original_sources], ""])
            linked_entities = [e for e in entities if ident in e["body"].get("refs", [])]
            linked_relations = [r for r in active if ident in r["body"].get("refs", [])]
            lines.extend(["## Used by", *[f"- [[{e['id']}|{e['body']['title']}]]" for e in linked_entities], *[f"- [[{r['id']}|{r['body']['title']}]]" for r in linked_relations], ""])
            (target / f"{ident}.md").write_text("\n".join(lines), encoding="utf-8")
        index = [f"# Grafo de domínio — {self.meta['name']}", "", "Export derivado do ledger. Edite as fontes no CLI; alterações neste Markdown não atualizam o projeto.", "", "## Entidades", *[f"- [[{r['id']}|{r['body']['title']}]] — `{r['body']['entity_type']}`" for r in entities if r['id'] in exported], "", "## Fontes e evidências", *[f"- [[{i}|{self.get(i)['body']['title']}]]" for i in sorted(source_ids)], ""]
        (target / "index.md").write_text("\n".join(index), encoding="utf-8")
        return {"directory": str(target), "entities_exported": len(exported), "relations_exported": len(active), "sources_exported": len(source_ids), "source_of_truth": "project_ledger", "editable_import": False}

    def ingest_proposals(self, actor, proposal):
        """Validate and append agent-proposed entities/relations as ledger records."""
        require(actor.strip() and isinstance(proposal, dict), "Ingestão exige actor e objeto JSON.")
        entities = proposal.get("entities", [])
        relations = proposal.get("relations", [])
        require(isinstance(entities, list) and isinstance(relations, list) and (entities or relations), "Informe entities e/ou relations como listas.")
        proposed_ids = [x.get("id") for x in entities + relations if isinstance(x, dict)]
        require(len(proposed_ids) == len(entities) + len(relations) and all(isinstance(i, str) and re.fullmatch(r"[A-Za-z0-9_-]{1,90}", i) for i in proposed_ids), "Cada proposta exige ID válido.")
        require(len(set(proposed_ids)) == len(proposed_ids), "IDs duplicados no lote.")
        for ident in proposed_ids:
            require(self.db.execute("SELECT 1 FROM records WHERE id=?", (ident,)).fetchone() is None, "Ingestão é append-only; ID já existe: " + ident)
        proposed_entities = {x["id"] for x in entities}
        known_entities = {r["id"] for r in self.records("entity")} | proposed_entities
        with self.transaction():
            for item in entities:
                body = {k: v for k, v in item.items() if k != "id"}
                require(body.get("title") and body.get("entity_type") in ENTITY_TYPES and isinstance(body.get("aliases", []), list), "Entidade exige title, entity_type e aliases válidos.")
                body["knowledge_status"] = "proposed"
                require(body.get("refs") and any(self.get(ref)["kind"] in {"source", "evidence"} for ref in body["refs"]), "Cada entidade exige fonte ou evidência já registrada.")
                self.save("entity", actor, body, item["id"])
            for item in relations:
                body = {k: v for k, v in item.items() if k != "id"}
                require(body.get("title") and body.get("predicate") in RELATION_TYPES and body.get("certainty") in {"confirmed", "possible"} and body.get("rationale"), "Relação exige title, predicate, certainty e rationale válidos.")
                body["knowledge_status"] = "proposed"
                require(body.get("subject") in known_entities and body.get("object") in known_entities and body["subject"] != body["object"], "Extremos da relação precisam existir ou estar no lote.")
                if body.get("predicate") in {"replaces", "revokes"}:
                    require(body.get("target_relation") in {r["id"] for r in self.records("relation")}, "target_relation precisa existir antes desta ingestão.")
                    body["refs"] = list(body.get("refs", [])) + [body["target_relation"]]
                body["refs"] = list(dict.fromkeys(body.get("refs", []) + [body["subject"], body["object"]]))
                require(body.get("refs") and any(self.get(ref)["kind"] in {"source", "evidence"} for ref in body["refs"]), "Relação exige fonte original ou evidência rastreável.")
                require(self.get(body["subject"])["kind"] == "entity" and self.get(body["object"])["kind"] == "entity", "Extremos precisam ser entidades registradas.")
                if body["predicate"] in {"replaces", "revokes"}:
                    require(body["certainty"] == "confirmed", "Substituição ou revogação exige certainty confirmed.")
                self.save("relation", actor, body, item["id"])
        return {"accepted": True, "append_only": True, "entities": [self.get(i) for i in [x["id"] for x in entities]], "relations": [self.get(i) for i in [x["id"] for x in relations]], "review_required_before_use": True}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", default=".")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init"); p.add_argument("--name", required=True); p.add_argument("--owner", required=True)
    sub.add_parser("status"); sub.add_parser("audit")
    p = sub.add_parser("record"); p.add_argument("kind"); p.add_argument("--actor", required=True); p.add_argument("--file", required=True); p.add_argument("--id")
    p = sub.add_parser("list"); p.add_argument("--kind")
    p = sub.add_parser("show"); p.add_argument("id")
    p = sub.add_parser("artifact"); p.add_argument("--actor", required=True); p.add_argument("--id", required=True); p.add_argument("--file", required=True); p.add_argument("--refs", nargs="+", required=True); p.add_argument("--tags", nargs="+", required=True); p.add_argument("--claims")
    p = sub.add_parser("review"); p.add_argument("--actor", default="reviewer"); p.add_argument("--target", required=True); p.add_argument("--verdict", choices=["pass", "rework", "blocked"], required=True); p.add_argument("--findings")
    p = sub.add_parser("gate"); p.add_argument("gate"); p.add_argument("--artifacts", nargs="+", required=True)
    p = sub.add_parser("approve"); p.add_argument("--request", required=True); p.add_argument("--actor", required=True)
    p = sub.add_parser("handoff"); p.add_argument("--recipient", required=True); p.add_argument("--refs", nargs="+", required=True); p.add_argument("--pending", default="")
    p = sub.add_parser("human-decision"); p.add_argument("--actor", required=True); p.add_argument("--file", required=True)
    p = sub.add_parser("route"); p.add_argument("--text", required=True); p.add_argument("--python", required=True); p.add_argument("--model-path"); p.add_argument("--timeout", type=int, default=120); p.add_argument("--action"); p.add_argument("--expected-artifact"); p.add_argument("--gate"); p.add_argument("--max-context-chars", type=int)
    p = sub.add_parser("dispatch"); p.add_argument("--task"); p.add_argument("--agent", required=True); p.add_argument("--refs", nargs="+", required=True); p.add_argument("--reason", required=True)
    p = sub.add_parser("complete"); p.add_argument("--task", required=True); p.add_argument("--actor", required=True); p.add_argument("--outputs", nargs="+", required=True)
    p = sub.add_parser("export-audit"); p.add_argument("--out", required=True)
    p = sub.add_parser("search"); p.add_argument("query"); p.add_argument("--limit", type=int, default=10)
    p = sub.add_parser("neighbors"); p.add_argument("id"); p.add_argument("--depth", type=int, default=1); p.add_argument("--confirmed-only", action="store_true")
    p = sub.add_parser("impact"); p.add_argument("id"); p.add_argument("--confirmed-only", action="store_true")
    p = sub.add_parser("context"); p.add_argument("query"); p.add_argument("--refs", nargs="*", default=[]); p.add_argument("--max-chars", type=int, default=12000); p.add_argument("--limit", type=int, default=12)
    p = sub.add_parser("ingest"); p.add_argument("--actor", required=True); p.add_argument("--file", required=True)
    p = sub.add_parser("export-graph"); p.add_argument("--dir", required=True)
    p = sub.add_parser("context-feedback"); p.add_argument("--actor", required=True); p.add_argument("--event-seq", type=int, required=True); p.add_argument("--relevant-refs", nargs="*", default=[]); p.add_argument("--retrieved-relevant", nargs="*", default=[]); p.add_argument("--omitted-relevant", nargs="*", default=[]); p.add_argument("--irrelevant", nargs="*", default=[]); p.add_argument("--harness-tokens", type=int); p.add_argument("--reviewed-response-ms", type=int); p.add_argument("--rating", type=int)
    p = sub.add_parser("context-accept"); p.add_argument("--actor", required=True); p.add_argument("--ids", nargs="+", required=True); p.add_argument("--rationale", required=True)
    sub.add_parser("context-metrics")
    args = parser.parse_args(argv)
    try:
        if args.cmd == "init":
            result = Project.init(args.project, args.name, args.owner).status()
        else:
            project = Project(args.project)
            project.audit()
            if args.cmd == "status": result = project.status()
            elif args.cmd == "audit": result = project.audit()
            elif args.cmd == "record": result = project.record(args.kind, args.actor, load(args.file), args.id)
            elif args.cmd == "list": result = project.records(args.kind)
            elif args.cmd == "show": result = project.get(args.id)
            elif args.cmd == "artifact": result = project.artifact(args.actor, args.id, args.file, args.refs, args.tags, load(args.claims) if args.claims else [])
            elif args.cmd == "review": result = project.review(args.actor, args.target, args.verdict, load(args.findings) if args.findings else [])
            elif args.cmd == "gate": result = project.gate_request(args.gate, args.artifacts)
            elif args.cmd == "approve": result = project.approve_interactive(args.request, args.actor)
            elif args.cmd == "handoff": result = project.handoff("rfp", args.recipient, args.refs, args.pending)
            elif args.cmd == "human-decision": result = project.human_decision(args.actor, load(args.file))
            elif args.cmd == "route": result = project.route(args.text, args.python, args.model_path, args.timeout, args.action, args.expected_artifact, args.gate, args.max_context_chars)
            elif args.cmd == "dispatch": result = project.dispatch(args.task, args.agent, args.refs, args.reason)
            elif args.cmd == "complete": result = project.finish_task(args.task, args.actor, args.outputs)
            elif args.cmd == "export-audit":
                result = project.audit()
                out = Path(args.out)
                out.write_text("\n".join(canonical(dict(e)) for e in project.db.execute("SELECT * FROM events ORDER BY seq")) + "\n", encoding="utf-8")
                result["export"] = str(out.resolve())
            elif args.cmd == "search": result = {"results": project.graph_search(args.query, args.limit)}
            elif args.cmd == "neighbors": result = project.graph_neighbors(args.id, args.depth, not args.confirmed_only)
            elif args.cmd == "impact": result = project.graph_impact(args.id, not args.confirmed_only)
            elif args.cmd == "context": result = project.context_packet(args.query, args.refs, args.max_chars, args.limit)
            elif args.cmd == "ingest": result = project.ingest_proposals(args.actor, load(args.file))
            elif args.cmd == "export-graph": result = project.export_graph(args.dir)
            elif args.cmd == "context-feedback": result = project.context_feedback(args.actor, args.event_seq, args.relevant_refs, args.retrieved_relevant, args.omitted_relevant, args.irrelevant, args.harness_tokens, args.reviewed_response_ms, args.rating)
            elif args.cmd == "context-accept": result = project.context_accept(args.actor, args.ids, args.rationale)
            elif args.cmd == "context-metrics": result = project.context_metrics()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (Error, sqlite3.Error, OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
