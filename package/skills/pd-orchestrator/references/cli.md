# Uso do CLI

Use `python3 /caminho/da/skill/pd-orchestrator/scripts/pd.py --project /caminho/do/projeto COMANDO`. A opção `--project` vem antes do comando. IDs são resolvidos somente no banco desse projeto. Consulte `--help` em cada comando.

## Iniciar e retomar

```text
init --name "Iniciativa" --owner "Responsável"
status
list --kind source
show SOURCE-ID
audit
export-audit --out /caminho/audit.jsonl
search "fechamento de caixa" --limit 10
neighbors ENT-001 --depth 2
impact ENT-001
context "como o estoque afeta o atendimento" --max-chars 12000 --limit 12
export-graph --dir /caminho/do/projeto/context-graph
context-feedback --actor reviewer --event-seq 24 --relevant-refs ENT-001 REL-001 --retrieved-relevant ENT-001 --omitted-relevant REL-001 --irrelevant SRC-002 --harness-tokens 1200 --reviewed-response-ms 45000 --rating 4
context-accept --actor reviewer --ids ENT-001 ENT-002 REL-001 --rationale "Fontes confrontadas e relações revisadas"
context-metrics
```

`status` verifica integridade e retorna gates aprovados, tarefas pendentes, perguntas abertas e artefatos desatualizados. O export contém eventos com hashes; o banco e os blobs mantêm o conteúdo completo e devem ser preservados juntos.

## Fontes e afirmações

Prepare JSON e use `record source --actor research --id SRC-001 --file fonte.json`:

```json
{
  "title": "Relato inicial do responsável",
  "source_type": "user_report",
  "locator": "Conversa de intake, mensagem identificada pelo responsável",
  "content": "Conteúdo literal ou passagem com contexto e limitações."
}
```

Tipos de fonte: `document`, `web`, `user_report`, `fieldwork`, `simulation`. Fontes são imutáveis: correção ou complemento recebe outro ID. Para web, acrescente título original, URL, data de acesso, localização e limitações. O content é snapshot da passagem; o link sozinho não basta.

`record evidence --actor research --id EVD-001 --file evidencia.json`:

```json
{
  "title": "Observação apoiada em registro",
  "refs": ["SRC-001"],
  "observation": "O que o registro efetivamente permite afirmar.",
  "limitations": "Relato de uma pessoa; ainda não confrontado com outras fontes."
}
```

Uma fonte sintética é recusada como evidência. Conteúdo apoiado em um relato mantém a limitação do relato. Hipóteses usam `record hypothesis`; questões usam `record question` com `status: open|resolved`, `blocking: true|false`, `gates: ["G1"]`, impacto e responsável. Resolução de questão exige refs para a resposta. Personas seguem o template de persona.

Decisões humanas de escopo, investimento ou regras usam `human-decision --actor "human:Responsável" --file decisao.json`. O JSON exige `title`, `decision_type`, `rationale` e `refs` para a manifestação/contexto. O owner confirma o resumo e um desafio no terminal. Isso registra a decisão de negócio, sem aprovar automaticamente um gate. `record decision` permanece restrito às três categorias delegadas de baixa complexidade.

## Grafo de domínio e recuperação

O ledger continua sendo a fonte oficial. O grafo é reconstruído a partir de registros `entity` e `relation`; não há um segundo banco ou cópia editável. IDs, versões, hashes, ator e referências de origem permanecem nos registros. Use `search` para busca lexical com normalização de acentos/aliases, `neighbors` para navegar relações em até quatro saltos, `impact` para percorrer impactos direcionais, e `context` para montar um pacote JSON limitado que o agente recebe como contexto. A busca lexical é determinística; não requer embeddings ou serviço externo. `context` informa caracteres efetivamente emitidos e deixa `token_count` nulo para o harness preencher, sem estimar tokens por caracteres.

Entidades aceitas: `domain`, `process`, `rule`, `requirement`, `decision`, `risk`, `persona`, `system`, `data`, `gate`, `artifact` e `concept`. Relações aceitas: `supports`, `contradicts`, `depends_on`, `affects`, `owned_by`, `used_in`, `produces`, `blocks`, `replaces`, `revokes`, `related_to`. Toda entidade e relação aponta para uma fonte original ou evidência; relações exigem `certainty: confirmed|possible`. `impact` separa os resultados em `confirmed` e `possible`; se qualquer elo do caminho for possível, o resultado do caminho inteiro é possível.

Agentes propõem entidades/relações em JSON e submetem o lote com `ingest --actor ID --file proposals.json`. O lote é append-only, validado e transacional: erros rejeitam o lote inteiro. Propostas não entram em busca, impacto, contexto nem exportação até uma aceitação registrada com `context-accept` por `reviewer` independente ou pelo owner humano. A aceitação registra versão proposta, racional e responsável. Não sobrescreva fontes para corrigir conteúdo: crie uma fonte nova e relacione explicitamente a substituição/revogação. O grafo oculta a relação anterior quando a relação de ciclo de vida aceita e atual existe; preserva ambas as fontes para conflito e auditoria. Relações derivadas de versões desatualizadas não são recuperadas.

Formato de proposta:

```json
{
  "entities": [
    {"id":"ENT-001","title":"Processo de fechamento","entity_type":"process","aliases":["fechamento do caixa"],"refs":["SRC-001"]},
    {"id":"ENT-002","title":"Rastreabilidade de movimentações","entity_type":"requirement","aliases":[],"refs":["EVD-001"]}
  ],
  "relations": [
    {"id":"REL-001","title":"Fechamento precisa explicar movimentações","subject":"ENT-001","predicate":"depends_on","object":"ENT-002","certainty":"possible","refs":["EVD-001"],"rationale":"A evidência sugere dependência; validar com responsável."}
  ]
}
```

