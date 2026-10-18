---
name: pd-grilling
description: Conduzir ou preparar rodadas de decisões e perguntas de discovery para agentes e personas, usando o grilling de Matt Pocock com coordenação do orquestrador.
---

# Grilling coordenado

Leia `references/grilling-upstream.md`, cópia atribuída da skill grilling de Matt Pocock. Preserve rodadas por dependências, recomendações e espera pelas respostas. O humano decide; fatos disponíveis são investigados pelos agentes. A confirmação de entendimento autoriza o escopo acordado, sem aprovar automaticamente os gates futuros.

Quando acionado como especialista, produza a árvore de decisões no recorte da tarefa: decisões resolvidas com fonte, fronteira pronta para perguntar, perguntas dependentes e recomendação com justificativa. Retorne ao orquestrador para ele agrupar a rodada. Só faça uma rodada direta se o orquestrador delegar essa interlocução. Não reinicie perguntas já respondidas no ledger.

Quando uma persona não tem informação suficiente para representar uma posição real, peça detalhes em vez de inventá-la. Questões exploratórias não são todas bloqueadoras: classifique qual conclusão ou gate depende de cada resposta.

Após a resposta humana, registre fonte com locator da conversa ou arquivo, vincule as questões resolvidas e recompute a fronteira. Apresente a síntese de entendimento antes de executar trabalho novo que dependa de decisões ainda não confirmadas.
