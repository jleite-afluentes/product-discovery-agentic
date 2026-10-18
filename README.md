# Product Discovery Agentic

Orquestração local e reutilizável para conduzir discovery e preparar entregáveis rastreáveis para squads agênticas. Agentes especializados usam skills, grilling, métodos de design e gates humanos. Laya propõe rotas; o runtime mantém versões, referências, tarefas e auditoria.

## Pacote instalável

A versão atual é 0.4.0. Consulte [package/README.md](package/README.md) para instalação, uso e requisitos.

- 15 skills e 36 perfis de agentes e especialistas para o Codex.
- Project Charter rastreável e apresentações em PPTX ou Slidev técnico.
- 100 técnicas avaliadas por aplicabilidade, gate, critérios e handoff.
- Estado e auditoria por projeto, sem incluir dados de clientes no pacote.
- Grafo/RAG local reconstruído do ledger, busca lexical, contexto limitado e export Markdown para Obsidian.
- Laya local 0.4.11 com checkpoint multilíngue fixado.

O roteamento está em modo assistido: a avaliação inicial acertou 6 de 12 casos sintéticos e não justifica despacho automático. As aprovações de gates exigem uma pessoa. A auditoria local mantém versões e hashes; não é assinatura externa de identidade.

## Documentação

- [Arquitetura conceitual](docs/arquitetura_product_discovery_agentic.md).
- [Revisão da versão anterior](docs/revisao_old_version.md).
- [Investigação de acurácia e orçamento do Laya](docs/investigations/laya-2026-10-17/relatorio.md).
- [Métodos e contratos do orquestrador](package/skills/pd-methods/references/matrix.md) e [gates](package/skills/pd-orchestrator/references/gates.json).
- [Direitos autorais e atribuição](package/COPYRIGHT.md).
- [Skills aprovadas para apresentações e Project Charter](docs/artifact-skills.md).
- [Arquitetura de contexto, grafo e avaliação RAG](docs/context-rag.md).

Contextos e registros específicos de iniciativas permanecem fora deste repositório. O diretório `old_version/` é uma referência local e também não faz parte da publicação.

## Desenvolvimento

Execute os testes com Python 3.12 ou superior:

```sh
python3 -m unittest discover -s tests -v
```

Autor: João Leite de Oliveira Neto, PMP. Desenvolvido com apoio de Codex.
