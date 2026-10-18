# Skills para apresentações e Project Charter

Seleção confirmada em 18 de outubro de 2026: A, B, F e G, usando E como referência.

| Opção | Integração | Estado na versão 0.3.0 |
| --- | --- | --- |
| A | `pd-presentations` + Presentations | Skill própria coordena narrativa/fontes; motor PPTX externo do ambiente |
| B | `slidev` oficial | Skill MIT incluída em revisão fixa; runtime de renderização separado |
| F | `pd-project-charter` | Skill própria, sob PM, com template, rastreabilidade e autorização humana |
| G | Documents | Dependência externa para DOCX e inspeção visual |
| E | `project-charter` de Janelle Cipriano | Referência upstream e template preservados com MIT; não instalada separadamente |

O roteamento do Charter permanece sob o PM. Não foi acrescentada uma classe ao Laya nem habilitado despacho automático. O Charter não altera as alçadas ou critérios dos gates. Uma autorização de discovery não é autorização de desenvolvimento; o patrocinador competente continua responsável pelo mandato.

Os arquivos do pacote são genéricos. Os projetos, bancos, configurações locais, modelos e entregáveis de clientes ficam fora do bundle. Nenhum arquivo das skills nativas OpenAI foi redistribuído.

Fontes primárias fixadas:

- [Slidev SKILL.md](https://github.com/slidevjs/slidev/blob/73053ab2b9653ed475960301b56e1ce4439d9c75/skills/slidev/SKILL.md) e [MIT](https://github.com/slidevjs/slidev/blob/73053ab2b9653ed475960301b56e1ce4439d9c75/LICENSE).
- [Project Charter de Janelle Cipriano](https://github.com/janellecipriano/pm-skills/blob/d2891d28bc77fb7dbaa2278689b6cc18431ef833/skills/project-charter/SKILL.md) e [MIT](https://github.com/janellecipriano/pm-skills/blob/d2891d28bc77fb7dbaa2278689b6cc18431ef833/LICENSE).
- [Direitos e fronteiras de autoria](../package/COPYRIGHT.md).

A evolução de memória de domínio/RAG permanece em especificação. Esta seleção acrescenta as capacidades de produção de artefatos; não declara aquele índice implementado.

## Verificação local

- 43 testes de workflow e instalação passaram com o Python compatível do ambiente.
- `quick_validate.py` aprovou `pd-project-charter` e `slidev`; o validador foi executado no ambiente existente com PyYAML.
- Instalador verificou os 150 arquivos declarados no manifesto. O ZIP contém 151 arquivos, incluindo o manifesto, com 15 skills e 36 perfis.
- Skills e referências upstream preservadas byte a byte, incluindo as licenças MIT. Links locais das instruções de Charter e entrega de apresentações foram verificados.
- ZIP inspecionado: sem projetos, estado de cliente, configuração local de runtime, modelos ou caches.
- Instalações gerenciadas em `~/.codex/skills` e `~/.agents/skills` atualizadas para 0.3.0, com runtime local preservado. Nenhuma configuração global de modelo alterada.
- SHA-256 do ZIP: `6973e27a962a604d6129db3291ff81484a0a9bd01ab7a9c81c2137f956ab6d90`.

Essas verificações cobrem instruções, integridade e instalação. Não foi produzido um deck ou Charter de cliente nesta atualização; renderizadores PPTX/DOCX do harness e o runtime Slidev serão exercitados quando houver uma entrega nesses formatos.
