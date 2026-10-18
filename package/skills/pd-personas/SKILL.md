---
name: pd-personas
description: Construir e consultar perspectivas sintéticas limitadas ao contexto autorizado do projeto.
---

# Facilitação de personas

## Personas com limites explícitos

Ficha mínima: pessoa/papel representado, tipo, contexto, objetivos conhecidos, responsabilidades, decisões autorizadas, restrições, comportamentos relatados, fontes, hipóteses e lacunas. Use identificadores do projeto. Peça detalhes quando a lacuna mudar a representação, conclusão ou recomendação. Não invente opiniões, personalidade, citações ou consentimento da pessoa real.

Ao consultar uma persona, identifique a pergunta, evidências fornecidas e limites. Sua resposta distingue posição conhecida, inferência e hipótese; pode produzir objeções e perguntas. O orquestrador decide a próxima rota. Mantenha respostas sintéticas como simulação ou hipótese e nunca como evidência de mercado. Saída: fichas e contribuições vinculadas, com questões para validação real.

## Contrato compartilhado

Receba do orquestrador o caminho explícito do projeto, ID da tarefa, objetivo, gate, versões das entradas e critérios de saída. Leia apenas esse contexto e as referências metodológicas necessárias. Nunca grave dados de projeto nas skills instaladas.

Use `pd-grilling` para decisões ou lacunas que mudem a conclusão. Investigue fatos disponíveis antes de perguntar. Retorne perguntas e recomendações ao orquestrador; ele coordena as rodadas com o humano. Ausência de evidência pode gerar uma tarefa de investigação; impede declarar a conclusão afetada como confirmada.

Selecione métodos em `pd-methods`. Personas fornecem perspectivas e hipóteses; respostas sintéticas não são observações de pessoas reais. Registre fontes, limitações, contradições e decisões. Mantenha `actor`, versões e referências no ledger, por meio do CLI de `pd-orchestrator/scripts/pd.py`.

Entregue: resumo da contribuição, artefatos versionados, fontes, hipóteses, perguntas, riscos, dependências afetadas e próximo responsável. Não aprove gates. Só delegue decisões reversíveis das categorias autorizadas; encaminhe as demais ao humano. O revisor não pode ser autor do artefato que revisa.
