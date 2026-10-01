# Implementação PBIR — Página 04: Produtos e Categorias

> **Status:** definição PBIR criada; validação visual no Power BI Desktop pendente.

## Objetivo

Analisar o mix comercial sob duas perspectivas: **escala de vendas** e **rentabilidade**.

## Novas medidas

### Ranking Produto

Classifica os produtos por faturamento no contexto atual de filtros.

### Participação Produto %

Calcula quanto cada produto representa do faturamento dentro do contexto selecionado.

## Visuais implementados

| Visual | Tipo PBIR | Campo / medida |
|---|---|---|
| Faturamento | cardVisual | `[Faturamento]` |
| Margem Bruta | cardVisual | `[Margem Bruta]` |
| Margem % | cardVisual | `[Margem %]` |
| Quantidade Vendida | cardVisual | `[Quantidade Vendida]` |
| Preço Médio Unitário | cardVisual | `[Preço Médio Unitário]` |
| Faturamento por categoria | barChart | categoria + faturamento |
| Margem % por categoria | barChart | categoria + margem % |
| Ranking de produtos | barChart | produto + faturamento |
| Mix detalhado | tableEx | ranking, categoria, SKU, produto e KPIs |

## Leitura de negócio

A página permite distinguir:

- categorias grandes em receita;
- categorias com maior rentabilidade;
- produtos líderes em faturamento;
- produtos de grande volume e preço médio baixo;
- produtos com maior participação no mix;
- produtos que faturam bem, mas comprimem a margem.

## Decisão sobre dispersão

A especificação inicial previa um gráfico de dispersão **faturamento × margem**.

Nesta versão PBIR foi priorizada uma tabela analítica detalhada, pois o papel semântico do scatter ainda não foi validado no Power BI Desktop. Após a primeira renderização, a tabela pode coexistir com um scatter nativo caso o Desktop gere uma definição PBIR estável.

## Validação no Desktop

- [ ] reconhecer os 9 visuais;
- [ ] validar Ranking Produto;
- [ ] validar Participação Produto %;
- [ ] ordenar faturamento por categoria;
- [ ] ordenar ranking de produtos;
- [ ] conferir margem % por categoria;
- [ ] testar filtro por categoria;
- [ ] testar filtro por período;
- [ ] testar filtro por filial;
- [ ] conferir total da tabela;
- [ ] reconciliar faturamento e margem com SQL;
- [ ] avaliar inclusão do scatter faturamento × margem.

## Critério de conclusão

A autoria PBIR está concluída. A página será considerada final após renderização e QA no Power BI Desktop.
