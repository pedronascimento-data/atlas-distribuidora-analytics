# Atlas Distribuidora Analytics

Projeto de portfólio que simula a construção de uma solução **end-to-end de Dados e Business Intelligence** para uma distribuidora de materiais de construção.

O projeto cobre o fluxo:

`Negócio → Requisitos → Dados Sintéticos → MySQL OLTP → SQL → ETL → Data Warehouse → Power BI`

## Problema de negócio

Com o crescimento da operação, dados de clientes, vendas, produtos, representantes, filiais e estoque passam a ficar distribuídos entre planilhas e sistemas operacionais.

A solução proposta centraliza essas informações para responder perguntas como:

- Qual é o faturamento consolidado?
- Quais representantes estão atingindo as metas?
- Quais clientes concentram maior parte da receita?
- Quais categorias e produtos apresentam maior ou menor giro?
- Quais itens estão abaixo do estoque mínimo?
- Como o desempenho varia por filial, estado e período?

## Stack

- Python
- Pandas e NumPy
- MySQL 8+
- SQL
- Modelagem relacional e dimensional
- Power BI / Power Query / DAX *(dashboard em desenvolvimento)*
- Git e GitHub
- Markdown

## Pipeline implementado

```text
Regras de negócio
       ↓
Python — geração sintética
       ↓
Validação dos CSVs
       ↓
MySQL — camada operacional
       ↓
SQL / Views analíticas
       ↓
ETL
       ↓
MySQL — Data Warehouse
       ↓
Reconciliação e testes
       ↓
Power BI
```

Os dados são reproduzíveis e podem ser gerados em três escalas:

| Escala | Clientes | Produtos | Pedidos |
|---|---:|---:|---:|
| `small` | 250 | 120 | 2.000 |
| `portfolio` | 1.500 | 500 | 18.000 |
| `full` | 12.000 | 4.500 | 100.000 |

## O que já está implementado

### Negócio

- visão e contexto do projeto;
- requisitos;
- regras de negócio;
- estrutura da empresa fictícia.

### Python e qualidade de dados

- geração parametrizável de massa sintética;
- semente fixa para reprodutibilidade;
- hierarquia comercial, clientes, produtos, vendas, metas e estoque;
- validações de integridade referencial;
- verificação de unicidade;
- reconciliação de descontos;
- preparação dos CSVs para carga.

### Engenharia e modelagem

- arquitetura da solução;
- modelo relacional normalizado;
- schema MySQL operacional;
- dicionário de dados;
- modelo dimensional estrela;
- Data Warehouse físico;
- ETL do OLTP para o DW;
- validações de reconciliação entre origem e destino.

### SQL analítico

- JOINs;
- CTEs;
- `LAG()`;
- `RANK()`;
- `ROW_NUMBER()`;
- agregações;
- views reutilizáveis;
- KPIs e regras de negócio.

## Documentação de negócio

| Documento | Conteúdo |
|---|---|
| [01 — Visão do Projeto](docs/negocio/01-visao-do-projeto.md) | Contexto, problema, objetivos e escopo |
| [02 — Requisitos de Negócio](docs/negocio/02-requisitos-de-negocio.md) | Requisitos funcionais e indicadores |
| [03 — Regras de Negócio](docs/negocio/03-regras-de-negocio.md) | Regras que orientam dados e KPIs |
| [04 — Manual da Empresa](docs/negocio/04-manual-da-empresa.md) | Estrutura e funcionamento da empresa fictícia |

## Documentação técnica

| Documento | Conteúdo |
|---|---|
| [Arquitetura da Solução](docs/tecnico/01-arquitetura-da-solucao.md) | Camadas e fluxo de dados |
| [Modelagem Relacional](docs/tecnico/02-modelagem-relacional.md) | Entidades, cardinalidades e decisões |
| [Dicionário de Dados](docs/tecnico/03-dicionario-de-dados.md) | Campos e regras do banco operacional |
| [Modelo Dimensional](docs/tecnico/04-modelo-dimensional.md) | Dimensões, fatos, grãos e KPIs |
| [Geração, Carga e ETL](docs/tecnico/05-geracao-carga-etl.md) | Execução reproduzível do pipeline |

