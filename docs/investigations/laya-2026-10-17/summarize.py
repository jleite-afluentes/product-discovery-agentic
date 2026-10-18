import json,statistics
from pathlib import Path
p=Path('/private/tmp/pd-laya-investigation'); rows=json.loads((p/'results.json').read_text()); report=[]
for v in dict.fromkeys(r['variant'] for r in rows):
 rr=[r for r in rows if r['variant']==v]; s={'variant':v,'splits':{},'latency_ms':{'mean':round(statistics.mean(r['ms'] for r in rr),1),'min':min(r['ms'] for r in rr),'max':max(r['ms'] for r in rr)},'tokens':{},'truncation_count':0}
 for r in rr:
  conf=[]; margins=[]
  for stage in r['stages']:
   a=stage['answer']; pr=sorted(a.get('probabilities',{}).values(),reverse=True); margins.append(pr[0]-pr[1] if len(pr)>1 else None); conf.append(a['answer_confidence'])
   u=stage['usage']; s['truncation_count']+=bool(u.get('truncated') or u.get('state_tokens_dropped') or u.get('options'))
  r['stage_margins']=margins; r['path_min_confidence']=min(conf)
 for split in ['original','paraphrase','all']:
  ss=[r for r in rr if split=='all' or r['split']==split]; acc=sum(r['correct'] for r in ss); accepted=[r for r in ss if r['actual']!='abstain' and r['path_min_confidence']>=.8]
  s['splits'][split]={'n':len(ss),'correct':acc,'accuracy':acc/len(ss),'accepted_at_08':len(accepted),'coverage_at_08':len(accepted)/len(ss),'precision_at_08':sum(r['correct'] for r in accepted)/len(accepted) if accepted else None,'accepted_errors':[{k:r[k] for k in ['id','expected','actual','path_min_confidence','stage_margins']} for r in accepted if not r['correct']]}
 s['example_usage']=rr[0]['stages'][0]['usage']; report.append(s)
(p/'results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)); (p/'summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)); print(json.dumps(report,ensure_ascii=False,indent=2))