Cada chamada de `context` retorna IDs, versões, hashes, origens, limite, truncamento e revisão de grafo. Inclua os IDs retornados nas referências do artefato de saída. Assim o mecanismo já existente de versões marca o derivado como desatualizado quando uma dependência muda. Não envie todo o ledger ao agente; recupere somente o pacote relacionado à tarefa. `export-graph --dir` gera notas Markdown com wikilinks e distinção entre ligações confirmadas e possíveis, que podem ser abertas como vault no Obsidian ou em outro editor. São projeções de leitura; alterações nelas não atualizam o ledger nem ingressam automaticamente no grafo.

Cada `context` grava no audit log um hash da pergunta, IDs/versões/hashes recuperados, tamanho em caracteres, truncamento e latência de recuperação. Para medir precisão/recall e omissões, uma revisão marca o conjunto relevante, quais itens foram recuperados e quais faltaram com `context-feedback`. A revisão rotula todos os itens recuperados como relevantes ou irrelevantes e informa o conjunto relevante total. O feedback também pode registrar tokens reportados pelo harness, tempo observado para revisar a resposta e nota de relevância. `context-metrics` agrega precisão, recall, cobertura de feedback, tokens disponíveis e latências. Sem rótulos humanos, o sistema não afirma precisão/recall. O tempo registrado por `context` mede apenas recuperação local; o tempo total requer medição no harness/revisor.

## Artefatos e revisão

```text
artifact --actor ba --id REQ-001 --file /caminho/requisitos.md --refs EVD-001 --tags requirements traceability --claims /caminho/claims.json
review --actor reviewer --target REQ-001 --verdict pass
review --actor reviewer --target REQ-001 --verdict rework --findings /caminho/findings.json
```

Os arquivos são copiados para blobs por hash; o original permanece editável. Registrar de novo o mesmo ID cria uma nova versão e exige novo parecer. `claims.json` é uma lista de `statement`, `status: supported|hypothesis`, `refs` e, quando aplicável, `location` (seção ou slide). Uma afirmação supported exige referência a evidência. Registre refs para todos os registros que sustentam a entrega, incluindo artefatos de origem de documentos e decks. Atualizar uma dependência marca derivados transitivamente como stale.

`findings.json` é uma lista de objetos com localização, severidade, achado, impacto e condição de resolução. Parecer pass requer lista vazia; não esconda findings em aprovação condicional. Pendências explicitamente aceitas no escopo devem ser tratadas no artefato e apresentadas ao humano.

## Rotas e tarefas

```text
route --text "Tarefa principal e contexto mínimo" --action "Classificar a responsabilidade" --expected-artifact "Rota recomendada" --gate G2 --python /caminho/laya/bin/python --model-path /caminho/modelo
dispatch --task TASK-ID --agent ba --refs EVD-001 --reason "Confirmação do System 2: tarefa de requisitos"
complete --task TASK-ID --actor ba --outputs REQ-001
```

`route` executa inferência Laya real em subprocesso com timeout. Informe ação, artefato esperado e gate atual; sem os três, a sugestão é sempre escalada ao System 2. Resultado inválido, contexto acima do orçamento, truncamento ou indisponibilidade também escala sem inventar rota. A tarefa preserva probabilidades, margem entre as duas melhores opções, uso informado pelo Laya, revisão do modelo, contexto em caracteres e limite de tentativas. Caracteres não são tokens; quando o harness não fornece tokens, a auditoria registra `not_reported_by_harness`. O despacho automático permanece desativado.

`references/execution-policy.json` define candidatos de modelo e esforço por tipo de tarefa, junto com limites de contexto, saída e tentativas. Eles são recomendações sujeitas à disponibilidade e aos esforços suportados pelo harness. Não altere a configuração global do Codex para aplicar esta política. Use entradas relevantes com referências e hashes; ao atingir limites, registre pendências, reduza o escopo preservando rastreabilidade ou escale. Não omita evidências exigidas nem faça tentativas silenciosas.

`dispatch` registra a confirmação do System 2 e torna a tarefa pronta; Codex aciona o agente e `complete` registra suas entregas. Repetir complete numa tarefa concluída é recusado. Tarefas já prontas/concluídas são identificadas ao retomar.

Agentes usam as skills de seus perfis e retornam grilling ao orquestrador. O CLI não dispara sozinho um processo de LLM.

## Gates humanos

```text
gate G0 --artifacts MANDATE-001
approve --request GATE_REQUEST-ID --actor "human:Responsável"
```

`gate` confere sequência, tags obrigatórias, revisões atuais, fontes versionadas e perguntas bloqueadoras. O owner deve executar `approve` no próprio terminal, revisar o resumo e digitar o desafio apresentado. Não há flag de aprovação automática. A confirmação aprova o hash daquela solicitação; mudança de dependências invalida a prontidão.

Um gate não pode pular os anteriores. É possível voltar e reaprovar uma fase afetada; gates derivados também precisam ser reavaliados. Não alterar diretamente o banco para contornar validação.

Após G5:

```text
handoff --recipient "Squad destinatária" --refs RFP-001 RTM-001 --pending "Pendências e responsáveis"
```

Registre evidência do aceite real do receptor e produza artefato com tag `handoff_acceptance`, revisão e solicitação G6. O humano confirma G6. O aceite não é exigido em G5, evitando a dependência circular da versão anterior.
