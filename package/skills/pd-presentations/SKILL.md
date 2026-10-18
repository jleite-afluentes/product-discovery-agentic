---
name: pd-presentations
description: Produzir decks executivos e técnicos com vínculo entre slides e artefatos.
---

# Apresentações

## Deck executivo e técnico

Produza storyline antes da renderização. Executivo/comercial: contexto, problema, oportunidade, evidência, proposta, valor esperado, riscos, roadmap e decisões. Técnico: arquitetura e alternativas, jornadas, contratos, dados, integrações, requisitos, avaliação de IA, migração e aceite. Ajuste a extensão ao público.

Cada slide terá título que comunica uma conclusão e referências aos IDs/versões no mapa de slides e nas notas quando possível. Números e promessas exigem fonte ou rótulo de hipótese. Escolha o formato pelo pedido e consulte [entrega de apresentações](references/delivery.md) para os motores aprovados: Presentations para PPTX e Slidev para decks técnicos em Markdown/HTML. Carregue somente a skill e as referências do formato utilizado. Inspecione a renderização e registre o fonte, os exports e seu mapa como artefatos derivados. Sem ferramenta de renderização, entregue roteiro e declare exportação pendente, sem chamar Markdown de PowerPoint.

## Contrato compartilhado

Receba do orquestrador o caminho explícito do projeto, ID da tarefa, objetivo, gate, versões das entradas e critérios de saída. Leia apenas esse contexto e as referências metodológicas necessárias. Nunca grave dados de projeto nas skills instaladas.

Use `pd-grilling` para decisões ou lacunas que mudem a conclusão. Investigue fatos disponíveis antes de perguntar. Retorne perguntas e recomendações ao orquestrador; ele coordena as rodadas com o humano. Ausência de evidência pode gerar uma tarefa de investigação; impede declarar a conclusão afetada como confirmada.

Selecione métodos em `pd-methods`. Personas fornecem perspectivas e hipóteses; respostas sintéticas não são observações de pessoas reais. Registre fontes, limitações, contradições e decisões. Mantenha `actor`, versões e referências no ledger, por meio do CLI de `pd-orchestrator/scripts/pd.py`.

Entregue: resumo da contribuição, artefatos versionados, fontes, hipóteses, perguntas, riscos, dependências afetadas e próximo responsável. Não aprove gates. Só delegue decisões reversíveis das categorias autorizadas; encaminhe as demais ao humano. O revisor não pode ser autor do artefato que revisa.
