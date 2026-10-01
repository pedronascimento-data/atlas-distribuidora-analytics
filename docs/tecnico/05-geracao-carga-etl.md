# Documento Técnico 05 — Geração, Carga e ETL

> **Projeto:** Atlas Distribuidora Analytics  
> **Etapa:** Pipeline de dados  
> **Status:** Implementado

## 1. Objetivo

Tornar o projeto reproduzível do início ao fim:

1. criar o banco operacional;
2. gerar dados sintéticos;
3. validar a massa gerada;
4. carregar os dados no MySQL;
5. criar a camada dimensional;
6. executar o ETL;
7. reconciliar origem e destino.

## 2. Preparação do ambiente

```bash
python -m venv .venv
pip install -r requirements.txt
```

## 3. Criar o banco operacional

Execute no MySQL:

```text
sql/01_schema_operacional.sql
```

## 4. Gerar os dados sintéticos

Desenvolvimento:

```bash
python python/generate_mock_data.py --scale small
```

Portfólio:

```bash
python python/generate_mock_data.py --scale portfolio
```

Volume ampliado:

```bash
python python/generate_mock_data.py --scale full
```

Os dados são gravados em `data/generated/`.

## 5. Validar os CSVs

Antes de inserir qualquer dado no banco:

```bash
python python/validate_generated_data.py
```

O script verifica, entre outros pontos:

- referências entre tabelas;
- unicidade de estoque por filial/produto;
- unicidade de meta por representante/mês;
- preços, custos e quantidades;
- datas de faturamento;
- reconciliação entre desconto do pedido e desconto dos itens.

Uma falha encerra o processo com código de erro diferente de zero.

## 6. Carregar o banco operacional

Configure as variáveis de ambiente.

### Windows PowerShell

```powershell
$env:MYSQL_HOST="localhost"
$env:MYSQL_PORT="3306"
$env:MYSQL_USER="root"
$env:MYSQL_PASSWORD="sua_senha"
$env:MYSQL_DATABASE="atlas_distribuidora"
```

Execute:

```bash
python python/load_operational.py --truncate
```

A opção `--truncate` permite repetir a carga do zero.

## 7. Criar as views analíticas

```text
sql/02_views_analiticas.sql
```

As views centralizam regras recorrentes como faturamento, margem, metas, estoque crítico e inatividade.

## 8. Criar o Data Warehouse

```text
sql/04_schema_dimensional.sql
```

O banco `atlas_dw` é separado da camada operacional e contém dimensões e fatos em esquema estrela.

## 9. Executar o ETL

```text
sql/05_etl_dimensional.sql
```

O ETL realiza:

- carga da dimensão calendário;
- cliente com geografia;
- produto com categoria, marca e fornecedor;
- hierarquia representante → supervisor → gerente;
- filial com geografia;
- fato de vendas;
- fato de metas;
- snapshot de estoque.

## 10. Validar origem x destino

```text
sql/06_validacoes_pipeline.sql
```

As consultas verificam:

- quantidade de linhas de vendas;
- reconciliação do faturamento;
- reconciliação das metas;
- duplicidades em dimensões;
- integridade das chaves dimensionais;
- métricas inválidas.

## 11. Ordem completa

```text
01_schema_operacional.sql
        ↓
generate_mock_data.py
        ↓
validate_generated_data.py
        ↓
load_operational.py
        ↓
02_views_analiticas.sql
        ↓
04_schema_dimensional.sql
        ↓
05_etl_dimensional.sql
        ↓
06_validacoes_pipeline.sql
        ↓
Power BI
```

## 12. Decisões de engenharia

### Dados reproduzíveis

O repositório armazena o código gerador, não milhares de linhas de dados derivados.

### Semente fixa

`SEED = 42` permite reproduzir a mesma massa usando os mesmos parâmetros.

### Escala configurável

O mesmo código atende teste rápido, demonstração e um cenário de maior volume.

### Separação OLTP x DW

`atlas_distribuidora` representa a operação; `atlas_dw` representa a camada analítica.

### Qualidade antes e depois da carga

Há validação antes da persistência e reconciliação depois do ETL.

### Credenciais fora do código

Informações de conexão são lidas de variáveis de ambiente e não são versionadas.

## 13. Próxima etapa

A base passa a estar pronta para:

- análise exploratória em Python/Pandas;
- definição das medidas DAX;
- construção do dashboard no Power BI;
- documentação dos insights executivos.
