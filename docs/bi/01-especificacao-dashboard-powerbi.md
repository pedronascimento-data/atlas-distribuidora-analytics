# Especificação do Dashboard Power BI

> **Projeto:** Atlas Distribuidora Analytics  
> **Camada:** Business Intelligence  
> **Status:** Especificação inicial  
> **Fonte:** `atlas_dw`

## 1. Objetivo

Construir um dashboard comercial e operacional que permita acompanhar resultado, metas, clientes, produtos e estoque sem expor a complexidade do banco transacional.

## 2. Modelo semântico

### Relacionamentos de vendas

```text
dim_data ───────────────┐
dim_cliente ────────────┤
dim_produto ────────────┤
dim_representante ──────┼── fato_vendas
dim_filial ─────────────┘
```

### Relacionamentos de metas

```text
dim_data ───────────────┐
                        ├── fato_metas
dim_representante ──────┘
```

### Relacionamentos de estoque

```text
dim_data ───────────────┐
dim_produto ────────────┼── fato_estoque
dim_filial ─────────────┘
```

Configuração recomendada:

- cardinalidade 1:N da dimensão para a fato;
- direção de filtro simples;
- fatos sem relacionamento direto entre si;
- `dim_data[data_completa]` marcada como tabela de datas;
- chaves técnicas ocultas na visualização de relatório.

## 3. Página 01 — Visão Executiva

### Objetivo

Responder rapidamente: **como está o negócio e o resultado está evoluindo?**

### KPIs

- Faturamento
- Margem Bruta
- Margem %
- Ticket Médio
- Atingimento da Meta %
- Crescimento MoM %

### Visuais

- linha de faturamento por mês;
- barras de faturamento por categoria;
- mapa ou barras por UF;
- faturamento x meta;
- Top 5 representantes;
- cartões de KPI.

### Filtros

- período;
- filial;
- estado;
- categoria.

## 4. Página 02 — Performance Comercial

### Objetivo

Avaliar representantes, supervisores e metas.

### Indicadores

- faturamento;
- meta;
- atingimento;
- gap para meta;
- ranking de representantes;
- ticket médio;
- clientes compradores.

### Visuais

- ranking de representantes;
- matriz gerente → supervisor → representante;
- gráfico de faturamento x meta;
- evolução mensal por equipe;
- distribuição de performance.

### Drill-down

```text
Gerente
  ↓
Supervisor
  ↓
Representante
```

## 5. Página 03 — Clientes

### Objetivo

Identificar concentração de receita e comportamento da carteira.

### Indicadores

- clientes compradores;
- faturamento por cliente;
- ticket médio;
- participação de clientes no faturamento.

### Visuais

- Top clientes;
- faturamento por UF/cidade;
- curva acumulada de participação;
- matriz cliente x faturamento x pedidos;
- evolução da carteira compradora.

Uma evolução futura poderá incorporar classificação RFM e inatividade dinâmica.

## 6. Página 04 — Produtos e Categorias

### Objetivo

Analisar mix, receita e rentabilidade.

### Indicadores

- faturamento;
- quantidade vendida;
- margem;
- margem %;
- preço médio.

### Visuais

- faturamento por categoria;
- margem % por categoria;
- Top produtos;
- matriz categoria → produto;
- dispersão faturamento x margem.

## 7. Página 05 — Estoque

### Objetivo

Relacionar disponibilidade de produto e risco operacional.

### Indicadores

- valor em estoque;
- estoque atual;
- produtos abaixo do mínimo;
- produtos acima do máximo.

### Visuais

- produtos críticos;
- estoque por filial;
- valor de estoque por categoria;
- matriz produto x filial;
- distribuição por faixa de estoque.

## 8. Medidas DAX

As medidas iniciais estão versionadas em:

`powerbi/medidas.dax`

Grupos:

- vendas;
- tempo;
- metas;
- comercial;
- estoque;
- participação.

## 9. Padrões de construção

- medidas explícitas para KPIs;
- nomes em português orientados ao negócio;
- evitar excesso de colunas calculadas;
- usar a tabela calendário para inteligência temporal;
- conferir qualquer KPI agregado contra SQL antes de publicar;
- manter filtros consistentes entre páginas;
- usar tooltips apenas quando acrescentarem contexto.

## 10. Critérios de validação

Antes de considerar o dashboard concluído:

1. faturamento Power BI = faturamento reconciliado no DW;
2. quantidade de pedidos = `DISTINCTCOUNT(numero_pedido)`;
3. margem = faturamento líquido - custo;
4. meta respeita período e hierarquia comercial;
5. filtros de filial, produto e representante propagam corretamente;
6. relações entre tabelas não criam ambiguidade;
7. totais da página executiva possuem rastreabilidade SQL.

## 11. Entregáveis finais previstos

- arquivo `.pbix`;
- screenshots das páginas;
- imagem do modelo semântico;
- catálogo das medidas DAX;
- README com principais insights;
- comparação entre resultados SQL e Power BI.
