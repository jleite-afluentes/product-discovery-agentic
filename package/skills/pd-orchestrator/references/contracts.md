# Contratos e alçadas

## Tríade de responsabilidades

O owner humano estabelece políticas e aprova gates. Executores propõem e produzem. O revisor independente avalia sem editar o artefato de origem. O orquestrador aplica a política; Laya recomenda rotas permitidas, sem autoridade para mudar regras. Não confundir escolha de modelo com aprovação de negócio.

## Pacote de tarefa

`project_path`, `project_id`, `task_id`, owner lógico, objetivo, gate, IDs/versões das entradas, fontes, método, permissões, limites de execução e critério de saída. Até três tentativas de rework por tarefa antes de sintetizar a divergência e pedir decisão; não repetir chamadas indefinidamente. O host pode impor limites menores.

## Entrega entre agentes

Resumo; artefatos com hash e refs; afirmações e limites; hipóteses; contradições; perguntas com impacto; critérios satisfeitos e pendentes; próximo responsável. Subagente contribui; owner consolida. Nova informação não reescreve silenciosamente uma decisão aprovada.

## Aprovação e evidência

Parecer pass é recomendação técnica. Gate é aprovação humana. O runtime exige terminal interativo e desafio vinculado ao hash da solicitação; registra o texto digitado e o owner declarado. Isso reduz aprovações acidentais e impede o comando não interativo, mas não autentica a pessoa contra um operador com acesso à mesma máquina. A garantia de identidade exige controle externo de acesso/assinatura, fora deste pacote local.

Uma fonte registra um relato ou documento; não torna suas alegações verdadeiras automaticamente. Evidências mantêm limitações. Personas/simulações não fornecem validação de usuário. Review verifica semântica; tags e schemas apenas verificam estrutura.

## Isolamento e auditoria

Cada projeto tem UUID e banco próprio; refs são resolvidas só nele. Conteúdo de clientes não entra no pacote. O ledger mantém eventos encadeados por hash, versões imutáveis e snapshots de arquivos. Mudanças em referências propagam a condição stale. Exporte e guarde o head externamente se precisar comparar integridade ao longo do tempo. A cadeia não é inviolável contra reescrita completa por quem controla o armazenamento.

## Métodos e gates

Gates têm critérios e tags em gates.json. Técnicas podem apoiar vários gates e ser repetidas. Não usar a presença de 100 nomes como prova de maturidade. A ficha de avaliação informa a adequação e os cuidados mínimos; execução de pesquisa requer protocolo específico aprovado, participantes e dados reais quando aplicável.
