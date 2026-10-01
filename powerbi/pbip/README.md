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

O TMDL contém cinco dimensões, três fatos, tabela de medidas, relacionamentos estrela, hierarquias, parâmetros de conexão e medidas DAX.

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
8. Revise os visuais usando `../campos-visuais.md`.

## Páginas

1. Visão Executiva — **10 visuais PBIR**
2. Performance Comercial — **8 visuais PBIR**
3. Clientes — **7 visuais PBIR**
4. Produtos e Categorias — **9 visuais PBIR**
5. Estoque — **8 visuais PBIR**

## Controle de versão

Não versionar:

```text
**/.pbi/localSettings.json
**/.pbi/cache.abf
```

## Implementação do relatório

### Visão Executiva

[Documentação](../../docs/bi/06-visao-executiva-pbir.md)

### Performance Comercial

[Documentação](../../docs/bi/07-performance-comercial-pbir.md)

### Clientes

- 4 cards;
- 1 ranking de clientes;
- 1 gráfico por UF;
- 1 tabela de carteira.

[Documentação](../../docs/bi/08-clientes-pbir.md)

### Produtos e Categorias

- 5 cards;
- 2 análises por categoria;
- 1 ranking de produtos;
- 1 tabela de mix detalhado.

[Documentação](../../docs/bi/09-produtos-categorias-pbir.md)

### Estoque

- 4 cards;
- 2 análises de valor de estoque;
- 1 análise de posições críticas por filial;
- 1 tabela de diagnóstico produto × filial.

[Documentação](../../docs/bi/10-estoque-pbir.md)

**Status geral:** 42 visuais PBIR versionados nas cinco páginas planejadas. A autoria PBIR está concluída; renderização, QA e refinamento no Power BI Desktop ainda estão pendentes.


## QA automatizado

Validação estrutural local:

```bash
python python/validate_powerbi_project.py
```

Validação completa com os schemas públicos PBIR:

```bash
pip install -r requirements-dev.txt
python python/validate_powerbi_project.py --schema --strict-schema
```

O workflow `.github/workflows/powerbi-qa.yml` executa essa validação automaticamente em alterações da camada Power BI.

[Documentação de QA](../../docs/bi/11-qa-automatizado.md)
