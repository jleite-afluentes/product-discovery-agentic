import os,json,time,statistics,hashlib
from pathlib import Path
os.environ['HF_HUB_OFFLINE']='1'; os.environ['TOKENIZERS_PARALLELISM']='false'
ROOT=Path.cwd(); OUT=Path('/private/tmp/pd-laya-investigation')
config=json.loads((ROOT/'package/skills/pd-orchestrator/references/routing.json').read_text())
original=json.loads((ROOT/'tests/routing_cases.json').read_text())
# Frozen before evaluating any variant. These are semantic paraphrases, not independent holdout data.
extra=[('Precisamos escolher qual oportunidade traz mais valor e definir a direção do produto.','pm'),('Procure estudos oficiais sobre este problema e organize as evidências encontradas.','research'),('Descreva as regras para cancelar uma transação e as condições para aceitar esse requisito.','ba'),('Desenhe como o usuário passa pelas telas e identifique barreiras de uso.','ux'),('Descubra se a API suporta a integração e estime riscos da arquitetura proposta.','feasibility'),('Faça uma avaliação independente dos requisitos e aponte inconsistências.','reviewer'),('Monte o documento de solicitação de proposta para iniciar o trabalho da equipe.','rfp'),('Represente um gestor fictício com base nos depoimentos e indique o que ainda não sabemos sobre ele.','personas'),('Redija um manual técnico organizado com links para as decisões que o sustentam.','documentation'),('Crie uma apresentação de dez slides para a diretoria.','presentations'),('Autorize a passagem de fase e aprove a contratação.','abstain'),('Resolva o projeto inteiro para mim.','abstain'),('Faça uma pesquisa, desenhe telas e escreva contratos, sem prioridade entre essas tarefas.','abstain'),('Qual é a previsão do tempo amanhã?','abstain'),('Documente os resultados de uma pesquisa já concluída em um relatório técnico.','documentation'),('Revise de forma independente a qualidade de uma apresentação já concluída.','reviewer')]
cases=[dict(c,id='original-'+str(i+1),split='original') for i,c in enumerate(original)]+[dict(text=t,expected=e,id='paraphrase-'+str(i+1),split='paraphrase') for i,(t,e) in enumerate(extra)]
(OUT/'frozen_cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2))
ptlabels=['Gestão de produto','Pesquisa','Análise de negócio','Experiência do usuário','Viabilidade técnica','Revisão independente','RFP','Personas','Documentação','Apresentações','Abster-se']
enlabels=['Product management','Research','Business analysis','User experience','Technical feasibility','Independent review','RFP','Personas','Documentation','Presentations','Abstain']
ptdesc=['Estratégia, objetivos de negócio, valor e priorização de oportunidades.','Busca de fontes e evidências; planejamento de entrevistas e coleta.','Processos, regras de negócio, requisitos e critérios de aceite.','Jornadas, fluxos de interação, usabilidade e acessibilidade.','Arquitetura, APIs, integrações, dados, segurança e custos técnicos.','Auditoria e avaliação independente de qualidade; apontar inconsistências.','Composição da solicitação de proposta e pacote de intake para desenvolvimento.','Criação e consulta de perfis sintéticos de pessoas com fontes e lacunas.','Redação de documentos, manuais e relatórios executivos ou técnicos.','Criação de slides e apresentações executivas ou técnicas.','Pedido vago, tarefas sem prioridade, aprovação humana ou assunto fora de discovery.']
endesc=['Strategy, business goals, value and opportunity prioritization.','Find sources and evidence; plan interviews and data collection.','Processes, business rules, requirements and acceptance criteria.','Journeys, interaction flows, usability and accessibility.','Architecture, APIs, integrations, data, security and technical costs.','Independent quality audit and review; report inconsistencies.','Compose a request for proposal and development intake package.','Create and consult synthetic person profiles with sources and gaps.','Write documents, manuals and executive or technical reports.','Create slides and executive or technical presentations.','Vague request, unprioritized tasks, human approval or out-of-domain topic.']
keys=list(config['routes'])
baseins='Select the specialist responsible for the MAIN discovery task. If unclear or asking approval, abstain.'
ptins='Selecione o especialista responsável pela tarefa principal de discovery. Se o pedido for vago, exigir aprovação humana ou estiver fora do domínio, escolha Abster-se.'
variants=[dict(name='baseline',labels=keys,desc=[config['routes'][k]['description'] for k in keys],ins=baseins),dict(name='pt_instruction_only',labels=keys,desc=[config['routes'][k]['description'] for k in keys],ins=ptins),dict(name='pt_short',labels=ptlabels,desc=ptdesc,ins=ptins),dict(name='en_short_pt_input',labels=enlabels,desc=endesc,ins=baseins),dict(name='pt_short_json',labels=ptlabels,desc=ptdesc,ins=ptins,json=True),dict(name='pt_hierarchy',labels=ptlabels,desc=ptdesc,ins=ptins,hierarchy=True)]
(OUT/'frozen_variants.json').write_text(json.dumps(variants,ensure_ascii=False,indent=2))
print('FROZEN',hashlib.sha256((OUT/'frozen_cases.json').read_bytes()).hexdigest(),flush=True)
import laya,torch
torch.set_num_threads(4)
t0=time.monotonic(); agent=laya.load(str(ROOT/'.runtime/models/laya-multilingual'),device='cpu'); print('LOAD_SECONDS',time.monotonic()-t0,flush=True)
allresults=[]
def infer(state,labels,desc,ins):
 r=agent.system_one(state,{'route':{'type':'choice','instructions':ins,'criteria':dict(zip(labels,desc))}},max_len=4096,head_max_len=1024)
 return r['answers']['route'],r.get('usage',{})
groups={'Estratégia e descoberta':['pm','research','ux','personas'],'Modelagem e tecnologia':['ba','feasibility'],'Revisão e entregáveis':['reviewer','rfp','documentation','presentations'],'Abster-se':['abstain']}
groupdesc=['Definir direção e prioridades, pesquisar evidências, entender usuários, jornadas e personas.','Definir processos e requisitos ou avaliar arquitetura e viabilidade técnica.','Avaliar independentemente a qualidade ou produzir documentos, RFP e apresentações.','Pedido vago, sem prioridade, aprovação humana ou fora do domínio.']
for v in variants:
 rows=[]
 for c in cases:
  ts=time.monotonic(); state={'tarefa':c['text']} if v.get('json') else c['text']; stages=[]
  subset=keys
  if v.get('hierarchy'):
   ga,gu=infer(state,list(groups),groupdesc,'Escolha a categoria da tarefa principal.'); stages.append({'answer':ga,'usage':gu}); subset=groups[ga['choice']]
  if len(subset)==1:
   actual=subset[0]; a=stages[-1]['answer']; usage=stages[-1]['usage']
  else:
   ids=[keys.index(k) for k in subset]; labels=[v['labels'][i] for i in ids]; desc=[v['desc'][i] for i in ids]
   a,usage=infer(state,labels,desc,v['ins']); actual=subset[labels.index(a['choice'])]; stages.append({'answer':a,'usage':usage})
  row={**c,'variant':v['name'],'actual':actual,'correct':actual==c['expected'],'confidence':a['answer_confidence'],'stages':stages,'ms':round((time.monotonic()-ts)*1000)}; rows.append(row)
 summary={'variant':v['name'],'n':len(rows),'correct':sum(r['correct'] for r in rows),'original_correct':sum(r['correct'] for r in rows if r['split']=='original'),'paraphrase_correct':sum(r['correct'] for r in rows if r['split']=='paraphrase'),'mean_ms':round(statistics.mean(r['ms'] for r in rows)),'errors':[(r['id'],r['expected'],r['actual'],round(r['confidence'],3)) for r in rows if not r['correct']]}
 allresults.extend(rows); (OUT/'results.json').write_text(json.dumps(allresults,ensure_ascii=False,indent=2)); print(json.dumps(summary,ensure_ascii=False),flush=True)
