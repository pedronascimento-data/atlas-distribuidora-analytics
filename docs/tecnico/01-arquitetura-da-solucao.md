# Documento Técnico 01 — Arquitetura da Solução

> **Projeto:** Atlas Distribuidora Analytics  
> **Camada:** Arquitetura de Dados e BI  
> **Status:** Versão inicial implementada  
> **Autor:** Pedro Nascimento  
> **Atualização:** Outubro de 2026

## 1. Objetivo

Definir uma arquitetura simples, reproduzível e compatível com um projeto de portfólio que demonstre o ciclo completo de uma solução de dados: origem transacional, transformação, camada analítica e consumo em BI.

## 2. Visão geral

```text
┌──────────────────────────────┐
│  Camada Operacional (OLTP)   │
│          MySQL               │
│                              │
│ clientes • produtos • pedidos│
│ estoque • metas • equipe     │
└──────────────┬───────────────┘
               │
               │ SQL / Python
               ▼
┌──────────────────────────────┐
│ Preparação e Transformação   │
│                              │
│ limpeza • regras • joins     │
│ validações • enriquecimento  │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Camada Analítica             │
│ Modelo Dimensional           │
│                              │
│ dimensões + tabelas fato     │
└──────────────┬───────────────┘
               │
               │ Power Query
               ▼
┌──────────────────────────────┐
│ Power BI                     │
│                              │
│ KPIs • análises • dashboards │
└──────────────────────────────┘
```

## 3. Camada operacional

O banco operacional representa o funcionamento da distribuidora em formato relacional normalizado.

Principais domínios:

- estrutura geográfica;
- filiais;
- estrutura comercial;
- clientes;
- fornecedores;
- categorias, marcas e produtos;
- pedidos e itens;
- estoque por filial;
- metas mensais.

O objetivo dessa camada é preservar integridade e reduzir redundância.

## 4. Transformação

A camada de transformação será responsável por preparar os dados operacionais para análise.

Atividades previstas:

1. padronização de tipos;
2. tratamento de valores nulos;
3. aplicação das regras de negócio;
4. cálculo de valores derivados;
5. criação de chaves analíticas;
6. validação de totais;
7. montagem das dimensões e fatos.

SQL será utilizado para consultas e transformações próximas ao banco. Python/Pandas será usado posteriormente para análises exploratórias e rotinas complementares.

## 5. Camada analítica

O modelo dimensional adotará **esquema estrela**, favorecendo consultas e uso no Power BI.

### Dimensões principais

- `dim_data`
- `dim_cliente`
- `dim_produto`
- `dim_representante`
- `dim_filial`

### Fatos principais

- `fato_vendas`
- `fato_metas`
- `fato_estoque`

A granularidade é definida individualmente para cada fato no documento de modelo dimensional.

## 6. Consumo no Power BI

O Power BI será a camada de apresentação.

Responsabilidades:

- relacionamentos do modelo semântico;
- medidas DAX;
- KPIs;
- filtros e segmentações;
- dashboards executivos e operacionais.

Exemplos de indicadores:

- faturamento;
- margem;
- ticket médio;
- quantidade de pedidos;
- atingimento de meta;
- clientes ativos e inativos;
- participação por categoria;
- produtos de baixo giro;
- estoque abaixo do mínimo.

## 7. Princípios adotados

### Separação entre operação e análise

O modelo operacional não será usado como se fosse um modelo dimensional. Cada estrutura atende a uma finalidade distinta.

### Regras de negócio documentadas

Indicadores devem possuir definição rastreável aos documentos de negócio.

### Reprodutibilidade

Scripts SQL, documentação e futuras rotinas Python devem permitir reconstruir o ambiente.

### Dados fictícios

Todo dado utilizado no projeto terá finalidade educacional e não representará clientes, colaboradores ou resultados reais.

## 8. Fluxo de atualização previsto

```text
Banco operacional
      ↓
Extração
      ↓
Validação
      ↓
Transformação
      ↓
Modelo dimensional
      ↓
Power BI
      ↓
Indicadores
```

## 9. Evoluções futuras

- geração automatizada de massa de dados com Python;
- processo ETL reproduzível;
- testes de qualidade de dados;
- incremental refresh no Power BI;
- documentação de medidas DAX;
- publicação de screenshots e análise executiva.
