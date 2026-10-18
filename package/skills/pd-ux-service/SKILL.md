---
name: pd-ux-service
description: Analisar tarefas, jornadas, interação, acessibilidade e experiências de serviço.
---

# UX e serviço

## Experiência e serviço

Separe ações observadas de intenções e emoções inferidas. Modele jornada por ator e contexto, incluindo espera, canais, falhas, recuperação e acessibilidade. Considere linguagem, dispositivos e condições reais sem inferir capacidade individual a partir de escolaridade. Para protótipos e avaliações, defina tarefas, participantes, registro e critérios antes da coleta. Inspeção heurística e simulação não substituem testes de uso. Saída: jornadas, fluxos e plano de avaliação; carregue ferramentas de Product Design somente se instaladas e pertinentes.

## Contrato compartilhado

Receba do orquestrador o caminho explícito do projeto, ID da tarefa, objetivo, gate, versões das entradas e critérios de saída. Leia apenas esse contexto e as referências metodológicas necessárias. Nunca grave dados de projeto nas skills instaladas.

Use `pd-grilling` para decisões ou lacunas que mudem a conclusão. Investigue fatos disponíveis antes de perguntar. Retorne perguntas e recomendações ao orquestrador; ele coordena as rodadas com o humano. Ausência de evidência pode gerar uma tarefa de investigação; impede declarar a conclusão afetada como confirmada.

Selecione métodos em `pd-methods`. Personas fornecem perspectivas e hipóteses; respostas sintéticas não são observações de pessoas reais. Registre fontes, limitações, contradições e decisões. Mantenha `actor`, versões e referências no ledger, por meio do CLI de `pd-orchestrator/scripts/pd.py`.

Entregue: resumo da contribuição, artefatos versionados, fontes, hipóteses, perguntas, riscos, dependências afetadas e próximo responsável. Não aprove gates. Só delegue decisões reversíveis das categorias autorizadas; encaminhe as demais ao humano. O revisor não pode ser autor do artefato que revisa.
