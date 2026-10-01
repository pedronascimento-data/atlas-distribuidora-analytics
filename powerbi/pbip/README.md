# Power BI Project — PBIP/TMDL/PBIR

Esta pasta contém a versão **source-controlled** do dashboard Atlas.

## O que existe aqui

```text
pbip/
├── AtlasDistribuidoraAnalytics.pbip
├── AtlasDistribuidoraAnalytics.Report/
│   ├── definition.pbir
│   └── definition/
│       ├── report.json
│       ├── version.json
│       └── pages/
│           ├── pages.json
│           ├── Visão Executiva
│           ├── Performance Comercial
│           ├── Clientes
│           ├── Produtos e Categorias
│           └── Estoque
└── AtlasDistribuidoraAnalytics.SemanticModel/
    ├── definition.pbism
    └── definition/
        ├── database.tmdl
        ├── model.tmdl
        ├── expressions.tmdl
        ├── relationships.tmdl
        └── tables/
```

## Modelo já implementado

O TMDL contém:

- `dim_data`;
- `dim_cliente`;
- `dim_produto`;
- `dim_representante`;
- `dim_filial`;
- `fato_vendas`;
- `fato_metas`;
- `fato_estoque`;
- `_Medidas`.

Também estão declarados:

- relacionamentos estrela;
- hierarquia de calendário;
- hierarquia comercial;
- hierarquia de produtos;
- hierarquia geográfica;
- medidas DAX;
- pastas de exibição;
- parâmetros de conexão `Server` e `Database`.

## Conexão padrão

```text
Server   = localhost
Database = atlas_dw
```

As tabelas utilizam **Import mode** e Power Query M com `MySQL.Database`.

## Como abrir

1. Garanta que o banco `atlas_dw` esteja criado e carregado.
2. Abra `AtlasDistribuidoraAnalytics.pbip` no Power BI Desktop.
3. Informe as credenciais do MySQL quando solicitado.
4. Caso necessário, altere o parâmetro `Server`.
5. Atualize o modelo.
6. Valide o faturamento contra `sql/06_validacoes_pipeline.sql`.
7. Importe `../tema-atlas.json`.
8. Monte os visuais usando `../campos-visuais.md`.

## Páginas

As cinco páginas 1280 × 720 já existem no PBIR:

1. Visão Executiva
2. Performance Comercial
3. Clientes
4. Produtos e Categorias
5. Estoque

Elas estão intencionalmente sem visuais nesta versão inicial. Os arquivos de visual devem ser gerados/validados pelo Power BI Desktop para evitar inserir PBIR inválido no repositório.

## Controle de versão

Arquivos locais e cache do Desktop não devem ser commitados:

```text
**/.pbi/localSettings.json
**/.pbi/cache.abf
```

Depois de abrir e salvar o projeto pela primeira vez no Desktop, revise o diff gerado pelo Power BI antes de continuar a montagem visual.


## Implementação do relatório

A página **Visão Executiva** já possui 10 definições `visual.json` versionadas no PBIR:

- 6 cards;
- 1 gráfico de linha;
- 1 gráfico de colunas;
- 2 gráficos de barras.

Consulte [Implementação PBIR — Visão Executiva](../../docs/bi/06-visao-executiva-pbir.md).

**Status:** autoria PBIR concluída; renderização e QA no Power BI Desktop ainda pendentes.
