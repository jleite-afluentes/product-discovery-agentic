# Investigação de acurácia do Laya

Investigação de 17 de outubro de 2026. Objetivo: identificar caminhos locais de melhoria do roteamento de discovery antes de treinamento ou mudança da instalação. O usuário confirmou avaliação separada de acerto, precisão das decisões aceitas e cobertura, priorizando formulação, categorias e hierarquia.

## Conclusão

Rótulos e descrições curtos em português elevaram o acerto dos 12 casos originais de 6 para 10. Nas 16 entradas adicionais, essa variante acertou 7. É uma candidata de desenvolvimento, sem evidência suficiente para promovê-la a roteador automático. A ordem das opções altera respostas e a confiança pode ser alta em erros. Não houve mudança no pacote ou na instalação.

## Método

Laya 0.4.11, checkpoint local convaiinnovations/laya-multilingual, revisão 1720e3e3357cfe1e281542e223f8273b0890ca34, CPU e quatro threads. Mesmos pesos, sem download ou treinamento. Seis formulações e 16 casos adicionais foram congelados antes da primeira rodada. Todos os casos são sintéticos; os 16 adicionais incluem paráfrases, ambiguidade, fora do domínio e fronteiras entre ação solicitada e assunto do artefato.

Houve 168 pares caso-configuração na primeira rodada. A hierarquia pode exigir mais de uma chamada por caso. Modelo carregado uma vez por rodada; tempos de inferência aquecida não representam o CLI integrado, que inclui carregamento e verificação do checkpoint. Diagnósticos de ordem e one-vs-rest foram definidos após os primeiros resultados e são exploratórios.

## Resultados da primeira rodada

| Configuração | Originais | Adicionais | Total |
|---|---|---|---|
| Configuração atual | 6/12 | 6/16 | 12/28 |
| Somente instrução em português | 8/12 | 5/16 | 13/28 |
| Rótulos e descrições curtos em português | 10/12 | 7/16 | 17/28 |
| Rótulos e descrições em inglês, tarefa em português | 6/12 | 9/16 | 15/28 |
| Português curto com estado JSON | 6/12 | 8/16 | 14/28 |
| Hierarquia em quatro grupos | 3/12 | 6/16 | 9/28 |

A variante portuguesa curta tem o maior total da rodada, mas não domina nos casos adicionais. A variante com descrições em inglês acertou 9/16 neles. Isso impede concluir que um único idioma de instrução seja a causa dos erros ou que a melhor configuração já tenha generalizado.

## Confiança e cobertura

No limiar diagnóstico 0,8, excluindo a resposta abstain, a configuração atual aceitaria 4/28 casos, dos quais 2 corretos. A portuguesa curta aceitaria 3/28, todos corretos, mas três observações não sustentam uma taxa confiável de precisão. A variante JSON aceitaria 9/28, com 8 corretos; chegou a encaminhar uma pergunta de previsão do tempo para viabilidade técnica com escore 0,9307.

Essas coberturas são hipotéticas. O pacote segue em modo assistido, com dispatch automático desativado. O limiar não foi ajustado nem validado para produção. Scores de perguntas binárias e de perguntas com onze opções não são diretamente comparáveis.

## Diagnósticos adicionais

Inverter ou rotacionar opções mudou de 7 a 11 das 28 previsões por condição, mantendo os textos. A variante portuguesa curta variou entre 7/12 e 10/12 nos originais; escolher a ordem que maximiza estes casos seria ajuste no próprio conjunto de desenvolvimento.

One-vs-rest usou dez perguntas choice A/B, escolhendo a maior P(A) e abstendo-se se todas fossem inferiores a 0,5, regra fixada antes desse diagnóstico. Resultado: 4/12 originais e 7/16 adicionais. Não melhorou o problema neste teste. A hierarquia específica testada também piorou; isso não demonstra que todas as decomposições possíveis falhem.

Todos os arquivos do lock mantiveram seus hashes antes e depois. Nenhuma condição reportou truncamento, descarte do estado ou colapso das opções.

