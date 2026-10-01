# Power BI como código — PBIP, TMDL e PBIR

## Objetivo

Além do arquivo final do dashboard, o Atlas mantém a definição do Power BI em formatos de texto versionáveis.

Isso permite demonstrar no GitHub não apenas a aparência do relatório, mas também:

- tabelas do modelo;
- colunas e tipos;
- relacionamentos;
- medidas DAX;
- hierarquias;
- parâmetros de fonte;
- páginas do relatório;
- futuras definições de visuais.

## Estrutura adotada

`PBIP` funciona como o ponto de entrada do projeto.

O modelo semântico utiliza **TMDL**, enquanto a definição do relatório utiliza **PBIR**.

```text
.pbip
  ↓
.Report (PBIR)
  ↘
.SemanticModel (TMDL)
```

## Benefício para portfólio

Um `.pbix` é um artefato binário difícil de revisar no GitHub.

Com PBIP:

- mudanças no DAX aparecem em diff;
- novas tabelas aparecem como arquivos;
- relacionamentos ficam explícitos;
- páginas podem ser versionadas separadamente;
- o recrutador técnico consegue avaliar a organização do modelo sem abrir o Power BI.

## Limitação atual

O PBIP continua dependendo do Power BI Desktop para:

- autenticar no MySQL;
- processar o modelo Import;
- validar completamente o TMDL/PBIR;
- gerar e testar os arquivos de visuais;
- produzir o `.pbix`, se desejado.

Por isso, o scaffold versionado não substitui a etapa final de validação no Desktop.

## Convenção do Atlas

Código fonte:

`powerbi/pbip/`

Tema:

`powerbi/tema-atlas.json`

Catálogo de medidas legível:

`powerbi/medidas.dax`

Mapa de construção:

`powerbi/campos-visuais.md`

QA:

`docs/bi/03-checklist-validacao-dashboard.md`

## Fluxo recomendado

```text
GitHub
  ↓
abrir .pbip
  ↓
autenticar MySQL
  ↓
refresh
  ↓
reconciliar KPIs
  ↓
montar visuais
  ↓
salvar PBIP
  ↓
revisar git diff
  ↓
capturar screenshots
```
