#!/usr/bin/env python3
"""Build a source-only installable package, excluding all project contexts and models."""
import hashlib
import json
from pathlib import Path
import zipfile
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "package"
VERSION = "0.2.1"
subprocess.run([sys.executable, str(PACKAGE / "scripts/sync_agents.py")], check=True)
paths = sorted(p for p in PACKAGE.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc" and p.name not in {".DS_Store", "manifest.json"})
manifest = {"name": "product-discovery-agentic", "version": VERSION, "files": {str(p.relative_to(PACKAGE)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
(PACKAGE / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
out = ROOT / f"dist/product-discovery-agentic-{VERSION}.zip"
out.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as archive:
    for p in paths + [PACKAGE / "manifest.json"]:
        archive.write(p, "product-discovery-agentic/" + str(p.relative_to(PACKAGE)))
print(json.dumps({"archive": str(out), "files": len(paths)+1, "sha256": hashlib.sha256(out.read_bytes()).hexdigest(), "skills": len(list((PACKAGE/'skills').iterdir())), "native_agents": len(list((PACKAGE/'agents').glob('*.toml')))}, ensure_ascii=False))