## Auditoria do contrato atual

- Schema choice e campo answer_confidence estão corretos.
- O orçamento atual max_len=4096 e head_max_len=1024 comportou os exemplos. Aumentar esses limites não é correção sustentada pelos resultados.
- O estado de roteamento contém só texto livre, sem ação explícita, artefato esperado, gate ou conjunto de candidatos permitido. Investigar contexto estruturado é diferente de simplesmente envolver a mesma frase em JSON.
- O worker retorna probabilidades e uso de tokens; o ledger atual não persiste todos esses detalhes. Guardar distribuição, margem e versão do schema permitiria investigar confusões e instabilidade.
- Aprovação humana é uma restrição de autoridade, distinta de escolher especialista. Não deve depender exclusivamente de o modelo acertar uma classe chamada abstain.

## O que as fontes estabelecem

A documentação informa que texto e ordem das opções participam da pergunta, e que os escores precisam de ajuste e validação no domínio antes de serem usados como probabilidade confiável. [Questions and answers](https://nandhakishorm.github.io/laya/questions-and-answers/).

O model card declara que o checkpoint multilíngue é fornecido sem calibração e tem limitações zero-shot em decisões tipadas de workflows específicos. Isso é compatível com os resultados observados, sem provar uma causa única. [Model card](https://huggingface.co/convaiinnovations/laya-multilingual#limits).

O guia oferece ajuste fino a partir do modelo multilíngue, mas ganhos publicados em outros benchmarks não garantem ganho em discovery. [Fine-tuning](https://nandhakishorm.github.io/laya/finetune/).

Calibração por temperatura comum aos logits preserva a ordem das classes: pode melhorar a decisão de escalar, mas não aumenta sozinha o acerto bruto da rota. Ajuste de classificação e calibração são trabalhos diferentes.

## Desenho implementado na v0.2.0

1. A rota recebe ação, artefato esperado e gate; contexto ausente força escalada ao System 2. A autoridade humana continua fora da escolha de especialista.
2. Rótulos e descrições curtos em português viraram a configuração candidata. Nenhuma ordem de opções foi promovida com base no melhor resultado observado.
3. A auditoria conserva probabilidades, top três, margem, versão/runtime, uso e latência para investigar erros e instabilidade.
4. `execution-policy.json` organiza modelos e esforço por tipo de tarefa. Seleção de modelo é candidata, verifica o harness ativo e não altera a configuração global.
5. Orçamentos locais e behavior ao atingir limite estão documentados. Caracteres não representam tokens; o uso do Laya é guardado quando reportado e consumo do harness ausente é marcado explicitamente.
6. O dispatch automático continua desativado. Separação de conjuntos, revisão humana dos rótulos e avaliação por família semântica são requisitos para qualquer promoção futura.
7. Fine-tuning permanece condicionado a evidência posterior; não treinar nos 28 exemplos de desenvolvimento e apresentar a memorização como generalização.

O comportamento de ponta a ponta foi verificado com uma inferência real e 44 testes automatizados. Esse smoke de uma chamada não altera as métricas de acurácia da investigação. Consulte [validação 0.2.0](../../validation/validacao_0.2.0.md).

## Limitações e reprodução

Os 28 exemplos já foram inspecionados e passam a ser conjunto de desenvolvimento. Os rótulos foram definidos pela investigação, sem revisão humana independente; há casos de fronteira que podem admitir mais de um responsável dependendo do contrato. Não há teste final de produção nem avaliação com demandas reais. Os resultados não estabelecem uma garantia estatística de precisão, cobertura ou melhoria futura.

Scripts, configurações congeladas, casos e respostas completas acompanham este relatório. Eles usam o runtime e checkpoint locais já preparados. Resultados da primeira rodada estão em results.json e summary.json; diagnósticos posteriores em followup_results.json e followup_summary.json. Scripts não fazem parte do pacote instalado. Hashes do checkpoint constam no diagnóstico adicional.
