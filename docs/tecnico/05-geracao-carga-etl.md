# Documento Técnico 05 — Geração, Carga e ETL

> **Projeto:** Atlas Distribuidora Analytics  
> **Etapa:** Pipeline de dados  
> **Status:** Implementado

## 1. Objetivo

Tornar o projeto reproduzível do início ao fim:

1. criar o banco operacional;
2. gerar dados sintéticos;
3. carregar os dados no MySQL;
4. criar a camada dimensional;
5. executar o ETL;
6. reconciliar os resultados.

## 2. Preparação do ambiente

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente e instale as dependências:

```bash
pip install -r requirements.txt
```

## 3. Criar o banco operacional

Execute no MySQL:

```text
sql/01_schema_operacional.sql
sql/02_views_analiticas.sql
```

## 4. Gerar dados sintéticos

Para desenvolvimento:

```bash
python python/generate_mock_data.py --scale small
```

Para a demonstração principal do portfólio:

```bash
python python/generate_mock_data.py --scale portfolio
```

Para aproximar o volume descrito no manual da empresa:

```bash
python python/generate_mock_data.py --scale full
```

Os dados são gravados em `data/generated/`.

## 5. Carregar o banco operacional

Configure as variáveis de ambiente de acesso ao MySQL.

### Windows PowerShell

```powershell
$env:MYSQL_HOST="localhost"
$env:MYSQL_PORT="3306"
$env:MYSQL_USER="root"
$env:MYSQL_PASSWORD="sua_senha"
$env:MYSQL_DATABASE="atlas_distribuidora"
```

Depois execute:

```bash
python python/load_operational.py --truncate
```

A opção `--truncate` limpa as tabelas antes da nova carga.

## 6. Criar o Data Warehouse

Execute:

```text
sql/04_schema_dimensional.sql
```

Isso cria o banco `atlas_dw` com dimensões e fatos em esquema estrela.

## 7. Executar o ETL

Execute:

```text
sql/05_etl_dimensional.sql
```

A carga realiza:

- criação da dimensão calendário;
- desnormalização dos atributos de clientes;
- desnormalização de produto/categoria/marca/fornecedor;
- hierarquia representante → supervisor → gerente;
- filial com geografia;
- carga da fato de vendas;
- carga de metas;
- snapshot de estoque.

## 8. Validar o pipeline

Execute:

```text
sql/06_validacoes_pipeline.sql
```

As validações verificam:

- igualdade de contagem entre origem e destino;
- reconciliação do faturamento;
- reconciliação das metas;
- duplicidades em dimensões;
- integridade dimensional;
- quantidades, custos e vendas inválidas.

## 9. Ordem completa

```text
01_schema_operacional.sql
        ↓
generate_mock_data.py
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

## 10. Decisões de engenharia

### CSVs fora do Git

Os datasets são reconstruíveis e podem ser grandes. O repositório versiona o código que os produz, não a saída.

### Semente fixa

A geração utiliza uma semente determinística para tornar testes e comparações reproduzíveis.

### Separação OLTP e DW

Os bancos `atlas_distribuidora` e `atlas_dw` possuem responsabilidades diferentes e não são tratados como um único modelo.

### Reconciliação antes do dashboard

O Power BI só deve consumir a camada analítica após as validações de integridade e faturamento.

## 11. Próxima etapa

Com a base pronta, o próximo estágio do projeto é:

- análise exploratória em Python/Pandas;
- definição das medidas DAX;
- construção do dashboard no Power BI;
- documentação dos insights.
