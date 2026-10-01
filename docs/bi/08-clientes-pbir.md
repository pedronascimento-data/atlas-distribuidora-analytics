# Implementação PBIR — Página 03: Clientes

> **Status:** definição PBIR criada; validação visual no Power BI Desktop pendente.

## Objetivo

Analisar tamanho, valor e concentração da carteira de clientes, além da distribuição geográfica do faturamento.

## Novas medidas

### Ranking Cliente

Ordena os clientes por faturamento dentro do contexto selecionado.

### Participação Top 10 Clientes %

Compara o faturamento dos dez maiores clientes com o faturamento total do contexto atual.

A medida respeita filtros de período, filial, UF e demais dimensões do modelo.

## Visuais implementados

| Visual | Tipo PBIR | Campo / medida |
|---|---|---|
| Clientes Compradores | cardVisual | `[Clientes Compradores]` |
| Ticket Médio | cardVisual | `[Ticket Médio]` |
| Faturamento Médio por Cliente | cardVisual | `[Faturamento por Cliente Médio]` |
| Concentração Top 10 | cardVisual | `[Participação Top 10 Clientes %]` |
| Ranking de clientes | barChart | cliente + `[Faturamento]` |
| Faturamento por UF | columnChart | UF + `[Faturamento]` |
| Carteira detalhada | tableEx | ranking, cliente, cidade, UF e KPIs |

## Tabela detalhada

A tabela contém:

- ranking;
- razão social;
- cidade;
- UF;
- faturamento;
- pedidos;
- ticket médio;
- participação no faturamento.

O cabeçalho utiliza `autoSizeColumnWidth` e `growToFit`, seguindo o padrão PBIR para tabelas.

## Leitura de negócio

A página permite responder:

1. quantos clientes efetivamente compraram;
2. quanto um pedido vale em média;
3. quanto cada cliente representa em receita média;
4. quanto os dez maiores clientes concentram;
5. quais clientes lideram faturamento;
6. em quais UFs a receita está concentrada.

## Validação no Desktop

- [ ] reconhecer os 7 visuais;
- [ ] validar Ranking Cliente;
- [ ] validar Participação Top 10 Clientes %;
- [ ] ordenar ranking por faturamento decrescente;
- [ ] aplicar Top N visual após renderização, se necessário;
- [ ] testar filtros de período;
- [ ] testar filtro por UF;
- [ ] testar filtro por filial;
- [ ] conferir total de clientes compradores;
- [ ] reconciliar faturamento com SQL;
- [ ] revisar largura das colunas da tabela.

## Critério de conclusão

A autoria PBIR está concluída. A página será considerada final após renderização e QA no Power BI Desktop.
