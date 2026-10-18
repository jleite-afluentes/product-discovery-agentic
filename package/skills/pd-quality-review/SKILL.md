---
name: pd-quality-review
description: Confrontar fontes e critérios; emitir findings sem alterar o trabalho avaliado.
---

# Revisão independente

## Revisão independente

Receba versões exatas e critérios do gate, além das fontes originais. Não edite o artefato de origem. Examine suporte às afirmações, contradições, amostragem, dados sintéticos, RTM e dependências. Separe validade sobre o produto de completude documental. Para métodos, use a ficha e adapte critérios à decisão. Um campo preenchido não prova qualidade.

Registre parecer `pass`, `rework` ou `blocked`, achados, severidade, localização, impacto e condição de resolução. O CLI verifica autoria distinta e versão; a independência de execução depende de agente ou sessão separada. O parecer recomenda; o humano aprova. Saída: review registrado para o hash exato.

## Contrato compartilhado

Receba do orquestrador o caminho explícito do projeto, ID da tarefa, objetivo, gate, versões das entradas e critérios de saída. Leia apenas esse contexto e as referências metodológicas necessárias. Nunca grave dados de projeto nas skills instaladas.

Use `pd-grilling` para decisões ou lacunas que mudem a conclusão. Investigue fatos disponíveis antes de perguntar. Retorne perguntas e recomendações ao orquestrador; ele coordena as rodadas com o humano. Ausência de evidência pode gerar uma tarefa de investigação; impede declarar a conclusão afetada como confirmada.

Selecione métodos em `pd-methods`. Personas fornecem perspectivas e hipóteses; respostas sintéticas não são observações de pessoas reais. Registre fontes, limitações, contradições e decisões. Mantenha `actor`, versões e referências no ledger, por meio do CLI de `pd-orchestrator/scripts/pd.py`.

Entregue: resumo da contribuição, artefatos versionados, fontes, hipóteses, perguntas, riscos, dependências afetadas e próximo responsável. Não aprove gates. Só delegue decisões reversíveis das categorias autorizadas; encaminhe as demais ao humano. O revisor não pode ser autor do artefato que revisa.
