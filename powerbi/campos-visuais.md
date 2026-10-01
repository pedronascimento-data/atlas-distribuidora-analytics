# Mapa de Campos e Visuais — Power BI

Este documento reduz erros durante a montagem do `.pbix`.

## Visão Executiva

| Visual | Campo / Medida | Observação |
|---|---|---|
| Card Receita | `[Faturamento]` | moeda |
| Card Margem | `[Margem %]` | percentual |
| Card Ticket | `[Ticket Médio]` | moeda |
| Card Meta | `[Atingimento Meta %]` | percentual |
| Card MoM | `[Crescimento MoM %]` | percentual |
| Card Pedidos | `[Quantidade de Pedidos]` | inteiro |
| Linha mensal | `dim_data[ano_mes]` + `[Faturamento]` | ordenar cronologicamente |
| Faturamento x Meta | `dim_data[ano_mes]`, `[Faturamento]`, `[Meta]` | combo chart |
| Categoria | `dim_produto[categoria]`, `[Faturamento]` | barras |
| Top representantes | `dim_representante[representante]`, `[Faturamento]` | Top N = 5 |

## Performance Comercial

| Visual | Campo / Medida |
|---|---|
| Card Faturamento | `[Faturamento]` |
| Card Meta | `[Meta]` |
| Card Atingimento | `[Atingimento Meta %]` |
| Card Gap | `[Gap para Meta]` |
| Ranking | `dim_representante[representante]`, `[Ranking Representante]`, `[Faturamento]` |
| Comparativo | representante + `[Faturamento]` + `[Meta]` |
| Matriz | gerente → supervisor → representante |
| Evolução | `dim_data[ano_mes]` + `[Faturamento]` |

## Clientes

| Visual | Campo / Medida |
|---|---|
| Card clientes | `[Clientes Compradores]` |
| Card ticket | `[Ticket Médio]` |
| Card faturamento médio | `[Faturamento por Cliente Médio]` |
| Top clientes | `dim_cliente[razao_social]` + `[Faturamento]` |
| Receita geográfica | `dim_cliente[uf]` + `[Faturamento]` |
| Tabela | cliente, cidade, UF, faturamento, pedidos |
| Participação | `[Participação Cliente %]` |

## Produtos e Categorias

| Visual | Campo / Medida |
|---|---|
| Card faturamento | `[Faturamento]` |
| Card margem | `[Margem Bruta]` |
| Card margem % | `[Margem %]` |
| Card quantidade | `[Quantidade Vendida]` |
| Categoria | `dim_produto[categoria]` + `[Faturamento]` |
| Margem categoria | categoria + `[Margem %]` |
| Top produtos | produto + `[Faturamento]` |
| Dispersão X | `[Faturamento]` |
| Dispersão Y | `[Margem %]` |
| Dispersão tamanho | `[Quantidade Vendida]` |

## Estoque

| Visual | Campo / Medida |
|---|---|
| Card valor | `[Valor em Estoque]` |
| Card estoque | `[Estoque Atual]` |
| Card abaixo mínimo | `[Produtos Abaixo do Mínimo]` |
| Card acima máximo | `[Produtos Acima do Máximo]` |
| Filial | `dim_filial[filial]` |
| Categoria | `dim_produto[categoria]` |
| Produto | `dim_produto[produto]` |

## Slicers recomendados

### Globais

- `dim_data[data_completa]`
- `dim_filial[filial]`
- `dim_filial[uf]`

### Contextuais

- `dim_produto[categoria]`
- `dim_representante[gerente]`
- `dim_representante[supervisor]`
- `dim_representante[representante]`

## Campos que devem ficar ocultos para o usuário

Ocultar na exibição do relatório:

- todas as colunas `*_key`;
- todos os `id_*_origem`;
- IDs técnicos;
- campos usados exclusivamente para relacionamento.

Manter visíveis apenas dimensões compreensíveis e medidas orientadas ao negócio.
