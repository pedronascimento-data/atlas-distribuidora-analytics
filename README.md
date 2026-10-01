# Atlas Distribuidora Analytics

Projeto de portfólio que simula a construção de uma solução **end-to-end de Dados e Business Intelligence** para uma distribuidora de materiais de construção.

O projeto cobre o fluxo completo:

`Negócio → Requisitos → Modelagem Relacional → MySQL → SQL Analítico → Modelo Dimensional → Power BI`

## Problema de negócio

Com o crescimento da operação, dados de clientes, vendas, produtos, representantes, filiais e estoque passam a ficar distribuídos entre planilhas e sistemas operacionais.

A solução proposta busca centralizar essas informações para responder perguntas como:

- Qual é o faturamento consolidado?
- Quais representantes estão atingindo as metas?
- Quais clientes concentram maior parte da receita?
- Quais categorias e produtos apresentam maior ou menor giro?
- Quais itens estão abaixo do estoque mínimo?
- Como o desempenho varia por filial, estado e período?

## Stack

- MySQL 8+
- SQL
- Power BI
- Power Query
- DAX
- Python / Pandas *(próxima etapa)*
- Git e GitHub
- Markdown

## O que já está implementado

### Negócio

- visão do projeto;
- requisitos de negócio;
- regras de negócio;
- manual da empresa fictícia.

### Engenharia e modelagem

- arquitetura da solução;
- modelo relacional normalizado;
- dicionário de dados;
- esquema dimensional em estrela;
- definição de granularidade das tabelas fato.

### SQL

- DDL completo do banco operacional;
- PKs, FKs, restrições e índices;
- views analíticas;
- faturamento e margem;
- estoque crítico;
- metas;
- inatividade de clientes;
- consultas com JOINs, CTEs e window functions.

## Arquitetura

```text
MySQL operacional
       ↓
SQL / Python
       ↓
Transformação e validação
       ↓
Modelo dimensional
       ↓
Power BI
       ↓
KPIs e dashboards
```

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
| [Arquitetura da Solução](docs/tecnico/01-arquitetura-da-solucao.md) | Camadas e fluxo dos dados |
| [Modelagem Relacional](docs/tecnico/02-modelagem-relacional.md) | Entidades, cardinalidades e decisões |
| [Dicionário de Dados](docs/tecnico/03-dicionario-de-dados.md) | Campos e regras do banco operacional |
| [Modelo Dimensional](docs/tecnico/04-modelo-dimensional.md) | Dimensões, fatos, grãos e KPIs |

## Scripts SQL

| Arquivo | Objetivo |
|---|---|
| [01_schema_operacional.sql](sql/01_schema_operacional.sql) | Criação física do banco MySQL |
| [02_views_analiticas.sql](sql/02_views_analiticas.sql) | Views reutilizáveis para análises |
| [03_consultas_analiticas.sql](sql/03_consultas_analiticas.sql) | KPIs, CTEs, rankings e window functions |

## Exemplos de análises SQL

O projeto já contém consultas para:

- faturamento, ticket médio e margem;
- crescimento mensal com `LAG()`;
- ranking de representantes com `RANK()`;
- participação no faturamento com funções de janela;
- Top 10 clientes;
- performance por categoria;
- produtos de baixo giro;
- clientes sem compra há mais de 90 dias;
- atingimento de metas;
- estoque abaixo do mínimo.

## Modelo dimensional

### Dimensões

`dim_data` • `dim_cliente` • `dim_produto` • `dim_representante` • `dim_filial`

### Fatos

`fato_vendas` • `fato_metas` • `fato_estoque`

O grão principal de vendas é **uma linha por item de pedido faturado**.

## Roadmap

- [x] Visão do projeto
- [x] Requisitos e regras de negócio
- [x] Arquitetura
- [x] Modelagem relacional
- [x] Dicionário de dados
- [x] Schema MySQL
- [x] Views analíticas
- [x] Consultas SQL avançadas
- [x] Modelo dimensional conceitual
- [ ] Massa de dados fictícios
- [ ] ETL / carga dimensional
- [ ] Análise exploratória em Python
- [ ] Dashboard Power BI
- [ ] Medidas DAX documentadas
- [ ] Validação e apresentação final

## Competências demonstradas

- levantamento e tradução de requisitos;
- modelagem de dados;
- SQL e MySQL;
- JOINs, CTEs e window functions;
- regras de negócio;
- modelagem dimensional;
- pensamento orientado a KPIs;
- documentação funcional e técnica;
- planejamento de solução de BI.

---

Projeto educacional desenvolvido por **Pedro Nascimento** como estudo de caso de Dados e Business Intelligence.
