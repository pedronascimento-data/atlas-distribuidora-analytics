# Análise Exploratória de Dados — Atlas Distribuidora

> **Projeto:** Atlas Distribuidora Analytics  
> **Ferramentas:** Python, Pandas e Matplotlib  
> **Status:** Implementada de forma reproduzível

## 1. Objetivo

A EDA conecta a camada de engenharia à camada de decisão.

O foco não é apenas produzir gráficos, mas responder perguntas relevantes para a gestão comercial e transformar os resultados em requisitos objetivos para o dashboard.

## 2. Arquivos

### Script automatizado

`python/eda_analysis.py`

Executa a análise completa e gera:

- tabelas agregadas em CSV;
- gráficos em PNG;
- resumo automático em Markdown.

### Notebook

`notebooks/01_eda_atlas.ipynb`

Apresenta o raciocínio da análise em formato sequencial, adequado para leitura no GitHub.

## 3. Perguntas analisadas

### Resultado geral

- Qual é o faturamento?
- Qual é a margem bruta?
- Qual é a margem percentual?
- Quantos pedidos foram faturados?
- Qual é o ticket médio?
- Quantos clientes efetivamente compraram?

### Evolução temporal

- Como o faturamento evolui mensalmente?
- Há crescimento ou retração mês contra mês?
- A margem acompanha a receita?
- Existem períodos de maior concentração?

### Clientes

- Quais clientes geram mais receita?
- Qual é a participação dos maiores clientes?
- Qual é o nível de concentração da carteira?
- Quais clientes apresentam maior ticket médio?

### Produtos e categorias

- Quais categorias lideram em receita?
- Quais categorias possuem melhor margem?
- Quais produtos combinam volume e rentabilidade?
- Quais produtos possuem baixa relevância comercial?

### Equipe comercial

- Quais representantes lideram o faturamento?
- Qual é o ranking comercial?
- Como faturamento e meta se relacionam?
- Quem está abaixo, próximo ou acima da meta?

### Estoque

- Quantas posições produto/filial estão abaixo do mínimo?
- Qual o valor financeiro do estoque?
- Há produtos acima do estoque máximo?
- Há risco de ruptura em itens comercialmente relevantes?

## 4. Métricas calculadas

### Faturamento

```text
(quantidade × preço unitário) - desconto do item
```

### Margem bruta

```text
faturamento - (quantidade × custo unitário)
```

### Margem %

```text
margem bruta / faturamento
```

### Ticket médio

```text
faturamento / quantidade distinta de pedidos
```

### Crescimento MoM

```text
(faturamento atual - faturamento mês anterior)
------------------------------------------------
            faturamento mês anterior
```

### Participação de cliente/categoria

```text
faturamento do segmento / faturamento total
```

### Atingimento de meta

```text
faturamento / meta
```

## 5. Saída da análise

Por padrão:

```text
reports/eda/
├── resumo_eda.md
├── figures/
│   ├── faturamento_mensal.png
│   ├── faturamento_categoria.png
│   ├── top_produtos.png
│   └── top_clientes.png
└── tables/
    ├── kpis_executivos.csv
    ├── evolucao_mensal.csv
    ├── performance_categorias.csv
    ├── top_20_produtos.csv
    ├── top_50_clientes.csv
    ├── performance_representantes.csv
    ├── atingimento_metas.csv
    └── resumo_estoque.csv
```

## 6. Execução

Após gerar os dados:

```bash
python python/eda_analysis.py
```

Para caminhos personalizados:

```bash
python python/eda_analysis.py \
  --data-dir data/generated \
  --output-dir reports/eda
```

## 7. Relação com o Power BI

| Descoberta/Análise | Página do dashboard |
|---|---|
| Evolução de faturamento e margem | Visão Executiva |
| Faturamento x meta e ranking | Performance Comercial |
| Concentração e Top clientes | Clientes |
| Receita, volume e margem por produto | Produtos e Categorias |
| Estoque mínimo/máximo | Estoque |

## 8. Critério de qualidade

Os números da EDA devem ser reconciliáveis com:

1. as consultas SQL do banco operacional;
2. as fatos do Data Warehouse;
3. as medidas DAX do Power BI.

A mesma definição de negócio deve gerar o mesmo resultado em todas as camadas.

## 9. Próxima evolução analítica

Após a primeira versão do dashboard, o projeto poderá incorporar:

- análise Pareto 80/20;
- segmentação RFM;
- curva ABC de produtos;
- detecção de clientes em risco de inatividade;
- relação entre giro e estoque;
- análise de margem por faixa de produto.
