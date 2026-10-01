# QA Automatizado — Power BI Project

> **Escopo:** validação estática de PBIP, PBIR e TMDL antes da abertura no Power BI Desktop.

## Por que existe

PBIR utiliza arquivos JSON com schemas públicos. Alterações externas são suportadas, mas propriedades inválidas ou campos obrigatórios ausentes podem impedir a abertura do relatório no Power BI Desktop.

Por isso, o Atlas executa uma camada de QA antes da validação visual.

## Validador

Arquivo:

`python/validate_powerbi_project.py`

Execução estrutural, sem internet:

```bash
python python/validate_powerbi_project.py
```

Execução completa com validação dos schemas públicos:

```bash
pip install -r requirements-dev.txt
python python/validate_powerbi_project.py --schema --strict-schema
```

## O que é verificado

### PBIP/PBIR

- existe exatamente um `.pbip`;
- o projeto aponta para o diretório de relatório correto;
- `definition.pbir` aponta para o modelo semântico esperado;
- PBIR enhanced e PBIR-Legacy não coexistem;
- JSONs são sintaticamente válidos;
- arquivos com `$schema` podem ser confrontados com os schemas públicos.

### Páginas

- exatamente cinco páginas;
- `pageOrder` coincide com as pastas existentes;
- `activePageName` é válido;
- ID de cada `page.json` coincide com a pasta;
- canvas esperado de 1280 × 720.

### Visuais

- exatamente 42 visuais na versão atual;
- ID do `visual.json` coincide com a pasta;
- IDs não se repetem;
- medidas usadas por visuais existem no TMDL;
- colunas usadas por visuais existem nas tabelas TMDL.

### Modelo semântico

- tabelas referenciadas por `model.tmdl` coincidem com os arquivos em `tables/`;
- endpoints dos relacionamentos existem;
- tabela `_Medidas` existe;
- medidas TMDL são descobertas e usadas para checagem de referência.

## GitHub Actions

Workflow:

`.github/workflows/powerbi-qa.yml`

O QA é executado em pushes e pull requests que alterem:

- `powerbi/**`;
- o validador;
- dependências de QA;
- o próprio workflow.

## O que este QA não substitui

Mesmo passando no CI, ainda é necessário abrir o projeto no Power BI Desktop para verificar:

- processamento do modelo Import;
- autenticação MySQL;
- compatibilidade final do TMDL;
- renderização dos tipos de visual;
- papéis semânticos dos campos;
- interações;
- filtros Top N;
- formatação;
- experiência visual;
- reconciliação final dos KPIs.

## Fluxo de aceitação

```text
commit
  ↓
QA estático
  ↓
schemas PBIR
  ↓
referências TMDL
  ↓
Power BI Desktop
  ↓
refresh
  ↓
reconciliação SQL
  ↓
QA visual
  ↓
screenshots
```

A etapa de Desktop é o último gate técnico antes de o dashboard ser apresentado como concluído.
