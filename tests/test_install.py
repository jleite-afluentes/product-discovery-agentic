import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('installer',ROOT/'package/scripts/install.py')
mod=importlib.util.module_from_spec(s);s.loader.exec_module(mod)

class Install(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
 def tearDown(self):self.tmp.cleanup()
 def test_clean_install_and_native_profiles(self):
  import tomllib
  r=mod.install(self.root/'skills',self.root/'agents')
  self.assertEqual(13,r['skills'])
  for p in (self.root/'agents').glob('*.toml'):
   agent=tomllib.loads(p.read_text())
   self.assertTrue(agent['developer_instructions'].startswith('Skills directory:'))
  self.assertFalse((self.root/'skills/pd-orchestrator/.pd').exists())
 def test_preflight_preserves_foreign_skill(self):
  target=self.root/'skills/pd-research';target.mkdir(parents=True);(target/'SKILL.md').write_text('foreign')
  with self.assertRaises(ValueError):mod.install(self.root/'skills',self.root/'agents')
  self.assertEqual('foreign',(target/'SKILL.md').read_text())
  self.assertFalse((self.root/'skills/pd-orchestrator').exists())
 def test_upgrade_preserves_local_edits(self):
  mod.install(self.root/'skills',self.root/'agents')
  file=self.root/'skills/pd-rfp/SKILL.md';file.write_text(file.read_text()+'\nlocal change\n')
  with self.assertRaises(ValueError):mod.install(self.root/'skills',self.root/'agents',True)
  self.assertIn('local change',file.read_text())
 def test_managed_upgrade(self):
  mod.install(self.root/'skills',self.root/'agents')
  r=mod.install(self.root/'skills',self.root/'agents',True)
  self.assertEqual(13,r['skills'])
 def test_package_tamper_rejected(self):
  original=mod.ROOT
  clone=self.root/'clone';shutil.copytree(original,clone)
  (clone/'README.md').write_text('tampered')
  try:
   mod.ROOT=clone
   with self.assertRaises(ValueError):mod.verify()
  finally:mod.ROOT=original

if __name__=='__main__':unittest.main()
