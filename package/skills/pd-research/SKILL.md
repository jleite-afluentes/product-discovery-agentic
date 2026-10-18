---
name: pd-research
description: Investigar fontes recuperáveis, preparar coleta humana e sintetizar evidências sem inventar observações.
---

# Pesquisa e evidências

## Fontes e coleta

Pergunte qual decisão precisa de evidência. Para Internet, prefira documentação do fornecedor para funcionalidades e fontes primárias para dados e métodos. Abra o conteúdo, registre URL, título, data de acesso, passagem ou localização e limites. Separe alegação comercial de comportamento observado. Não reutilize marcadores de citação sem bibliografia recuperável.

Planeje participantes e amostragem conforme a decisão. Registre pesquisa como planejada, aguardando coleta, coletada ou analisada. Acesso a um sistema não prova que um fluxo foi observado. Ligação mínima: fonte original → observação → achado → oportunidade. Evidência contraditória permanece visível. Exemplos inventados serão ilustrativos, nunca casos reais. Saída: plano e registro de evidências; destaque o que necessita de campo ou confirmação humana.

## Contrato compartilhado

Receba do orquestrador o caminho explícito do projeto, ID da tarefa, objetivo, gate, versões das entradas e critérios de saída. Leia apenas esse contexto e as referências metodológicas necessárias. Nunca grave dados de projeto nas skills instaladas.

Use `pd-grilling` para decisões ou lacunas que mudem a conclusão. Investigue fatos disponíveis antes de perguntar. Retorne perguntas e recomendações ao orquestrador; ele coordena as rodadas com o humano. Ausência de evidência pode gerar uma tarefa de investigação; impede declarar a conclusão afetada como confirmada.

Selecione métodos em `pd-methods`. Personas fornecem perspectivas e hipóteses; respostas sintéticas não são observações de pessoas reais. Registre fontes, limitações, contradições e decisões. Mantenha `actor`, versões e referências no ledger, por meio do CLI de `pd-orchestrator/scripts/pd.py`.

Entregue: resumo da contribuição, artefatos versionados, fontes, hipóteses, perguntas, riscos, dependências afetadas e próximo responsável. Não aprove gates. Só delegue decisões reversíveis das categorias autorizadas; encaminhe as demais ao humano. O revisor não pode ser autor do artefato que revisa.
