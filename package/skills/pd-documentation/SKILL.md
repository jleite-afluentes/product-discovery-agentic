---
name: pd-documentation
description: Escrever documentação executiva, comercial e técnica com referências por afirmação.
---

# Documentação

## Escrita e derivação

Defina audiência, decisão atendida e versão de origem. Executivo: problema, impacto, alternativas, recomendação, evidências e pedido de decisão. Comercial: público, proposta de valor, diferenciais comprovados ou hipóteses identificadas. Técnico: processos, requisitos, dados, interfaces, NFRs, riscos, aceite e pendências.

Mantenha Markdown editável. Cada afirmação material aponta para registros de origem; argumentos comerciais não aumentam a força da evidência. Para Word/PDF, use as skills de documentos/PDF disponíveis; se ausentes, entregue Markdown e registre a exportação pendente. Registre cada arquivo exportado como novo artefato com refs para o original, claims por seção e versão. Revise visualmente exportações. Uma derivação fica desatualizada quando a origem muda.

## Contrato compartilhado

Project Charter é preparado pelo owner PM com `pd-project-charter`; esta skill cuida da derivação documental. Use Documents do ambiente para DOCX e a capacidade PDF quando solicitado, preserve fontes e status de autorização e revise a renderização. Não trate formatação como aprovação do patrocinador.

Receba do orquestrador o caminho explícito do projeto, ID da tarefa, objetivo, gate, versões das entradas e critérios de saída. Leia apenas esse contexto e as referências metodológicas necessárias. Nunca grave dados de projeto nas skills instaladas.

Use `pd-grilling` para decisões ou lacunas que mudem a conclusão. Investigue fatos disponíveis antes de perguntar. Retorne perguntas e recomendações ao orquestrador; ele coordena as rodadas com o humano. Ausência de evidência pode gerar uma tarefa de investigação; impede declarar a conclusão afetada como confirmada.

Selecione métodos em `pd-methods`. Personas fornecem perspectivas e hipóteses; respostas sintéticas não são observações de pessoas reais. Registre fontes, limitações, contradições e decisões. Mantenha `actor`, versões e referências no ledger, por meio do CLI de `pd-orchestrator/scripts/pd.py`.

Entregue: resumo da contribuição, artefatos versionados, fontes, hipóteses, perguntas, riscos, dependências afetadas e próximo responsável. Não aprove gates. Só delegue decisões reversíveis das categorias autorizadas; encaminhe as demais ao humano. O revisor não pode ser autor do artefato que revisa.
