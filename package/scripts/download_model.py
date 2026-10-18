#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path
from huggingface_hub import snapshot_download

p = argparse.ArgumentParser()
p.add_argument("--out", required=True)
p.add_argument("--revision", required=True)
a = p.parse_args()
repo = "convaiinnovations/laya-multilingual"
path = Path(snapshot_download(repo, revision=a.revision, local_dir=a.out, allow_patterns=["rl_agent_config.json", "model.safetensors", "tokenizer/*", "encoder/*", "README.md", "config.json"]))
tokenizer = path / "tokenizer/tokenizer_config.json"
before = hashlib.sha256(tokenizer.read_bytes()).hexdigest()
prior_lock = path / "pd-model-lock.json"
prior_normalization = json.loads(prior_lock.read_text()).get("normalization", {}) if prior_lock.exists() else {}
# The pinned SDK performs this compatibility migration on first load. Run it
# before locking, so inference never changes a file behind the integrity check.
from laya.agent import _fix_tokenizer_config
_fix_tokenizer_config(str(path))
after = hashlib.sha256(tokenizer.read_bytes()).hexdigest()
normalization = {"file": "tokenizer/tokenizer_config.json", "operation": "laya 0.4.11 tokenizer compatibility normalization", "before_sha256": before, "after_sha256": after}
if before == after and prior_normalization.get("after_sha256") == after:
    normalization = prior_normalization
files = {}
for file in path.rglob("*"):
    if file.is_file() and ".cache" not in file.parts and file.name != "pd-model-lock.json":
        with file.open("rb") as stream:
            files[str(file.relative_to(path))] = hashlib.file_digest(stream, "sha256").hexdigest()
(path / "pd-model-lock.json").write_text(json.dumps({"repo": repo, "revision": a.revision, "files": files, "normalization": normalization}, indent=2) + "\n")
print(json.dumps({"model_path": str(path.resolve()), "revision": a.revision, "files": len(files)}))
