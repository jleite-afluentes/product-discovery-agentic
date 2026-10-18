# Arquitetura de Product Discovery Agentic

Proposta conceitual 0.1 — 17 de outubro de 2026.

Registro conceitual anterior ao grilling. O [pacote implementado](../package/README.md) e seu [catálogo de métodos](../package/skills/pd-methods/references/methods.json) têm precedência sobre esta proposta. Os registros históricos de iniciativas permanecem locais e não são distribuídos aqui.

O objetivo é transformar uma demanda em uma decisão de produto sustentada por evidências: investir, experimentar, reformular, adiar ou abandonar. A orquestração organiza o trabalho de agentes e pessoas, mantém a origem dos achados e permite revisar decisões quando novas evidências surgem.

O ponto de partida é a versão anterior em `old_version/`, que já contém agentes, rastreabilidade e um catálogo de 100 técnicas. Nesta proposta, RFP passa a ser uma saída possível quando houver necessidade de contratação. Outras saídas incluem um plano de experimentos, um briefing de produto, um backlog inicial ou uma decisão fundamentada de não desenvolver.

## Tríade de responsabilidades

“Trica de Responsabilidades Montesquieu” foi interpretada inicialmente como **tríade de responsabilidades inspirada na separação de poderes**. Montesquieu trata da separação entre funções legislativa, executiva e judiciária em *O Espírito das Leis*, livro XI, capítulo VI. Sua aplicação a agentes abaixo é uma analogia de arquitetura proposta para este projeto. [Fonte primária em tradução](https://constitutioncenter.org/the-constitution/historic-document-library/detail/montesquieuthe-spirit-of-the-laws-1748).

| Responsabilidade | Função na orquestração | Limite de autoridade |
|---|---|---|
| Normativa | Propor objetivos, critérios de evidência, permissões, orçamento e condições de passagem | Políticas entram em vigor com aprovação do responsável humano; não podem ser alteradas pela execução para aprovar o próprio resultado |
| Executiva | Planejar pesquisas, analisar material, produzir alternativas e preparar experimentos | Não aprova o próprio artefato nem transforma hipótese em fato |
| Revisora | Avaliar fontes, rastreabilidade, contradições e aderência aos critérios vigentes | Emite parecer e devolve trabalho; não modifica silenciosamente o artefato avaliado |

O responsável humano decide prioridades, compromissos, exceções e continuidade. O orquestrador coordena tarefas e estado dentro dessas alçadas. Parecer favorável de um agente não equivale à aprovação de investimento nem à validação de mercado.

Para tornar a separação efetiva, o runtime deverá manter permissões distintas, autoria e versão dos artefatos, critérios de revisão congelados por ciclo e registro das decisões. O revisor receberá fontes e critérios, além do resultado candidato. Apenas dar nomes diferentes a agentes não garante independência nem elimina vieses compartilhados.

## Laya como System 1

Requisito definido pelo usuário: utilizar Laya como IA de tomada de decisão, alternativa ao JEV. O [projeto Laya](https://github.com/NandhaKishorM/laya) descreve um motor não autorregressivo de decisões tipadas, com escolhas, escores e respostas sim ou não. A documentação de [roteamento de agentes](https://laya.studio/use-cases/agent-tool-routing) apresenta a aplicação na seleção de ferramentas e modelos.

Nesta arquitetura, System 1 e System 2 descrevem funções computacionais. São independentes da tríade de responsabilidades: rapidez de inferência não confere autoridade para criar regras ou aprovar entregas.

| Camada | Responsabilidade proposta |
|---|---|
| Regras determinísticas do runtime | Verificar permissões, estados, orçamento e transições autorizadas |
| System 1 com Laya | Classificar solicitações e recomendar uma rota entre opções permitidas |
| System 2 com agentes de raciocínio | Investigar ambiguidades, elaborar planos, sintetizar evidências e comparar alternativas |
| Revisão independente e decisão humana | Avaliar resultados e decidir nas alçadas definidas pela governança |

O fluxo será: verificar regras obrigatórias, consultar Laya quando a tarefa couber em uma decisão tipada, conferir a resposta e despachar para a rota permitida. Uma resposta ambígua, inválida, fora do domínio avaliado ou abaixo do limiar da tarefa seguirá para System 2 ou para o responsável humano, conforme a alçada. Se Laya estiver indisponível, o runtime deverá preservar as restrições e registrar o caminho alternativo adotado.

Aplicações iniciais candidatas:

- Classificar a intenção de uma demanda para sugerir a skill responsável.
- Selecionar uma família de métodos dentre opções previamente filtradas por pré-requisitos.
- Recomendar se uma tarefa delimitada pode seguir pela rota rápida ou exige análise aprofundada.
- Sinalizar material para revisão; a classificação será um indício, sem conferir validade factual ao conteúdo.

Cada chamada registrará tipo de decisão, opções, referências de entrada, versão do modelo e da configuração, resultado, escore quando disponível, rota efetiva e motivo de escalada. Os limites de entrada deverão ser verificados para impedir truncamento silencioso de evidências relevantes.

Laya não aprovará o próprio trabalho, alterará políticas nem substituirá evidências de usuários. Seu escore não será interpretado como probabilidade confiável de acerto sem avaliação e calibração na tarefa e no domínio do projeto.

Antes de habilitar rotas automáticas, o protótipo deverá avaliar exemplos de discovery em português, com casos ambíguos e contraditórios. A comparação incluirá regras simples e uma rota com System 2, medindo erros de encaminhamento, escaladas, latência e custo no ambiente real. Limiares serão definidos por tarefa a partir dessa avaliação. A distribuição, a versão, o hardware e a execução local ou hospedada ainda serão escolhidos; Laya não está instalado nem integrado ao projeto nesta etapa.

## Papéis propostos

| Papel | Responsabilidade principal | Entrega |
|---|---|---|
| Orquestrador | Escolher a próxima tarefa conforme estado, dependências e orçamento | Plano de trabalho e transições registradas |
| Curador de políticas | Preparar regras e critérios para aprovação humana | Política versionada |
| Especialista em problemas | Delimitar contexto, atores, sintomas e possíveis causas | Enquadramento e hipóteses |
| Planejador de pesquisa | Selecionar métodos e desenhar a coleta | Plano de pesquisa |
| Analista de evidências | Relacionar fontes, achados, divergências e limitações | Registro de evidências e síntese |
| Especialista em produto e experiência | Formular oportunidades e alternativas | Oportunidades, jornadas e conceitos |
| Planejador de experimentos | Definir como testar hipóteses críticas | Protocolo, métricas e regra de decisão |
| Revisor independente | Verificar qualidade metodológica e consistência | Parecer com achados e referências |
| Responsável humano | Decidir sobre problema, pesquisa, investimento e entrega | Decisão registrada e justificativa |

Esses papéis são contratos lógicos. O primeiro protótipo pode ter um coordenador, um executor e um revisor, com instruções especializadas para cada tarefa. A divisão em mais agentes depende dos resultados dos testes.

## Ciclo de discovery e problem solving

| Etapa | Pergunta que orienta o trabalho | Entrega mínima | Condição para avançar |
|---|---|---|---|
| Entrada | Qual decisão precisamos tomar e para quem? | Demanda, público, objetivo e restrições | Decisão pretendida identificada |
| Enquadramento | Qual é o problema e como se manifesta? | Enunciado, contexto, sinais e hipóteses | Sintomas separados de causas presumidas |
| Investigação | Que evidências distinguem as hipóteses? | Plano, fontes e dados coletados | Coleta suficiente para a decisão delimitada ou lacunas explicitadas |
| Síntese | O que os dados sustentam e o que contradizem? | Achados, oportunidades e incertezas | Conclusões ligadas às fontes |
| Alternativas | Quais intervenções podem melhorar o resultado? | Opções, incluindo manter a situação atual | Comparação por valor, risco, custo e viabilidade |
| Experimento | Qual hipótese vale testar primeiro? | Protocolo, métrica, limiar e regra de parada | Condições definidas antes da execução |
| Decisão | A evidência justifica continuar? | Resultado, parecer e decisão humana | Investir, repetir, reformular, adiar ou abandonar |

O ciclo permite retorno a qualquer etapa afetada por novas evidências. Uma mudança no problema deve marcar como pendentes de revisão os requisitos e experimentos que dependiam dele.

Para análise de causas, técnicas como 5 Porquês, diagrama de causa e efeito e árvores de hipóteses podem gerar explicações candidatas. A causa só recebe suporte quando confrontada com evidências; uma cadeia de respostas plausíveis não demonstra causalidade.

## Biblioteca de métodos

A referência inicial para “100 frameworks e metodologias” é o catálogo de *Universal Methods of Design* já presente no projeto. A [lista original publicada em Design Research Methods](https://designresearchmethods.com/universal-methods-of-design-100/) reúne 100 métodos. Eles compõem um repertório de seleção, sem obrigação de aplicar todos em cada discovery.

O [catálogo de métodos do pacote](../package/skills/pd-methods/references/methods.json) mantém a lista e as avaliações operacionais. Frameworks adicionais de problem solving terão identificação própria para preservar a composição desse catálogo.

Cada método deverá ter uma ficha com: identificador e fonte; pergunta atendida; entradas necessárias; procedimento; artefato de saída; recursos e participantes; limitações; critérios de conclusão; e modalidade de execução, distinguindo análise automatizável, facilitação humana e coleta com participantes.

O roteador selecionará métodos nesta ordem:

1. Identificar a decisão e a incerteza que impede tomá-la.
2. Verificar acesso a fontes, pessoas, tempo e instrumentos necessários.
3. Eliminar métodos incompatíveis com essas condições.
4. Recomendar uma opção e uma alternativa, justificando evidência esperada e limitações.
5. Registrar o plano e os critérios antes de iniciar a coleta.

Exemplos de roteamento propostos:

| Incerteza | Métodos candidatos | Evidência procurada |
|---|---|---|
| Como uma dificuldade aparece no trabalho real? | Entrevistas e investigação contextual | Relatos e observações situadas |
| Quais padrões aparecem no material coletado? | Análise temática e diagrama de afinidades | Temas ligados aos registros originais |
| Como as pessoas organizam informações? | Card sorting | Agrupamentos produzidos por participantes |
| As pessoas conseguem concluir uma tarefa? | Teste de usabilidade | Desempenho observado em tarefas definidas |
| Qual alternativa merece investigação? | Matriz ponderada | Comparação com critérios e pesos explícitos |

A matriz organiza julgamentos; seus escores não demonstram demanda. Personas sem pesquisa serão rotuladas como proto-personas. Simulações com IA poderão explorar cenários e revisar roteiros, mas não serão contadas como entrevistas, observações ou testes com usuários reais.

## Contratos e memória

Cada tarefa deverá informar objetivo, decisão atendida, papel responsável, referências de entrada, versão da política, método, permissões, orçamento e condição de término. Sua saída deverá registrar artefato, fontes utilizadas, hipóteses, lacunas, limitações e próximo passo proposto.

O estado compartilhado terá registros separados para evidências, hipóteses, decisões, riscos, perguntas e artefatos. Cada evidência terá origem, data, contexto de coleta e limitações. Uma decisão terá responsável, justificativa, alternativas consideradas e referências às evidências utilizadas.

A cadeia de rastreabilidade será:

```text
Fonte → Evidência → Achado → Oportunidade → Hipótese
      → Experimento → Resultado → Decisão → Entrega
```

Uma conclusão poderá apontar para múltiplas fontes, incluindo evidências contrárias. Alterações manterão o histórico e sinalizarão dependências afetadas.

## Estados e controle da execução

Fluxo mínimo: `recebido → em_planejamento → em_execucao → em_revisao → pronto_para_decisao → concluido`.

O revisor pode devolver a tarefa de `em_revisao` para `em_execucao` com achados específicos. Uma informação indispensável ausente leva a `aguardando_evidencia`; a retomada retorna à etapa afetada. `aguardando_decisao_humana` registra uma escolha fora da alçada dos agentes. Cada espera terá motivo, responsável e condição de retomada.

Critérios para marcar uma tarefa como pronta para decisão:

- Afirmações materiais vinculadas a fontes ou identificadas como hipóteses.
- Método compatível com a pergunta e com os dados realmente disponíveis.
- Contradições e limitações relevantes expostas.
- Revisão feita por papel distinto do autor, usando a versão correta dos critérios.
- Pendências que alteram a decisão explicitadas ao responsável humano.

O runtime deverá limitar custo, duração e tentativas. Ao atingir o limite, registrará o trabalho parcial e a necessidade de decisão humana. Reexecuções deverão reconhecer tarefas já concluídas para evitar duplicar coletas, artefatos ou ações externas.

## Primeiro incremento de desenvolvimento

O primeiro incremento deverá demonstrar um ciclo completo com uma demanda de exemplo e um conjunto pequeno de documentos fornecidos. A entrega será uma decisão rastreável, com lacunas reais preservadas.

1. Definir os esquemas de tarefas, evidências, hipóteses, pareceres e decisões.
2. Implementar estado persistente, permissões por papel e histórico de transições.
3. Implementar coordenador, executor e revisor com fontes citáveis.
   Integrar Laya por um adaptador de decisões tipadas, com validação de respostas, escalada e rastreabilidade; avaliar seu roteamento antes de habilitar decisões automáticas.
4. Preparar fichas operacionais de um subconjunto inicial dos 100 métodos e conectar o roteador.
5. Executar cenários de avaliação: fonte ausente, fontes contraditórias, autoaprovação, critério alterado durante revisão, orçamento esgotado e retomada após interrupção.
6. Comparar os resultados com revisão humana antes de ampliar agentes e métodos.

O incremento estará pronto quando conseguir retomar uma execução, impedir autoaprovação, preservar hipóteses como hipóteses e reconstruir a origem de cada recomendação material. Contar documentos produzidos ou agentes acionados não será critério de sucesso.

## Decisões ainda abertas

O usuário de referência, o domínio de produto, os dados disponíveis, o ambiente de execução e as integrações serão definidos antes da implementação operacional. A interpretação da tríade e o uso de *Universal Methods of Design* como catálogo inicial são premissas desta proposta, sujeitas a ajuste.
