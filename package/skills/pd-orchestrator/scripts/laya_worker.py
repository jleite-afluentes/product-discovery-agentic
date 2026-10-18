#!/usr/bin/env python3
"""One real local Laya inference; stdout is reserved for a small JSON result."""
import contextlib
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import sys


def main():
    request = json.load(sys.stdin)
    path = request.get("model_path") or os.environ.get("PD_LAYA_MODEL")
    if not path or not Path(path).is_dir():
        raise ValueError("Configure um checkpoint local fixado; use setup_laya.py.")
    model_path = Path(path).resolve()
    lock = json.loads((model_path / "pd-model-lock.json").read_text())
    for file, expected in lock["files"].items():
        full = (model_path / file).resolve()
        if model_path not in full.parents:
            raise ValueError("Arquivo de checkpoint fora do diretório do modelo.")
        with full.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest() if hasattr(hashlib, "file_digest") else hashlib.sha256(stream.read()).hexdigest()
        if digest != expected:
            raise ValueError("Checkpoint alterado: " + file)
    # Disable network access for inference: setup is a separate, explicit operation.
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    with contextlib.redirect_stdout(sys.stderr):
        import laya
        import torch
        torch.set_num_threads(min(4, os.cpu_count() or 1))
        agent = laya.load(str(model_path), device=os.environ.get("PD_LAYA_DEVICE", "cpu"))
        criteria = {k: v.get("short_description", v["description"]) for k, v in request["routes"].items()}
        instruction = "Escolha a rota principal para a ação pedida. Considere o artefato esperado e o gate atual. Se houver múltiplas tarefas sem prioridade, pedido de aprovação humana ou assunto fora do discovery, escolha abstain."
        questions = {"route": {"type": "choice", "instructions": instruction, "criteria": criteria}}
        envelope = {"solicitacao": request["text"], "acao": request.get("action"), "artefato_esperado": request.get("expected_artifact"), "gate_atual": request.get("current_gate")}
        result = agent.system_one(json.dumps(envelope, ensure_ascii=False, separators=(",", ":")), questions, max_len=4096, head_max_len=1024)
    usage = result.get("usage", {})
    if usage.get("truncated") or usage.get("state_tokens_dropped", 0) or usage.get("options"):
        raise ValueError("Laya truncou contexto ou opções; encaminhe para System 2.")
    answer = result["answers"]["route"]
    print(json.dumps({"choice": answer["choice"], "confidence": answer["answer_confidence"], "probabilities": answer.get("probabilities"), "model": lock["repo"], "revision": lock["revision"], "runtime": {"laya": importlib.metadata.version("laya"), "torch": importlib.metadata.version("torch")}, "usage": usage}))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)