## Python

| Arquivo | Objetivo |
|---|---|
| [generate_mock_data.py](python/generate_mock_data.py) | Gerar a massa sintética |
| [validate_generated_data.py](python/validate_generated_data.py) | Validar integridade antes da carga |
| [load_operational.py](python/load_operational.py) | Carregar os CSVs no MySQL |

## SQL

| Arquivo | Objetivo |
|---|---|
| [01_schema_operacional.sql](sql/01_schema_operacional.sql) | Criar o banco operacional |
| [02_views_analiticas.sql](sql/02_views_analiticas.sql) | Criar views de análise |
| [03_consultas_analiticas.sql](sql/03_consultas_analiticas.sql) | KPIs, CTEs e window functions |
| [04_schema_dimensional.sql](sql/04_schema_dimensional.sql) | Criar o Data Warehouse |
| [05_etl_dimensional.sql](sql/05_etl_dimensional.sql) | Carregar dimensões e fatos |
| [06_validacoes_pipeline.sql](sql/06_validacoes_pipeline.sql) | Reconciliar origem e DW |

## Power BI

A camada de BI já possui especificação funcional e medidas iniciais versionadas:

- [Especificação do Dashboard](docs/bi/01-especificacao-dashboard-powerbi.md)
- [Medidas DAX](powerbi/medidas.dax)
- [Pasta Power BI](powerbi/README.md)

O dashboard foi planejado em cinco páginas: **Visão Executiva, Performance Comercial, Clientes, Produtos e Categorias, e Estoque**. O arquivo `.pbix` ainda está em desenvolvimento.

## Modelo dimensional

### Dimensões

`dim_data` • `dim_cliente` • `dim_produto` • `dim_representante` • `dim_filial`

### Fatos

`fato_vendas` • `fato_metas` • `fato_estoque`

O grão da fato de vendas é **uma linha por item de pedido faturado**.

## Exemplos de análises

O projeto contém consultas para:

- faturamento, ticket médio e margem;
- crescimento mensal com `LAG()`;
- ranking de representantes com `RANK()`;
- participação no faturamento;
- Top 10 clientes;
- performance por categoria;
- produtos de baixo giro;
- clientes sem compra há mais de 90 dias;
- atingimento de metas;
- estoque abaixo do mínimo.

## Execução resumida

```bash
pip install -r requirements.txt

python python/generate_mock_data.py --scale portfolio
python python/validate_generated_data.py
python python/load_operational.py --truncate
```

Depois, no MySQL:

```text
01_schema_operacional.sql
02_views_analiticas.sql
04_schema_dimensional.sql
05_etl_dimensional.sql
06_validacoes_pipeline.sql
```

> Consulte [Geração, Carga e ETL](docs/tecnico/05-geracao-carga-etl.md) para a ordem detalhada e configuração do ambiente.

## Roadmap

- [x] Visão do projeto
- [x] Requisitos e regras de negócio
- [x] Arquitetura
- [x] Modelagem relacional
- [x] Dicionário de dados
- [x] Schema MySQL
- [x] Views analíticas
- [x] Consultas SQL avançadas
- [x] Geração de dados fictícios com Python
- [x] Validação dos dados gerados
- [x] Modelo dimensional físico
- [x] ETL / carga dimensional
- [x] Validações e reconciliação do pipeline
- [ ] Análise exploratória em Python
- [x] Especificação do dashboard Power BI
- [x] Medidas DAX documentadas
- [ ] Arquivo e páginas do dashboard Power BI
- [ ] Apresentação executiva dos insights

## Competências demonstradas

- levantamento e tradução de requisitos;
- Python aplicado a dados;
- Pandas e NumPy;
- SQL e MySQL;
- modelagem relacional e dimensional;
- ETL;
- JOINs, CTEs e window functions;
- qualidade e reconciliação de dados;
- desenho de KPIs;
- documentação funcional e técnica;
- organização de projeto analítico end-to-end.

---

Projeto educacional desenvolvido por **Pedro Nascimento** como estudo de caso de Dados e Business Intelligence.
