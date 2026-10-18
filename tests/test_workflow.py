import importlib.util
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'package/skills/pd-orchestrator/scripts/pd.py'
spec=importlib.util.spec_from_file_location('pd',path)
pd=importlib.util.module_from_spec(spec);spec.loader.exec_module(pd)

class Workflow(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
  self.p=pd.Project.init(self.root/'one','Fixture one','Owner')
  self.source=self.p.record('source','research',{'title':'brief','locator':'fixture:source','content':'A user describes a problem.','source_type':'user_report'},'SRC-1')
 def tearDown(self):
  self.p.db.close();self.tmp.cleanup()
 def artifact(self,ident='ART-1',tags=None,refs=None,actor='pm'):
  file=self.root/(ident+'.md');file.write_text('Draft '+ident)
  return self.p.artifact(actor,ident,file,refs or ['SRC-1'],tags or ['mandate'],[])
 def passed(self,ident='ART-1',tags=None,refs=None):
  a=self.artifact(ident,tags,refs);self.p.review('reviewer',ident,'pass',[]);return a
 def approve(self,request):
  challenge='APROVAR '+request['id']+' '+request['hash'][:12]
  with patch.object(sys.stdin,'isatty',return_value=True),patch('builtins.input',return_value=challenge):
   return self.p.approve_interactive(request['id'],'human:Owner')
 def test_state_survives_restart(self):
  other=pd.Project(self.root/'one');self.assertEqual(other.get('SRC-1')['hash'],self.source['hash']);other.db.close()
 def test_project_isolation(self):
  other=pd.Project.init(self.root/'two','Fixture two','Owner')
  with self.assertRaises(pd.Error):other.get('SRC-1')
  self.assertNotEqual(other.meta['id'],self.p.meta['id']);other.db.close()
 def test_init_does_not_overwrite(self):
  with self.assertRaises(pd.Error):pd.Project.init(self.root/'one','other','Owner')
 def test_simulation_not_evidence(self):
  self.p.record('source','personas',{'title':'synthetic','locator':'fixture:persona','content':'I would buy it','source_type':'simulation'},'SIM-1')
  with self.assertRaises(pd.Error):self.p.record('evidence','research',{'title':'demand','refs':['SIM-1'],'observation':'buy','limitations':'simulated'})
 def test_claim_support_requires_evidence(self):
  f=self.root/'a.md';f.write_text('claim')
  with self.assertRaises(pd.Error):self.p.artifact('pm','A',f,['SRC-1'],['mandate'],[{'statement':'verified demand','status':'supported','refs':['SRC-1']}])
 def test_review_not_self(self):
  self.artifact(actor='reviewer')
  with self.assertRaises(pd.Error):self.p.review('reviewer','ART-1','pass',[])
 def test_reviewer_role_required(self):
  self.artifact()
  with self.assertRaises(pd.Error):self.p.review('pm','ART-1','pass',[])
 def test_new_review_supersedes_pass(self):
  a=self.passed();self.p.review('reviewer','ART-1','rework',['Missing support'])
  self.assertFalse(self.p.artifact_passed(a))
 def test_new_artifact_requires_new_review(self):
  self.passed();self.artifact();self.assertFalse(self.p.artifact_passed(self.p.get('ART-1')))
 def test_dependency_change_marks_stale_transitively(self):
  self.p.record('hypothesis','pm',{'title':'H','refs':['SRC-1']},'H')
  self.passed(refs=['H']);self.artifact('DERIVED',['executive'],['ART-1'])
  self.p.record('hypothesis','pm',{'title':'H revised','refs':['SRC-1']},'H')
  self.assertTrue(self.p.stale(self.p.get('DERIVED')))
  self.assertIn('DERIVED',self.p.status()['stale_artifacts'])
 def test_gate_requires_current_independent_review(self):
  self.artifact()
  with self.assertRaises(pd.Error):self.p.gate_request('G0',['ART-1'])
 def test_gate_requires_tags(self):
  self.passed(tags=['other'])
  with self.assertRaises(pd.Error):self.p.gate_request('G0',['ART-1'])
 def test_gate_sequence(self):
  self.passed()
  with self.assertRaises(pd.Error):self.p.gate_request('G1',['ART-1'])
 def test_noninteractive_approval_rejected(self):
  self.passed();r=self.p.gate_request('G0',['ART-1'])
  with patch.object(sys.stdin,'isatty',return_value=False),self.assertRaises(pd.Error):self.p.approve_interactive(r['id'],'human:Owner')
 def test_agent_cannot_approve(self):
  self.passed();r=self.p.gate_request('G0',['ART-1'])
  with self.assertRaises(pd.Error):self.p.approve_interactive(r['id'],'orchestrator')
 def test_human_approval_is_bound_to_snapshot(self):
  self.passed();r=self.p.gate_request('G0',['ART-1']);self.approve(r)
  self.assertEqual(['G0'],self.p.active_gates());self.artifact();self.assertEqual([],self.p.active_gates())
 def test_new_blocker_prevents_pending_approval(self):
  self.passed();r=self.p.gate_request('G0',['ART-1'])
  self.p.record('question','pm',{'title':'missing','blocking':True,'status':'open','gates':['G0']})
  with self.assertRaises(pd.Error):self.approve(r)
 def test_source_immutable(self):
  with self.assertRaises(pd.Error):self.p.record('source','research',{'title':'replacement','content':'x','locator':'x','source_type':'document'},'SRC-1')
 def test_decision_alcada(self):
  with self.assertRaises(pd.Error):self.p.record('decision','pm',{'title':'change budget','scope':'low_complexity','reversible':True,'external_commitment':False,'decision_type':'investment','rationale':'why','refs':['SRC-1']})
 def test_ledger_tampering_detected(self):
  self.p.db.execute("UPDATE records SET body='{}' WHERE id='SRC-1'")
  with self.assertRaises(pd.Error):self.p.audit()
 def test_deleted_record_detected(self):
  self.p.db.execute("DELETE FROM records WHERE id='SRC-1'")
  with self.assertRaises(pd.Error):self.p.audit()
 def test_blob_tampering_detected(self):
  a=self.artifact();(self.p.home/a['body']['blob']).write_text('changed')
  with self.assertRaises(pd.Error):self.p.audit()
 def test_project_metadata_tampering_detected(self):
  self.p.meta['owner']='Other'
  with self.assertRaises(pd.Error):self.p.audit()
 def test_dispatch_resume_complete(self):
  task=self.p.dispatch(None,'pm',['SRC-1'],'investigate');self.artifact()
  self.p.finish_task(task['id'],'pm',['ART-1'])
  with self.assertRaises(pd.Error):self.p.finish_task(task['id'],'pm',['ART-1'])
  self.assertFalse(self.p.status()['tasks'])
 def test_missing_laya_escalates_no_fake_route(self):
  r=self.p.route('investigate',self.root/'missing-python')
  self.assertEqual(r['body']['state'],'awaiting_system2');self.assertIsNone(r['body']['candidate'])
 def test_invalid_laya_response_escalates(self):
  with patch('subprocess.run',return_value=subprocess.CompletedProcess([],0,'{"choice":"pm","confidence":NaN}','')):
   r=self.p.route('investigate','python')
  self.assertIsNone(r['body']['candidate'])
 def test_low_confidence_escalates(self):
  with patch('subprocess.run',return_value=subprocess.CompletedProcess([],0,'{"choice":"pm","confidence":0.2}','')):
   r=self.p.route('investigate','python')
  self.assertEqual(r['body']['state'],'awaiting_system2');self.assertEqual(r['body']['reason'],'abstention_or_low_confidence')
 def test_structured_context_and_route_telemetry(self):
  answer={"choice":"pm","confidence":0.91,"probabilities":{"pm":0.91,"research":0.05,"abstain":0.04},"model":"fixture-model","revision":"rev1","runtime":{"laya":"test"},"usage":{"input_tokens":30,"output_tokens":0,"state_tokens":12}}
  with patch('subprocess.run',return_value=subprocess.CompletedProcess([],0,json.dumps(answer),'')):
   r=self.p.route('priorizar oportunidade','python',action='classificar rota',expected_artifact='rota recomendada',gate='G1')
  body=r['body'];self.assertEqual('awaiting_system2',body['state']);self.assertTrue(body['context']['complete'])
  self.assertEqual([['pm',0.91],['research',0.05],['abstain',0.04]],body['top_candidates'])
  self.assertAlmostEqual(0.86,body['top_margin']);self.assertEqual({'source':'laya_usage','input_tokens':30,'output_tokens':0,'state_tokens':12},body['token_usage'])
 def test_incomplete_structured_context_forces_system2(self):
  with patch('subprocess.run',return_value=subprocess.CompletedProcess([],0,'{"choice":"pm","confidence":0.99}','')):
   r=self.p.route('investigate','python')
  self.assertEqual('structured_context_incomplete',r['body']['reason'])
  self.assertFalse(r['body']['context']['complete'])
 def test_unevaluated_high_confidence_not_auto_dispatch(self):
  with patch('subprocess.run',return_value=subprocess.CompletedProcess([],0,'{"choice":"pm","confidence":0.99}','')):
   r=self.p.route('investigate','python')
  self.assertEqual(r['body']['state'],'awaiting_system2')
 def test_long_input_rejected(self):
  r=self.p.route('x'*6001,'python')
  self.assertEqual('context_budget_exceeded',r['body']['reason'])
  self.assertEqual('awaiting_system2',r['body']['state'])
 def test_all_gates_then_handoff_without_cycle(self):
  for g in pd.policy()['gates']:
   if g['id']=='G6':self.p.handoff('rfp','Fixture squad',['G5-art'],'No blockers')
   ident=g['id']+'-art';self.passed(ident,g['required_tags'])
   self.approve(self.p.gate_request(g['id'],[ident]))
  self.assertEqual(7,len(self.p.active_gates()));self.assertTrue(self.p.audit()['ok'])

class PackageContracts(unittest.TestCase):
 def test_100_method_assessments(self):
  methods=json.loads((ROOT/'package/skills/pd-methods/references/methods.json').read_text())
  self.assertEqual(100,len(methods));self.assertEqual(100,len({m['id'] for m in methods}))
  agents=pd.registry()['agents'];gates={g['id'] for g in pd.policy()['gates']}
  for m in methods:
   self.assertIn(m['owner'],agents);self.assertTrue(set(m['gates'])<=gates)
   for field in ['inputs','outputs','acceptance','decision_and_limits','persona_handoff','handoff_to']:self.assertTrue(m[field])
class Regressions(unittest.TestCase):
 setUp=Workflow.setUp
 tearDown=Workflow.tearDown
 artifact=Workflow.artifact
 passed=Workflow.passed
 approve=Workflow.approve
 def test_future_nonblocking_question_does_not_invalidate_gate(self):
  self.p.record('question','pm',{'title':'future','blocking':False,'status':'open','gates':['G3']},'Q-future')
  self.passed();self.approve(self.p.gate_request('G0',['ART-1']))
  self.p.record('question','pm',{'title':'future','blocking':False,'status':'resolved','gates':['G3'],'refs':['SRC-1']},'Q-future')
  self.assertEqual(['G0'],self.p.active_gates())
 def test_stale_task_cannot_complete_and_can_replan(self):
  self.p.record('hypothesis','pm',{'title':'Input','refs':['SRC-1']},'INPUT')
  task=self.p.dispatch(None,'pm',['INPUT'],'Investigate')
  self.artifact(refs=['INPUT'])
  self.p.record('hypothesis','pm',{'title':'Input changed','refs':['SRC-1']},'INPUT')
  with self.assertRaises(pd.Error):self.p.finish_task(task['id'],'pm',['ART-1'])
  self.p.dispatch(task['id'],'pm',['INPUT'],'Replan with new input')
  self.artifact(refs=['INPUT']);self.p.finish_task(task['id'],'pm',['ART-1'])
 def test_unrelated_output_cannot_complete(self):
  self.p.record('hypothesis','pm',{'title':'Input','refs':['SRC-1']},'INPUT')
  task=self.p.dispatch(None,'pm',['INPUT'],'Investigate');self.artifact()
  with self.assertRaises(pd.Error):self.p.finish_task(task['id'],'pm',['ART-1'])
 def test_human_business_decision(self):
  body={'title':'Scope change','rationale':'Owner choice','refs':['SRC-1'],'decision_type':'change_scope'}
  challenge='DECIDIR '+pd.sha(pd.canonical(body)+pd.canonical([self.source['hash']]))[:12]
  with patch.object(sys.stdin,'isatty',return_value=True),patch('builtins.input',return_value=challenge):
   r=self.p.human_decision('human:Owner',body)
  self.assertEqual('human',r['body']['authority'])
 def test_agent_cannot_use_human_business_decision(self):
  with self.assertRaises(pd.Error):self.p.human_decision('pm',{'title':'Scope'})

if __name__=='__main__':unittest.main()
