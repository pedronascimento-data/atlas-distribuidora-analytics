# Documento Técnico 03 — Dicionário de Dados

> **Projeto:** Atlas Distribuidora Analytics  
> **Escopo:** Banco operacional  
> **Banco:** MySQL 8+

Este documento resume os principais campos do modelo operacional. O script SQL é a referência física definitiva de tipos, restrições e índices.

## estado

| Campo | Tipo | Regra |
|---|---|---|
| id_estado | INT | PK |
| nome | VARCHAR(60) | obrigatório |
| uf | CHAR(2) | obrigatório e único |

## cidade

| Campo | Tipo | Regra |
|---|---|---|
| id_cidade | INT | PK |
| nome | VARCHAR(100) | obrigatório |
| id_estado | INT | FK → estado |

## filial

| Campo | Tipo | Regra |
|---|---|---|
| id_filial | INT | PK |
| codigo | VARCHAR(10) | único |
| nome | VARCHAR(100) | obrigatório |
| id_cidade | INT | FK → cidade |
| ativa | BOOLEAN | padrão verdadeiro |

## gerente

| Campo | Tipo | Regra |
|---|---|---|
| id_gerente | INT | PK |
| codigo | VARCHAR(20) | único |
| nome | VARCHAR(120) | obrigatório |
| ativo | BOOLEAN | padrão verdadeiro |

## supervisor

| Campo | Tipo | Regra |
|---|---|---|
| id_supervisor | INT | PK |
| codigo | VARCHAR(20) | único |
| nome | VARCHAR(120) | obrigatório |
| id_gerente | INT | FK → gerente |
| ativo | BOOLEAN | padrão verdadeiro |

## representante

| Campo | Tipo | Regra |
|---|---|---|
| id_representante | INT | PK |
| codigo | VARCHAR(20) | único |
| nome | VARCHAR(120) | obrigatório |
| id_supervisor | INT | FK → supervisor |
| ativo | BOOLEAN | padrão verdadeiro |

## cliente

| Campo | Tipo | Regra |
|---|---|---|
| id_cliente | INT | PK |
| codigo | VARCHAR(20) | único |
| razao_social | VARCHAR(150) | obrigatório |
| nome_fantasia | VARCHAR(150) | opcional |
| documento | VARCHAR(18) | único |
| id_cidade | INT | FK → cidade |
| id_representante | INT | FK → representante |
| status | ENUM | ATIVO, INATIVO ou BLOQUEADO |
| data_cadastro | DATE | obrigatório |

> A regra de cliente inativo por mais de 90 dias sem compras deve ser derivada analiticamente. O campo `status` representa o status cadastral/operacional.

## categoria

| Campo | Tipo | Regra |
|---|---|---|
| id_categoria | INT | PK |
| nome | VARCHAR(100) | único |

## marca

| Campo | Tipo | Regra |
|---|---|---|
| id_marca | INT | PK |
| nome | VARCHAR(100) | único |

## fornecedor

| Campo | Tipo | Regra |
|---|---|---|
| id_fornecedor | INT | PK |
| codigo | VARCHAR(20) | único |
| razao_social | VARCHAR(150) | obrigatório |
| nome_fantasia | VARCHAR(150) | opcional |
| documento | VARCHAR(18) | único |
| ativo | BOOLEAN | padrão verdadeiro |

## produto

| Campo | Tipo | Regra |
|---|---|---|
| id_produto | INT | PK |
| sku | VARCHAR(30) | único |
| descricao | VARCHAR(180) | obrigatório |
| id_categoria | INT | FK → categoria |
| id_marca | INT | FK → marca |
| id_fornecedor | INT | FK → fornecedor |
| custo_atual | DECIMAL(12,2) | ≥ 0 |
| preco_atual | DECIMAL(12,2) | ≥ 0 |
| ativo | BOOLEAN | padrão verdadeiro |

## pedido

| Campo | Tipo | Regra |
|---|---|---|
| id_pedido | BIGINT | PK |
| numero_pedido | VARCHAR(30) | único |
| data_pedido | DATETIME | obrigatório |
| data_faturamento | DATETIME | opcional |
| id_cliente | INT | FK → cliente |
| id_representante | INT | FK → representante |
| id_filial | INT | FK → filial |
| status | ENUM | EM_DIGITACAO, APROVADO, FATURADO, CANCELADO, ENTREGUE |
| valor_frete | DECIMAL(12,2) | ≥ 0 |
| valor_desconto | DECIMAL(12,2) | ≥ 0 |

## pedido_item

| Campo | Tipo | Regra |
|---|---|---|
| id_pedido_item | BIGINT | PK |
| id_pedido | BIGINT | FK → pedido |
| id_produto | INT | FK → produto |
| quantidade | DECIMAL(12,3) | > 0 |
| preco_unitario | DECIMAL(12,2) | ≥ 0 |
| custo_unitario | DECIMAL(12,2) | ≥ 0 |
| desconto_item | DECIMAL(12,2) | ≥ 0 |

### Valor bruto do item

```text
quantidade × preco_unitario
```

### Valor líquido do item

```text
(quantidade × preco_unitario) - desconto_item
```

## estoque

| Campo | Tipo | Regra |
|---|---|---|
| id_estoque | BIGINT | PK |
| id_filial | INT | FK → filial |
| id_produto | INT | FK → produto |
| estoque_atual | DECIMAL(12,3) | ≥ 0 |
| estoque_minimo | DECIMAL(12,3) | ≥ 0 |
| estoque_maximo | DECIMAL(12,3) | ≥ estoque_minimo |
| atualizado_em | DATETIME | obrigatório |

A combinação de filial e produto é única.

## meta_representante

| Campo | Tipo | Regra |
|---|---|---|
| id_meta | BIGINT | PK |
| id_representante | INT | FK → representante |
| competencia | DATE | primeiro dia do mês de referência |
| valor_meta | DECIMAL(14,2) | > 0 |

A combinação representante + competência é única.
