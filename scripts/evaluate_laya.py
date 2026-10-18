#!/usr/bin/env python3
"""Synthetic integration cases, not a production calibration or market study."""
import argparse
import importlib.metadata
import json
from pathlib import Path
import time
import os

p = argparse.ArgumentParser(description=__doc__)
p.add_argument("--model-path", required=True)
p.add_argument("--out", required=True)
a = p.parse_args()
root = Path(__file__).resolve().parents[1]
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import laya
import torch
torch.set_num_threads(4)
agent = laya.load(a.model_path, device="cpu")
config = json.loads((root / "package/skills/pd-orchestrator/references/routing.json").read_text())
question = {"route": {"type": "choice", "instructions": "Select the specialist responsible for the MAIN discovery task. If unclear or asking approval, abstain.", "criteria": {k: v["description"] for k, v in config["routes"].items()}}}
results=[]
for case in json.loads((root / "tests/routing_cases.json").read_text()):
    start=time.monotonic()
    response=agent.system_one(case["text"], question, max_len=4096, head_max_len=1024)
    answer=response["answers"]["route"]
    usage=response.get("usage",{})
    results.append({**case,"actual":answer["choice"],"score":answer["answer_confidence"],"correct":answer["choice"]==case["expected"],"usage":usage,"latency_ms":round((time.monotonic()-start)*1000),"would_escalate": answer["answer_confidence"] < config["min_confidence"] or answer["choice"]=="abstain" or not config["automatic_dispatch"]})
lock=json.loads((Path(a.model_path)/"pd-model-lock.json").read_text())
report={"evaluation_type":"synthetic_integration_smoke_not_calibration","model":lock["repo"],"revision":lock["revision"],"laya_version":importlib.metadata.version("laya"),"device":"cpu","cases":len(results),"correct":sum(r["correct"] for r in results),"escalated":sum(r["would_escalate"] for r in results),"results":results,"automatic_dispatch_enabled":False,"limits":"Pequeno conjunto sintético escrito para integração; não estima acurácia em projetos reais nem justifica habilitar despacho automático."}
Path(a.out).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='results'},ensure_ascii=False))
