import os,json,time,hashlib,statistics
from pathlib import Path
os.environ['HF_HUB_OFFLINE']='1';os.environ['TOKENIZERS_PARALLELISM']='false'
p=Path('/private/tmp/pd-laya-investigation'); root=Path.cwd(); model=root/'.runtime/models/laya-multilingual'; lock=json.loads((model/'pd-model-lock.json').read_text())
def hashes():
 return {f:hashlib.sha256((model/f).read_bytes()).hexdigest()==h for f,h in lock['files'].items()}
report={'exploratory_post_results':True,'warning':'Designed after initial six ablations; paraphrases are no longer untouched holdout. No cases or labels changed. A second model load was authorized.','hash_before':hashes(),'conditions':{'order_permutations':['reversed','rotate_by_3'],'ovr':'10 binary A/B choice questions in one call; A=belongs, B=does not belong. Select maximum P(A); no calibrated routing confidence asserted.'},'results':[]}
cases=json.loads((p/'frozen_cases.json').read_text()); vs=json.loads((p/'frozen_variants.json').read_text()); base=vs[0]; pt=vs[2]; keys=list(json.loads((root/'package/skills/pd-orchestrator/references/routing.json').read_text())['routes'])
(p/'followup_results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
import laya,torch
torch.set_num_threads(4); ts=time.monotonic();a=laya.load(str(model),device='cpu');report['load_seconds']=time.monotonic()-ts
for v in [base,pt]:
 for perm in ['reversed','rotate_by_3']:
  inds=list(reversed(range(11))) if perm=='reversed' else list(range(3,11))+list(range(3)); criteria={v['labels'][i]:v['desc'][i] for i in inds}
  rows=[]
  for c in cases:
   ts=time.monotonic();r=a.system_one(c['text'],{'route':{'type':'choice','instructions':v['ins'],'criteria':criteria}},max_len=4096,head_max_len=1024);ans=r['answers']['route'];actual=keys[v['labels'].index(ans['choice'])]
   row={**c,'variant':v['name']+'_'+perm,'actual':actual,'correct':actual==c['expected'],'answer':ans,'usage':r.get('usage',{}),'ms':(time.monotonic()-ts)*1000};rows.append(row)
  report['results']+=rows;print(v['name'],perm,sum(r['correct'] for r in rows[:12]),sum(r['correct'] for r in rows[12:]),flush=True)
  (p/'followup_results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
questions={k:{'type':'choice','instructions':'A tarefa principal pertence a esta especialidade? '+pt['labels'][i],'criteria':{'A':pt['desc'][i],'B':'A tarefa principal não pertence a esta especialidade.'}} for i,k in enumerate(keys[:-1])}
report['conditions']['ovr_questions']=questions
for c in cases:
 ts=time.monotonic();r=a.system_one(c['text'],questions,max_len=4096,head_max_len=1024);scores={k:float(ans['probabilities']['A']) for k,ans in r['answers'].items()};ordered=sorted(scores,key=scores.get,reverse=True);chosen=ordered[0];actual=chosen if scores[chosen]>=.5 else 'abstain'; margin=scores[chosen]-scores[ordered[1]]
 report['results'].append({**c,'variant':'ovr_binary_pt','actual':actual,'correct':actual==c['expected'],'answer':r['answers'],'positive_scores':scores,'margin':margin,'score':scores[chosen],'usage':r.get('usage',{}),'ms':(time.monotonic()-ts)*1000})
report['hash_after']=hashes();(p/'followup_results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
rr=[r for r in report['results'] if r['variant']=='ovr_binary_pt'];print('ovr_binary_pt',sum(r['correct'] for r in rr[:12]),sum(r['correct'] for r in rr[12:]),flush=True)
print('HASHES',all(report['hash_before'].values()),all(report['hash_after'].values()),flush=True)
