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
