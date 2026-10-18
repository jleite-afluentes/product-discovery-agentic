---
name: pd-feasibility
description: Investigar integrações, arquitetura, migração, segurança, custos e falhas de soluções com IA.
---

# Viabilidade técnica

## Viabilidade

Avalie dados, integrações, autorizações, isolamento entre tenants, migração, reconciliação e operação degradada quando relevantes. Diferencie informação documentada, experimento técnico e estimativa. Para IA, descreva limites, dados necessários, supervisão, avaliação e fallback. Referencie documentação oficial atual para contratos de software. Não invente API ou capacidade do fornecedor. Saída: opções arquiteturais, riscos, provas técnicas necessárias e requisitos não funcionais verificáveis.

## Contrato compartilhado

Receba do orquestrador o caminho explícito do projeto, ID da tarefa, objetivo, gate, versões das entradas e critérios de saída. Leia apenas esse contexto e as referências metodológicas necessárias. Nunca grave dados de projeto nas skills instaladas.

Use `pd-grilling` para decisões ou lacunas que mudem a conclusão. Investigue fatos disponíveis antes de perguntar. Retorne perguntas e recomendações ao orquestrador; ele coordena as rodadas com o humano. Ausência de evidência pode gerar uma tarefa de investigação; impede declarar a conclusão afetada como confirmada.

Selecione métodos em `pd-methods`. Personas fornecem perspectivas e hipóteses; respostas sintéticas não são observações de pessoas reais. Registre fontes, limitações, contradições e decisões. Mantenha `actor`, versões e referências no ledger, por meio do CLI de `pd-orchestrator/scripts/pd.py`.

Entregue: resumo da contribuição, artefatos versionados, fontes, hipóteses, perguntas, riscos, dependências afetadas e próximo responsável. Não aprove gates. Só delegue decisões reversíveis das categorias autorizadas; encaminhe as demais ao humano. O revisor não pode ser autor do artefato que revisa.
