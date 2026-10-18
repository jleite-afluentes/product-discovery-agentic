---
name: pd-project-charter
description: Preparar ou revisar Project Charter (Termo de Abertura) com fontes, escopo e autorização humana no discovery. Use para mandato ou abertura de projeto; para requisitos detalhados ou contratação, use as skills de BA e RFP.
---

# Termo de Abertura do Projeto

Atue sob o owner Product Manager (`pm`), recebendo projeto, tarefa, objetivo, gate e referências versionadas. Consulte o estado no CLI do orquestrador antes de redigir. Trabalhe somente no projeto indicado; nunca grave seu conteúdo na skill instalada.

## Mandato e conteúdo

Delimite qual iniciativa será autorizada: discovery, desenvolvimento ou outro recorte fornecido. Um mandato para investigar não autoriza construir o produto. Reutilize informações confirmadas e use `pd-grilling` para lacunas que alterem a autorização, retornando as perguntas ao orquestrador.

Use [charter-template.md](references/charter-template.md) como estrutura adaptável. Vincule afirmações materiais a IDs/versões de fontes e decisões. Separe fatos, propostas, premissas e pendências. Sem valores ou responsáveis informados, deixe orçamento, datas, patrocinador e alçadas pendentes; não invente compromissos. Objetivos e critérios mensuráveis propostos precisam ser rotulados até a decisão humana.

Prepare uma visão executiva concisa e acrescente detalhes somente quando necessários à decisão. Para IA, explicite autonomia proposta, supervisão, dados utilizados, critérios de avaliação e alternativa em caso de falha. Não atribua concordância, assinatura ou aprovação a uma persona sintética.

## Registro e autorização

Registre Markdown e seu mapa de fontes como artefatos com `actor=pm` e referências fixadas, usando os comandos de `pd-orchestrator/references/cli.md`. O template contém espaço para o ID e a versão de cada referência. Para um mandato em G0, a tag `mandate` pode ser usada quando o conteúdo atende aos critérios; ela não aprova o gate. Não altere critérios ou políticas para aprovar o documento.

Solicite revisão por instância distinta. Mantenha o status de rascunho ou pendente de autorização até existir manifestação real e recuperável da autoridade competente para esse escopo. Nome digitado, parecer favorável ou aprovação de G0 pelo owner não substituem a autorização do patrocinador quando forem pessoas ou alçadas diferentes. Encaminhe a decisão ao humano; não execute o desafio de aprovação em seu nome. Mudanças de escopo, orçamento e compromissos exigem nova decisão humana e revalidação dos derivados afetados.

## Entregáveis

Entregue o Charter, referências por seção, lacunas com owner/condição de resolução e o pedido de decisão. Para DOCX, use a skill Documents disponível no ambiente e revise a renderização; para PDF, use a capacidade PDF. Registre cada exportação como derivada da versão Markdown. Se a capacidade de exportação faltar, entregue o Markdown e declare a exportação pendente. `pd-presentations` pode preparar uma apresentação do mandato usando as mesmas versões de origem.

## Referência de terceiros

A referência executiva é a skill `project-charter` de Janelle Cipriano, preservada em [project-charter-upstream.md](references/project-charter-upstream.md), com a [licença MIT](references/LICENSE-Janelle-Cipriano.txt) e [revisão de origem](references/provenance.json). Consulte-a quando necessário para a forma de uma página. O tratamento de premissas e autorizações deste fluxo é o descrito acima. Esta skill não representa certificação do PMI.
