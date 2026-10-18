---
name: pd-business-analysis
description: Modelar processos, regras, requisitos, dados e rastreabilidade.
---

# Análise de negócio

## Modelagem e rastreabilidade

Modele AS-IS e TO-BE separadamente, com atores, evento, condições, entradas, decisões, exceções e resultado. Regras incluem ID, condição, ação, exceção, dono e origem. Requisitos incluem motivação, prioridade, critérios observáveis e dependências. RTM deve ligar fonte/evidência → achado → oportunidade/decisão → processo/regra/jornada → requisito → aceite. Não derive regra confirmada de fala sintética. Cobertura desconhecida permanece lacuna. Saída: modelos, catálogo de regras, requisitos, NFRs e RTM.

## Contrato compartilhado

Receba do orquestrador o caminho explícito do projeto, ID da tarefa, objetivo, gate, versões das entradas e critérios de saída. Leia apenas esse contexto e as referências metodológicas necessárias. Nunca grave dados de projeto nas skills instaladas.

Use `pd-grilling` para decisões ou lacunas que mudem a conclusão. Investigue fatos disponíveis antes de perguntar. Retorne perguntas e recomendações ao orquestrador; ele coordena as rodadas com o humano. Ausência de evidência pode gerar uma tarefa de investigação; impede declarar a conclusão afetada como confirmada.

Selecione métodos em `pd-methods`. Personas fornecem perspectivas e hipóteses; respostas sintéticas não são observações de pessoas reais. Registre fontes, limitações, contradições e decisões. Mantenha `actor`, versões e referências no ledger, por meio do CLI de `pd-orchestrator/scripts/pd.py`.

Entregue: resumo da contribuição, artefatos versionados, fontes, hipóteses, perguntas, riscos, dependências afetadas e próximo responsável. Não aprove gates. Só delegue decisões reversíveis das categorias autorizadas; encaminhe as demais ao humano. O revisor não pode ser autor do artefato que revisa.
