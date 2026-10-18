# Revisão da orquestração anterior

A versão em `old_version/` especifica um fluxo sequencial de demanda até RFP, com contratos de handoff, hipóteses controladas, rastreabilidade e gates humanos. Esses elementos foram preservados e adaptados.

## Maturidade observada

O registro v1.0.0 declara prontidão para distribuição como pacote Markdown. O estado contém placeholders e fases não iniciadas. Nesta cópia não foram encontrados runtime, testes de comportamento ou registros de um discovery completo. Isso não permite concluir sobre execuções que tenham ocorrido fora dela.

## Melhorias incorporadas

| Problema anterior | Resposta na implementação inicial |
|---|---|
| Catálogo de 100 entradas confundido com métodos operacionalizados | Avaliações por técnica; procedimento específico ainda precisa ser preparado para a pesquisa concreta |
| Skills e agentes mantinham matrizes divergentes | Registro único de agentes utilizado em roteamento, dispatch e instalação |
| Aprovação de prontidão exigia handoff produzido depois | G5 avalia prontidão; handoff vem depois; G6 avalia aceite |
| Metadados podiam declarar baseline sem evento de aprovação | Aprovação vinculada ao hash de solicitação e confirmação interativa |
| Estado só documental | SQLite com transições, registros versionados, snapshots e auditoria |
| Revisão documental podia ser interpretada como validação de produto | Contratos separam evidência de produto, revisão de especificação e decisão humana |
| Hipóteses e referências podiam mudar sem revalidar derivados | Referências fixam versões; dependências alteradas marcam artefatos como stale |
| Fontes bibliográficas com marcadores não recuperáveis | Novas fontes exigem locator e passagem; não foram reaproveitadas alegações não verificadas |
| Regras do framework e estado de uma iniciativa se misturavam | Pacote genérico separado de cada banco de projeto |

## Limites que continuam exigindo avaliação

O runtime verifica estrutura, referências e transições; não demonstra por si só qualidade da evidência. Independência de agentes depende de execução em instâncias distintas no harness. Identidade humana e integridade contra adulteração total do armazenamento exigiriam controles externos. O roteamento Laya inicial não está calibrado no domínio. O piloto necessita de registros e decisões antes de chegar a uma RFP pronta para desenvolvimento.

Os documentos usados nessa comparação pertencem a um histórico local e não são distribuídos neste repositório. As conclusões acima resumem somente os aspectos necessários para explicar a evolução da implementação.
