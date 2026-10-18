# Product Discovery Agentic

Pacote local de skills, agentes e runtime de estado para conduzir discovery e compor uma RFP rastreável para intake de uma squad agêntica. O Codex executa os agentes; o Laya propõe rotas; o Python mantém registros, versões e gates.

Versão 0.2.1. O Laya recebe contexto estruturado e mantém despacho automático desativado enquanto o roteamento não tiver evidência suficiente. A auditoria registra probabilidades, margem, uso informado, modelo, revisão, contexto e tentativas. A política por tarefa sugere modelos/esforços do harness e limites de contexto, saída e tentativas; a disponibilidade é confirmada em cada harness. Gates G0–G6 exigem aprovação humana.

## Conteúdo

- 13 skills, incluindo orquestração, PM com contexto de IA, pesquisa, BA, UX, viabilidade, personas, revisão, RFP, documentação, decks, métodos e grilling.
- Perfis nativos de agentes e especialistas para o Codex, sem fixar modelo ou alterar suas configurações globais.
- Avaliação de aplicabilidade das 100 técnicas, com gates, entradas, saídas, cuidados, personas e handoffs.
- CLI de estado com SQLite por projeto, referências versionadas, snapshots de artefatos e cadeia de auditoria.
- Instalador verificável e scripts para preparar o Laya isoladamente.
- Política configurável de modelos e orçamento por tarefa, sem alterar o modelo global.
- Seleção de contexto por evidências relevantes, com escalada explícita ao atingir limites.

## Instalação

Requer Python 3.11 ou superior para o instalador e Python 3.12 ou superior para o lock de dependências do Laya. O CLI de estado usa apenas a biblioteca padrão e suporta Python 3.9 ou superior. Execute os comandos dentro desta pasta extraída:

```bash
python3 scripts/install.py --verify-only
python3 scripts/install.py
```

O destino padrão das skills é `~/.agents/skills`; os agentes vão para `~/.codex/agents`. Para um ambiente que utilize `~/.codex/skills`, informe `--dest "$HOME/.codex/skills"`. Ambos os destinos podem ser alterados com `--dest` e `--agents-dest`.

O instalador verifica hashes e não copia projetos. Se encontrar um nome existente, para antes de substituir. `--upgrade` atualiza somente instalações gerenciadas sem edições locais. Não altera `config.toml`. Uma falha de disco pode deixar instalação parcial; reconcilie destinos gerenciados com `--upgrade`. Skills inteiras são substituídas atomicamente.

Abra um novo turno após instalar. Invoque `$pd-orchestrator` e informe o caminho do projeto. O harness precisa disponibilizar ferramentas de subagentes para executar os perfis em instâncias distintas. Sem elas, a coordenação pode ocorrer sequencialmente, mas revisão independente fica pendente de outra sessão ou pessoa.

## Laya local

O ambiente e o checkpoint ficam fora do pacote e dos projetos:

```bash
python3 scripts/setup_laya.py --runtime-dir "$HOME/.local/share/product-discovery-agentic" --download-model
```

A instalação deve ser executada com Python 3.12 ou superior; baixa dependências e um checkpoint multilíngue. A revisão do modelo é fixada, a normalização de compatibilidade do tokenizer é registrada e os arquivos preparados recebem hashes locais em `pd-model-lock.json`. `install-local.json` registra os caminhos do Python e do modelo. Inferência usa apenas esse checkpoint local, sem enviar conteúdo do projeto a um endpoint externo.

Ao instalar, `--runtime-config /caminho/install-local.json` permite registrar esses caminhos na skill do orquestrador como `local-runtime.json`. O arquivo é configuração de máquina, não faz parte da distribuição genérica e não contém contexto de clientes.

O lock de dependências foi testado em macOS ARM64 e Python 3.12. Outros sistemas podem exigir resolução compatível, sobretudo macOS Intel; preserve a versão do Laya e registre/teste qualquer alteração. O modelo não é incluído no ZIP. Não há credencial de API OpenAI exigida por este runtime; os agentes usam a sessão existente do Codex.

As recomendações de `references/execution-policy.json` são ponto de partida, não resultado de benchmark comparativo entre modelos. O Laya informa tokens de entrada, saída e estado na inferência; o harness do Codex pode não expor o consumo do agente. A auditoria distingue as fontes e marca como não informado o que não estiver disponível. Comprimento em caracteres serve apenas para impor o limite local de contexto e nunca é convertido em tokens.

## Primeiro projeto

```bash
python3 "$HOME/.agents/skills/pd-orchestrator/scripts/pd.py" --project "/caminho/do/projeto" init --name "Minha iniciativa" --owner "Responsável"
python3 "$HOME/.agents/skills/pd-orchestrator/scripts/pd.py" --project "/caminho/do/projeto" status
```

O contexto fica em `.pd/` dentro do projeto. Faça backup dessa pasta inteira. Os comandos de trabalho estão em `skills/pd-orchestrator/references/cli.md`.

## Governança e limites

Owner humano define regras e aprova gates; executores produzem; reviewer em instância distinta revisa. Agentes só podem registrar decisões delegadas de organização de evidências, escolha de template e seleção de método previamente autorizado. Alterações de escopo, regras e compromissos voltam ao humano.

Aprovação usa desafio em terminal interativo vinculado à solicitação. O sistema registra uma atestação do operador, não uma identidade autenticada externamente. A cadeia de hashes detecta alterações contra o histórico atual; não impede reescrita completa por quem controla o armazenamento. Exporte o head para um local independente quando precisar comparar integridade ao longo do tempo.

Schemas, tags e verificações de versão asseguram estrutura e referências. A revisão humana e dos especialistas avalia a adequação das evidências, dos experimentos e da RFP. Produzir arquivos não comprova validação do produto.

## Direitos autorais, referências e atribuição

- [Skills no Codex](https://learn.chatgpt.com/docs/build-skills) e [agentes personalizados](https://learn.chatgpt.com/docs/agent-configuration/subagents).
- [Laya](https://github.com/NandhaKishorM/laya), versão de biblioteca fixada em 0.4.11. Dependência externa; licença Apache 2.0 no projeto de origem.
- [Grilling de Matt Pocock](https://github.com/mattpocock/skills), cópia atribuída e fixada com licença MIT em `pd-grilling/references/`.
- [Lista original de 100 métodos](https://designresearchmethods.com/universal-methods-of-design-100/). O pacote contém avaliações próprias de aplicabilidade, sem reproduzir o livro.

As contribuições originais deste pacote são de João Leite de Oliveira Neto, PMP. A skill Grilling upstream de Matt Pocock permanece atribuída e licenciada sob MIT, com o texto da licença incluído. Consulte [COPYRIGHT.md](COPYRIGHT.md) para as fronteiras de autoria e demais atribuições. Desenvolvido com apoio de Codex.
