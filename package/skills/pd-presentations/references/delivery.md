# Entrega de apresentações

`pd-presentations` mantém narrativa e rastreabilidade. O motor de apresentação executa layout e exportação; a presença de sua skill não comprova instalação do runtime.

## PowerPoint e apresentação executiva

Use a skill Presentations disponibilizada pelo ambiente. Para pedido de PPTX ou entrega local, selecione explicitamente saída local e revise cada slide renderizado. Preserve gráficos e texto editáveis quando a ferramenta permitir. As skills nativas da OpenAI são dependências do harness e não são copiadas para este pacote. Se faltarem, registre a exportação pendente e entregue roteiro/mapa de fontes; não mude de formato sem informar o usuário.

## Slidev técnico

Para deck técnico em Markdown/HTML, use a skill `slidev` incluída no pacote. Leia primeiro `slidev/references/core-syntax.md`; consulte as referências de diagramas, código e exportação conforme a tarefa. Escolha outro formato se o usuário tiver exigido PPTX editável e o resultado exportado não atender.

Mantenha o projeto Slidev dentro da iniciativa indicada, fora das skills instaladas. Confira Node e o gerenciador de pacotes, registre as versões e use dependências locais fixadas por lockfile. Instalá-las é uma etapa separada da instalação das skills. Não altere ferramentas globais. Para exportar, confira os requisitos de navegador descritos em `slidev/references/core-exporting.md`.

O export `pptx` do Slidev usa imagens por slide. `pptx-editable`, quando suportado pela versão instalada, pode manter partes como imagens e converter slides incompatíveis em imagens. Verifique o arquivo produzido e descreva suas limitações; não prometa edição completa. HTML interativo e PDF também precisam de revisão visual. Para executar HTML, examine scripts, imports e recursos remotos de fontes fornecidas antes de renderizar. Use recursos locais quando o contexto exigir operação sem rede; não publique ou faça deploy só para produzir o artefato local.

Conserve o Markdown, assets, lockfile e mapa por slide com IDs/versões. Notas e slides derivados de um Charter referenciam sua versão e mantêm o status de autorização. Renderização não aprova escopo, orçamento ou gate.
