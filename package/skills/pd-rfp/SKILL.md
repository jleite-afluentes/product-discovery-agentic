---
name: pd-rfp
description: Compor RFP para intake de squad agêntica, sem criar regras de negócio novas.
---

# Composição da RFP

## RFP e intake

Carregue o template em `pd-orchestrator/references/templates/rfp.md`. Consolide conteúdo de origem, sem introduzir regra nova. Informe maturidade por seção, evidência, decisão, prioridade e pendências com owner. Inclua processos, regras, jornadas, requisitos funcionais e não funcionais, dados, integrações, restrições, migração quando aplicável e critérios de aceite. Explicite o que a squad deve confirmar antes de implementar.

G5 avalia RFP e prontidão; depois prepare handoff com destinatário, versões, decisões, lacunas, acesso às fontes e dúvidas. Apenas G6 avalia aceite do receptor, evitando a circularidade anterior. Saída: RFP, RTM, checklist e pacote de handoff; documentação e decks podem ser solicitados aos especialistas.

## Contrato compartilhado

Receba do orquestrador o caminho explícito do projeto, ID da tarefa, objetivo, gate, versões das entradas e critérios de saída. Leia apenas esse contexto e as referências metodológicas necessárias. Nunca grave dados de projeto nas skills instaladas.

Use `pd-grilling` para decisões ou lacunas que mudem a conclusão. Investigue fatos disponíveis antes de perguntar. Retorne perguntas e recomendações ao orquestrador; ele coordena as rodadas com o humano. Ausência de evidência pode gerar uma tarefa de investigação; impede declarar a conclusão afetada como confirmada.

Selecione métodos em `pd-methods`. Personas fornecem perspectivas e hipóteses; respostas sintéticas não são observações de pessoas reais. Registre fontes, limitações, contradições e decisões. Mantenha `actor`, versões e referências no ledger, por meio do CLI de `pd-orchestrator/scripts/pd.py`.

Entregue: resumo da contribuição, artefatos versionados, fontes, hipóteses, perguntas, riscos, dependências afetadas e próximo responsável. Não aprove gates. Só delegue decisões reversíveis das categorias autorizadas; encaminhe as demais ao humano. O revisor não pode ser autor do artefato que revisa.
