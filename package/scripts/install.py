#!/usr/bin/env python3
"""Install only the reusable package. Never copy projects or modify global config."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import os
import sys

ROOT = Path(__file__).resolve().parents[1]


def files(root):
    return sorted(p for p in root.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc" and p.name != ".DS_Store")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify():
    manifest = json.loads((ROOT / "manifest.json").read_text())
    for rel, expected in manifest["files"].items():
        path = (ROOT / rel).resolve()
        if ROOT not in path.parents or not path.is_file() or digest(path) != expected:
            raise ValueError("Package integrity failed: " + rel)
    actual = {str(p.relative_to(ROOT)) for p in files(ROOT) if p.name != "manifest.json"}
    if actual != set(manifest["files"]):
        raise ValueError("Unexpected or missing package files.")
    agents = json.loads((ROOT / "skills/pd-orchestrator/references/agents.json").read_text())["agents"]
    for key, agent in agents.items():
        if not (ROOT / "skills" / agent["skill"] / "SKILL.md").is_file():
            raise ValueError("Registry references missing skill: " + agent["skill"])
        if key != "orchestrator" and not (ROOT / "agents" / ("pd-" + key + ".toml")).is_file():
            raise ValueError("Registry references missing native agent: " + key)
        for specialist in agent["subagents"]:
            if key != "orchestrator" and not (ROOT / "agents" / ("pd-" + specialist + ".toml")).is_file():
                raise ValueError("Registry references missing specialist: " + specialist)
    return manifest


def install(dest, agents_dest, upgrade=False, runtime_config=None):
    manifest = verify()
    dest, agents_dest = Path(dest).expanduser().resolve(), Path(agents_dest).expanduser().resolve()
    local_runtime = None
    if runtime_config:
        local_runtime = json.loads(Path(runtime_config).read_text())
        if not Path(local_runtime["python"]).is_file() or not (Path(local_runtime["model_path"]) / "pd-model-lock.json").is_file():
            raise ValueError("Runtime Python or model lock not found.")
    if dest == agents_dest or dest in agents_dest.parents or agents_dest in dest.parents:
        raise ValueError("Skills and native agents need separate directories.")
    # Preflight every target before the first mutation. Existing foreign files are never overwritten.
    targets = []
    for skill in sorted((ROOT / "skills").iterdir()):
        target = dest / skill.name
        if target.exists():
            marker = target / ".pd-install.json"
            if not upgrade or not marker.is_file():
                raise ValueError("Existing skill; use --upgrade only for managed installs: " + str(target))
            old = json.loads(marker.read_text())
            expected = set(old["files"])
            actual = {str(p.relative_to(target)) for p in files(target) if p.name != ".pd-install.json"}
            if actual != expected or any(digest(target / p) != h for p, h in old["files"].items()):
                raise ValueError("Local skill edits detected; preserve/reconcile before upgrade: " + str(target))
        targets.append((skill, target, "skill"))
    for agent in sorted((ROOT / "agents").glob("*.toml")):
        target = agents_dest / agent.name
        marker = target.with_suffix(".pd-install.json")
        if target.exists() and (not upgrade or not marker.is_file() or json.loads(marker.read_text()).get("hash") != digest(target)):
            raise ValueError("Existing or edited native agent: " + str(target))
        targets.append((agent, target, "agent"))
    dest.mkdir(parents=True, exist_ok=True)
    agents_dest.mkdir(parents=True, exist_ok=True)
    # Each skill is replaced atomically; interruption may leave a partial installation.
    # Rerun with --upgrade to reconcile verified managed targets; project databases are never touched.
    for source, target, kind in targets:
        if kind == "skill":
            staging = Path(tempfile.mkdtemp(prefix=".pd-stage-", dir=dest))
            shutil.copytree(source, staging, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))
            if source.name == "pd-orchestrator" and local_runtime:
                (staging / "local-runtime.json").write_text(json.dumps(local_runtime, indent=2) + "\n")
            hashes = {str(p.relative_to(staging)): digest(p) for p in files(staging)}
            (staging / ".pd-install.json").write_text(json.dumps({"package_version": manifest["version"], "files": hashes}, indent=2) + "\n")
            backup = target.with_name(".pd-backup-" + target.name)
            if backup.exists():
                raise ValueError("Interrupted backup exists; reconcile it before retry: " + str(backup))
            if target.exists(): target.rename(backup)
            try: staging.rename(target)
            except BaseException:
                if backup.exists(): backup.rename(target)
                raise
            if backup.exists(): shutil.rmtree(backup)
        else:
            import tomllib
            content = source.read_text()
            obj = tomllib.loads(content)
            obj["developer_instructions"] = "Skills directory: " + str(dest) + ". " + obj["developer_instructions"]
            text = "\n".join(k + " = " + json.dumps(v, ensure_ascii=False) for k, v in obj.items()) + "\n"
            temp = target.with_suffix(".tmp")
            temp.write_text(text); os.replace(temp, target)
            target.with_suffix(".pd-install.json").write_text(json.dumps({"hash": digest(target), "package_version": manifest["version"]}) + "\n")
    return {"version": manifest["version"], "skills": len(list((ROOT / "skills").iterdir())), "native_agents": len(list((ROOT / "agents").glob("*.toml"))), "skills_dir": str(dest), "agents_dir": str(agents_dest), "next_turn": "Open a new turn to discover installed skills/agents. Invoke $pd-orchestrator with an explicit project path."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dest", default=str(Path.home() / ".agents/skills"))
    parser.add_argument("--agents-dest", default=str(Path.home() / ".codex/agents"))
    parser.add_argument("--upgrade", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--runtime-config", help="Optional install-local.json generated by setup_laya.py")
    args = parser.parse_args()
    try:
        if sys.version_info < (3, 11): raise ValueError("Installer requires Python 3.11+ (tomllib); core CLI supports Python 3.9+.")
        print(json.dumps(verify() if args.verify_only else install(args.dest, args.agents_dest, args.upgrade, args.runtime_config), ensure_ascii=False, indent=2))
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr); sys.exit(2)
