# Avaliação de aplicabilidade das 100 técnicas

Esta matriz avalia as 100 entradas da lista original de Universal Methods of Design. A fonte identifica os nomes; gate, owner, critérios e limites são propostas operacionais deste pacote. Não equivale a verificar o livro nem a validar empiricamente os métodos em cada domínio. Antes de executar pesquisa, o agente prepara protocolo específico conforme a ficha, a decisão e o contexto.

As fichas completas, com entradas, saídas, participação das personas, critérios e handoff, estão em `methods.json`. Use o filtro por gate e decisão; não aplique todos os métodos por obrigação.

| ID | Técnica | Gates candidatos | Owner | Decisão e limites |
|---|---|---|---|---|
| UMD-001 | A/B Testing | G3 | research | Comparar uma métrica entre variantes com alocação definida; requer volume, desenho estatístico e janela adequados; mudanças simultâneas confundem o efeito. |
| UMD-002 | AEIOU | G0, G1 | research | Observar atividades, ambientes, interações, objetos e usuários; registrar observação separada da interpretação. |
| UMD-003 | Affinity Diagramming | G1, G2 | research | Agrupar unidades com referência às notas originais; frequência no corpus não representa prevalência populacional. |
| UMD-004 | Artifact Analysis | G0, G1, G3 | research | Examinar documentos e objetos usados no trabalho; distinguir procedimento prescrito de prática observada. |
| UMD-005 | Automated Remote Research | G1, G2, G3 | research | Coletar remotamente com instrumento e eventos definidos; verificar consentimento, seleção e qualidade dos dados. |
| UMD-006 | Behavioral Mapping | G0, G1 | research | Registrar comportamento por tempo e espaço; não inferir motivação só da posição observada. |
| UMD-007 | Bodystorming | G2, G3 | pm | Encenar alternativas em contexto; registrar aprendizados como hipóteses até confronto com usuários. |
| UMD-008 | Brainstorm Graphic Organizers | G2, G3 | pm | Estruturar geração de alternativas; volume de ideias não é evidência de valor. |
| UMD-009 | Business Origami | G0, G1, G4 | ba | Representar atores e trocas com objetos; confirmar relações e exceções com responsáveis. |
| UMD-010 | Card Sorting | G1, G2, G3, G4 | ux | Investigar agrupamentos feitos por participantes; registrar itens, amostra e diferenças entre grupos. |
| UMD-011 | Case Studies | G0, G1, G3 | research | Comparar casos contextualizados e fontes; explicitar limites de transferência ao projeto. |
| UMD-012 | Cognitive Mapping | G1, G2, G3, G4 | ux | Elicitar relações percebidas pelo participante; não apresentar o mapa sintético do agente como modelo mental observado. |
| UMD-013 | Cognitive Walkthrough | G3, G4, G5 | reviewer | Inspecionar uma tarefa passo a passo com critérios e avaliadores; resultado é avaliação especializada. |
| UMD-014 | Collage | G1, G2 | research | Usar composição visual para elicitar significados; interpretação precisa de fala e contexto do participante. |
| UMD-015 | Competitive Testing | G1, G2, G3, G4 | ux | Comparar alternativas com tarefas e condições equivalentes; familiaridade prévia pode enviesar. |
| UMD-016 | Concept Mapping | G1, G2 | research | Explicitar conceitos e relações; cada relação relevante requer origem ou rótulo de hipótese. |
| UMD-017 | Content Analysis | G1, G2 | research | Definir corpus e código de análise; registrar revisões do código e divergências de interpretação. |
| UMD-018 | Content Inventory & Audit | G4, G5 | ba | Inventariar conteúdo com localização, owner e critério de qualidade; não confundir presença com utilidade. |
| UMD-019 | Contextual Design | G0, G1 | research | Integrar observação e modelagem de trabalho; requer pesquisa contextual e consolidação verificável. |
| UMD-020 | Contextual Inquiry | G0, G1 | research | Investigar tarefas no contexto de execução; distinguir o observado, o explicado e as interferências do pesquisador. |
| UMD-021 | Creative Toolkits | G1, G2 | research | Preparar materiais para expressão dos participantes; não usar produção do agente como participação real. |
| UMD-022 | Critical Incident Technique | G0, G1 | research | Reconstruir incidentes específicos com sequência e consequência; relatos retrospectivos podem ser incompletos. |
| UMD-023 | Crowdsourcing | G1, G2 | research | Definir quem contribui e como selecionar contribuições; participação aberta não garante representatividade. |
| UMD-024 | Cultural Probes | G1, G2 | research | Coletar sinais de contexto com materiais e instruções; sondas não medem prevalência nem causalidade. |
| UMD-025 | Customer Experience Audit | G3, G4, G5 | reviewer | Inspecionar pontos de contato com evidências e critérios; separar achado de auditoria de experiência observada. |
| UMD-026 | Design Charette | G2, G3 | pm | Organizar sessão curta de alternativas com registro; documentar opiniões minoritárias e decisões. |
| UMD-027 | Design Ethnography | G0, G1 | research | Observar contexto e práticas com responsável por campo; não simular etnografia com personas. |
| UMD-028 | Design Workshops | G2, G3 | pm | Definir participantes, objetivo e decisão da sessão; registrar autores e discordâncias. |
| UMD-029 | Desirability Testing | G1, G2, G3, G4 | ux | Investigar percepção de alternativas com estímulos comparáveis; preferência declarada não prova compra. |
| UMD-030 | Diary Studies | G0, G1 | research | Coletar registros ao longo do tempo com prompts; avaliar adesão e lacunas de registro. |
| UMD-031 | Directed Storytelling | G0, G1 | research | Elicitar narrativa de evento vivido; preservar contexto e distinguir lembrança de observação direta. |
| UMD-032 | Elito Method | G1, G2 | research | Relacionar observação, julgamento e conceito; manter explícito o salto interpretativo. |
| UMD-033 | Ergonomic Analysis | G3, G4, G5 | reviewer | Avaliar adequação física e cognitiva da tarefa; requer competência e medições compatíveis quando físicas. |
| UMD-034 | Evaluative Research | G1, G2, G3, G4 | ux | Definir hipótese, participantes e critério de avaliação; não usar o termo como substituto de um protocolo. |
| UMD-035 | Evidence-based Design | G0, G2, G3, G5 | pm | Justificar escolhas pelo conjunto de evidências e limitações; decisão aprovada não transforma alegação em fato. |
| UMD-036 | Experience Prototyping | G2, G3 | ux | Construir experiência para explorar hipótese; separar o que foi simulado do que foi realmente oferecido. |
| UMD-037 | Experience Sampling Method | G0, G1 | research | Coletar respostas em momentos definidos; controlar carga do participante e viés de momentos capturados. |
| UMD-038 | Experiments | G3 | research | Predefinir hipótese, manipulação, resultado e contraprova; explicitar fatores de confusão. |
| UMD-039 | Exploratory Research | G0, G1 | research | Investigar território ainda aberto; delimitar o que o estudo consegue e não consegue concluir. |
| UMD-040 | Eyetracking | G1, G2, G3, G4 | ux | Medir atenção com equipamento e protocolo adequados; olhar não demonstra compreensão ou intenção. |
| UMD-041 | Flexible Modeling | G0, G1, G4 | ba | Modelar atores e fluxos de forma revisável; preservar versões e regras que sustentam alterações. |
| UMD-042 | Fly-on-the-Wall Observation | G0, G1 | research | Observar sem interferência deliberada; registrar contexto, limites de acesso e interpretação. |
| UMD-043 | Focus Groups | G1, G2 | research | Elicitar percepções coletivas com moderação; influência social impede tratar consenso como preferência individual. |
| UMD-044 | Generative Research | G1, G2 | research | Explorar necessidades e possibilidades com participantes; resultados geram hipóteses de solução. |
| UMD-045 | Graffiti Walls | G1, G2 | research | Coletar contribuições abertas em contexto; registrar exposição, autoria quando autorizada e viés de autoseleção. |
| UMD-046 | Heuristic Evaluation | G3, G4, G5 | reviewer | Aplicar heurísticas identificadas com severidade e exemplos; não substituir teste com usuários. |
| UMD-047 | Image Boards | G2, G3 | pm | Explorar referências e direção visual; aprovação estética não demonstra sucesso operacional. |
| UMD-048 | Interviews | G0, G1 | research | Preparar roteiro ligado à decisão e pedir episódios concretos; perguntas indutivas enviesam respostas. |
| UMD-049 | KJ Technique | G1, G2 | research | Agrupar e nomear relações preservando unidades de origem; consenso analítico não elimina contradições. |
| UMD-050 | Kano Analysis | G1, G2, G3 | research | Coletar respostas funcionais e disfuncionais com público definido; classificação depende da amostra e formulação. |
| UMD-051 | Key Performance Indicators | G0, G2, G3, G5 | pm | Definir fórmula, baseline, fonte, frequência e responsável; indicador sem dado disponível é plano de medição. |
| UMD-052 | Laddering | G0, G1 | research | Explorar relações entre atributos, consequências e valores; aprofundamento não prova causa objetiva. |
| UMD-053 | Literature Reviews | G0, G1, G3 | research | Definir pergunta, busca, seleção e limites; registrar fontes primárias e conflitos. |
| UMD-054 | The Love Letter & The Breakup Letter | G1, G2 | research | Elicitar vínculo e frustração com relatos dos participantes; expressão projetiva requer interpretação contextual. |
| UMD-055 | Mental Model Diagrams | G1, G2, G3, G4 | ux | Construir representação a partir de pesquisa; marcar regiões sem suporte e não inventar cognição. |
| UMD-056 | Mind Mapping | G1, G2 | research | Organizar conceitos e perguntas exploratórias; ligações propostas precisam de validação. |
| UMD-057 | Observation | G0, G1 | research | Registrar tarefa, contexto e sequência; identificar diferenças entre notas factuais e interpretação. |
| UMD-058 | Parallel Prototyping | G2, G3 | ux | Criar alternativas comparáveis antes de convergir; controlar fidelidade e tarefa avaliada. |
| UMD-059 | Participant Observation | G0, G1 | research | Registrar participação do pesquisador e seus efeitos; respeitar limites de acesso acordados. |
| UMD-060 | Participatory Action Research | G1, G2 | research | Planejar investigação e mudança com participantes; explicitar responsabilidades e efeitos das intervenções. |
| UMD-061 | Participatory Design | G1, G2 | research | Cocriar com envolvidos reais e registrar contribuições; persona sintética não substitui participação. |
| UMD-062 | Personal Inventories | G0, G1 | research | Investigar artefatos pessoais relevantes com permissão; limitar coleta ao necessário e contextualizar uso. |
| UMD-063 | Personas | G0, G1, G2, G4 | personas | Sintetizar padrões sustentados por fontes; usar proto-persona quando a base ainda é hipotética. |
| UMD-064 | Photo Studies | G0, G1 | research | Definir o que registrar e por quê; preservar contexto e limites de interpretação das imagens. |
| UMD-065 | Picture Cards | G1, G2 | research | Usar estímulos para elicitação; registrar a interpretação do participante em vez de atribuir significado. |
| UMD-066 | Prototyping | G2, G3 | ux | Escolher fidelidade pela hipótese e tarefa; protótipo demonstra uma proposta, não viabilidade completa. |
| UMD-067 | Questionnaires | G1, G2, G3 | research | Definir constructos e testar compreensão das perguntas; avaliar amostra e não resposta. |
| UMD-068 | RITE | G1, G2, G3, G4 | ux | Registrar cada mudança entre sessões e sua motivação; iteração não autoriza somar resultados de variantes como equivalentes. |
| UMD-069 | Remote Moderated Research | G1, G2, G3, G4 | ux | Verificar acesso, gravação, tarefa e moderação; limitações de dispositivo e conexão afetam o resultado. |
| UMD-070 | Research Through Design | G2, G3 | ux | Documentar o que cada construção revelou; separar reflexão do autor de evidência de uso. |
| UMD-071 | Roleplaying | G2, G3 | pm | Encenar papéis para revelar hipóteses e exceções; não atribuir falas simuladas a pessoas reais. |
| UMD-072 | Scenario Description Swimlanes | G0, G1, G4 | ba | Representar sequência por ator e handoffs; verificar condições, espera e exceções. |
| UMD-073 | Scenarios | G4, G5 | ba | Descrever gatilho, contexto e resultado; distinguir cenário real, futuro e excepcional. |
| UMD-074 | Secondary Research | G0, G1, G3 | research | Avaliar origem, data, método e pertinência de materiais existentes; não reproduzir alegações sem fonte recuperável. |
| UMD-075 | Semantic Differential | G1, G2, G3 | research | Definir pares de atributos e escala compreensível; comparar estímulos sob condições semelhantes. |
| UMD-076 | Shadowing | G0, G1 | research | Acompanhar trabalho real registrando sequência e interrupções; observar poucos casos limita generalização. |
| UMD-077 | Simulation Exercises | G2, G3 | ux | Testar cenários e recuperação com premissas explícitas; saída simulada não é dado de operação real. |
| UMD-078 | Site Search Analytics | G1, G3 | research | Verificar eventos, períodos, termos e cobertura; pesquisas vazias não revelam sozinhas a intenção. |
| UMD-079 | Speed Dating | G1, G2, G3, G4 | ux | Apresentar conceitos em rodadas comparáveis; reações rápidas orientam exploração, não compromisso de compra. |
| UMD-080 | Stakeholder Maps | G0, G1, G4 | ba | Identificar influência, responsabilidade e alçada com fontes; validar papéis desconhecidos. |
| UMD-081 | Stakeholder Walkthrough | G3, G4, G5 | reviewer | Percorrer cenário com responsável real; registrar aceite e divergências sem presumir autorização. |
| UMD-082 | Storyboards | G2, G3 | ux | Explicitar ator, contexto, sequência e benefício hipotético; narrativa convincente não valida demanda. |
| UMD-083 | Surveys | G1, G2, G3 | research | Definir população, recrutamento, instrumento e análise; explicitar seleção e incerteza. |
| UMD-084 | Task Analysis | G0, G1, G4 | ba | Decompor objetivo, passos, decisões e exceções a partir do trabalho; não confundir procedimento ideal com real. |
| UMD-085 | Territory Maps | G1, G2 | research | Mapear domínio, fronteiras e relações; destacar áreas não investigadas. |
| UMD-086 | Thematic Networks | G1, G2 | research | Relacionar códigos, temas e suporte por fonte; testar coerência e casos negativos. |
| UMD-087 | Think-aloud Protocol | G1, G2, G3, G4 | ux | Definir tarefa e orientação neutra; verbalização pode alterar desempenho e não revela todo o raciocínio. |
| UMD-088 | Time-aware Research | G0, G1 | research | Planejar observação em momentos e ciclos relevantes; não generalizar um único horário ou período. |
| UMD-089 | Touchstone Tours | G0, G1 | research | Pedir que participante explique locais e objetos significativos; interpretar com sua narrativa. |
| UMD-090 | Triading | G1, G2, G3, G4 | ux | Comparar trios para elicitar construtos; evitar impor categorias do pesquisador. |
| UMD-091 | Triangulation | G1, G2 | research | Confrontar fontes e métodos com independência conhecida; múltiplas cópias da mesma origem não são confirmação. |
| UMD-092 | Unobtrusive Measures | G1, G3 | research | Analisar sinais indiretos com origem e contexto; proxy exige justificativa e verificação. |
| UMD-093 | Usability Report | G3, G5, G6 | documentation | Relatar método, participantes, versões, achados e severidade; não omitir limitações e casos sem sucesso. |
| UMD-094 | Usability Testing | G1, G2, G3, G4 | ux | Observar tarefas com usuários reais e critérios predefinidos; teste não confirma sozinho valor comercial. |
| UMD-095 | User Journey Maps | G1, G2, G3, G4 | ux | Ligar etapas, canais, ações e dores às fontes; emoções inferidas permanecem hipóteses. |
| UMD-096 | Value Opportunity Analysis | G0, G2, G3, G5 | pm | Comparar oportunidades por dimensões de valor explícitas; pesos são decisões, não fatos do mercado. |
| UMD-097 | Web Analytics | G1, G3 | research | Verificar instrumentação, funil, período e qualidade; correlação de eventos não prova causalidade. |
| UMD-098 | Weighted Matrix | G0, G2, G3, G5 | pm | Explicitar critérios, pesos, notas e sensibilidade; resultado depende dos julgamentos de entrada. |
| UMD-099 | Wizard of Oz | G2, G3 | ux | Simular capacidade com operador e protocolo; documentar o que foi manual e as condições de avaliação. |
| UMD-100 | Word Clouds | G1, G2 | research | Usar como exploração lexical com limpeza e contexto; tamanho de palavra não demonstra importância ou sentimento. |
