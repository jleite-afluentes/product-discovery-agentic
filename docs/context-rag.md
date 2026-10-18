# Contexto, grafo e recuperação

## O que está implementado

A versão 0.4.0 trata o ledger SQLite isolado por projeto como fonte oficial. Registros versionados `entity` e `relation` formam um grafo tipado em tempo de consulta; não há banco paralelo. O grafo cobre processos, regras, requisitos, decisões, riscos, personas, sistemas, dados, gates, artefatos e conceitos. Relações guardam origem, racional e certeza `confirmed` ou `possible`.

O CLI fornece `search`, `neighbors`, `impact`, `context`, `ingest`, `context-accept`, `context-feedback`, `context-metrics` e `export-graph`. A busca é lexical, sem embeddings ou endpoint. `context` devolve um pacote JSON com IDs, versões e hashes, fonte, limite de caracteres, truncamento e latência. Cada chamada grava metadados auditáveis; texto da pergunta não é incluído no log, apenas seu SHA-256. A contagem de tokens fica nula até que o harness a informe.

Ingestão é append-only e transacional. Agentes propõem entidades e ligações com IDs únicos e referências a fonte/evidência. Falha de esquema rejeita o lote. Propostas ficam fora da busca e do contexto até `context-accept`, executado por `reviewer` independente ou pelo owner humano com um racional registrado. Fontes conflitantes permanecem; a pessoa responsável registra relações `replaces`/`revokes` explícitas e rastreáveis. Relações que dependem de versões superadas deixam de ser recuperadas. Artefatos downstream devem registrar os IDs do pacote para aproveitar a invalidação transitiva já existente.

`export-graph --dir` gera notas Markdown com wikilinks, aptas a abrir no Obsidian. O export é somente projeção; edições no vault não retornam ao ledger. O grafo exporta ligações confirmadas e possíveis com seus IDs e fontes para revisão visual.

## Avaliação

Cada recuperação mede latência local, caracteres, quantidade de registros e truncamento. Um revisor pode registrar com `context-feedback` quais registros eram relevantes, quais foram recuperados, quais faltaram, quais eram irrelevantes, consumo de tokens reportado pelo harness, tempo observado para revisar a resposta e uma nota de relevância. `context-metrics` agrega essas medidas e informa cobertura de feedback. Precisão e recall são calculados sobre esses rótulos:

- Precisão = itens relevantes recuperados / todos os itens recuperados que foram rotulados como relevantes ou irrelevantes.
- Recall = itens relevantes recuperados / conjunto total de itens relevantes informado pelo revisor.

Essas medidas só têm significado com rótulos completos. O projeto ainda não traz conjunto de benchmark nem metas/limiares; resultados iniciais devem ser coletados antes de ajustar ranking, escolher embeddings ou alegar melhoria de acerto. O tempo de recuperação não mede o tempo total de resposta; esse precisa ser reportado pelo harness ou revisor.

## Limites e decisão de arquitetura

Este é um RAG lexical/grafo: recuperação local seleciona registros e relações e os fornece ao agente antes de gerar o artefato. Embeddings ficam para uma etapa futura se os casos rotulados mostrarem falhas lexicais mensuráveis. Isso evita custo e dependência externa enquanto não há benchmark. RAG não implica embeddings.

O termo GraphRAG pode se referir especificamente à abordagem de Microsoft Research, que inclui extração de grafo e sumarização de comunidades. Esta implementação não afirma reproduzi-la. O grafo de links do Obsidian é apenas uma interface opcional; o vault não é fonte normativa nem requisito.

## Uso mínimo

```text
pd.py --project /path/to/project search "política de desconto" --limit 8
pd.py --project /path/to/project impact ENT-RULE-001
pd.py --project /path/to/project context "como desconto afeta fechamento de caixa" --max-chars 12000
pd.py --project /path/to/project export-graph --dir /path/to/project/context-graph
```

Para detalhes de esquemas e validações, consulte [o guia do CLI](../package/skills/pd-orchestrator/references/cli.md).

## Referências

- Obsidian Graph view: <https://help.obsidian.md/Plugins/Graph+view>
- Armazenamento local em Markdown no Obsidian: <https://help.obsidian.md/Files+and+folders/How+Obsidian+stores+data>
- Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*: <https://arxiv.org/abs/2005.11401>
- Microsoft Research, *GraphRAG: Unlocking LLM discovery on narrative private data*: <https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/>
