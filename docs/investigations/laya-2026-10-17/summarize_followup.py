import json,statistics
from pathlib import Path
p=Path('/private/tmp/pd-laya-investigation'); d=json.loads((p/'followup_results.json').read_text()); baseline=json.loads((p/'results.json').read_text()); summary=[]
for v in dict.fromkeys(r['variant'] for r in d['results']):
 rows=[r for r in d['results'] if r['variant']==v]; out={'variant':v,'original_correct':sum(r['correct'] for r in rows[:12]),'paraphrase_correct':sum(r['correct'] for r in rows[12:]),'mean_ms':round(statistics.mean(r['ms'] for r in rows),1),'truncations':sum(bool(r['usage'].get('truncated') or r['usage'].get('state_tokens_dropped') or r['usage'].get('options')) for r in rows),'errors':[]}
 for r in rows:
  if v!='ovr_binary_pt':
   pr=sorted(r['answer']['probabilities'].values(),reverse=True);r['margin']=pr[0]-pr[1];r['score']=r['answer']['answer_confidence']
  if not r['correct']:out['errors'].append({k:r[k] for k in ['id','expected','actual','score','margin']})
 if v!='ovr_binary_pt':
  bn='pt_short' if v.startswith('pt_short') else 'baseline'; ref={r['id']:r for r in baseline if r['variant']==bn};out['changed_predictions']=sum(r['actual']!=ref[r['id']]['actual'] for r in rows)
 accepted=[r for r in rows if r['actual']!='abstain' and r['score']>=.8];out['diagnostic_08_coverage']=len(accepted)/28;out['diagnostic_08_precision']=sum(r['correct'] for r in accepted)/len(accepted) if accepted else None;out['accepted_n']=len(accepted);out['accepted_errors']=[r['id'] for r in accepted if not r['correct']];summary.append(out)
d['summary']=summary;d['conditions']['ovr_abstention']='Fixed before OVR run: abstain when every P(A)<0.5; otherwise argmax P(A). This binary score is not calibrated or directly comparable with multiclass confidence. No threshold tuned on the 28 cases.'
(p/'followup_results.json').write_text(json.dumps(d,ensure_ascii=False,indent=2));(p/'followup_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print(json.dumps(summary,ensure_ascii=False,indent=2))
