#!/usr/bin/env python3
"""Run with Python >=3.12. Creates an isolated, project-independent Laya runtime."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import venv

REVISION = "1720e3e3357cfe1e281542e223f8273b0890ca34"
ROOT = Path(__file__).resolve().parents[1]

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--runtime-dir", required=True)
    p.add_argument("--download-model", action="store_true")
    a = p.parse_args()
    if sys.version_info < (3, 12): raise SystemExit("Python >=3.12 required by the tested dependency lock.")
    root = Path(a.runtime_dir).expanduser().resolve()
    env = root / "laya"
    if not env.exists(): venv.create(env, with_pip=True)
    python = env / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    subprocess.run([str(python), "-m", "pip", "install", "-r", str(ROOT / "requirements-laya.lock")], check=True)
    config = {"python": str(python), "model_path": str(root / "models/laya-multilingual"), "repo": "convaiinnovations/laya-multilingual", "revision": REVISION}
    if a.download_model:
        subprocess.run([str(python), str(ROOT / "scripts/download_model.py"), "--out", config["model_path"], "--revision", REVISION], check=True)
    root.mkdir(parents=True, exist_ok=True)
    (root / "install-local.json").write_text(json.dumps(config, indent=2) + "\n")
    print(json.dumps(config, indent=2))

if __name__ == "__main__": main()
