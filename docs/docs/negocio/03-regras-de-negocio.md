# Documento 03 — Regras de Negócio

> **Projeto:** Atlas Distribuidora Analytics  
> **Documento:** Regras de Negócio (Business Rules Document - BRD)  
> **Versão:** 1.0  
> **Status:** Em desenvolvimento  
> **Autor:** Pedro Nascimento  
> **Última atualização:** Julho de 2026

---

# 1. Objetivo

Este documento estabelece as regras que governam o funcionamento da operação da Atlas Distribuidora.

Essas regras serão utilizadas como referência para a modelagem do banco de dados, implementação das consultas SQL, construção do modelo dimensional e desenvolvimento dos dashboards.

---

# 2. Estrutura Organizacional

A Atlas Distribuidora possui uma estrutura comercial hierárquica.

Diretoria Comercial

↓

Gerentes Comerciais

↓

Supervisores

↓

Representantes Comerciais

↓

Clientes

Cada representante pertence obrigatoriamente a um único supervisor.

Cada supervisor gerencia vários representantes.

---

# 3. Clientes

### RN001

Todo cliente possui um código único.

---

### RN002

Todo cliente pertence a uma cidade.

---

### RN003

Cada cidade pertence a um estado.

---

### RN004

Cada cliente é atendido por apenas um representante.

---

### RN005

Um representante pode atender diversos clientes.

---

### RN006

Clientes podem ser classificados como:

- Ativo
- Inativo
- Bloqueado

---

### RN007

Um cliente será considerado inativo quando permanecer mais de **90 dias sem realizar compras**.

---

# 4. Produtos

### RN008

Todo produto pertence a apenas uma categoria.

---

### RN009

Todo produto pertence a apenas uma marca.

---

### RN010

Cada produto possui apenas um fornecedor principal.

---

### RN011

Um fornecedor pode fornecer diversos produtos.

---

### RN012

Produtos podem estar ativos ou inativos.

Produtos inativos não poderão ser vendidos.

---

# 5. Pedidos

### RN013

Todo pedido pertence a um único cliente.

---

### RN014

Todo pedido pertence a uma única filial.

---

### RN015

Todo pedido é registrado por um único representante.

---

### RN016

Um pedido poderá possuir um ou mais itens.

---

### RN017

Cada item do pedido representa um único produto.

---

### RN018

O faturamento será calculado utilizando apenas pedidos faturados.

Pedidos cancelados não participarão de nenhum indicador.

---

### RN019

Os status possíveis do pedido serão:

- Em Digitação
- Aprovado
- Faturado
- Cancelado
- Entregue

---

# 6. Estoque

### RN020

O estoque será controlado por produto e filial.

---

### RN021

Cada filial possuirá estoque independente.

---

### RN022

Todo produto possuirá:

- Estoque Atual
- Estoque Mínimo
- Estoque Máximo

---

### RN023

Produtos abaixo do estoque mínimo deverão ser sinalizados.

---

# 7. Metas

### RN024

As metas serão cadastradas mensalmente.

---

### RN025

Cada representante possuirá uma meta individual.

---

### RN026

Cada supervisor possuirá meta correspondente à soma das metas de sua equipe.

---

### RN027

O percentual de atingimento será calculado como:

```
Faturamento ÷ Meta
```

---

# 8. Indicadores

### RN028

Ticket Médio

```
Faturamento
──────────────
Quantidade de Pedidos
```

---

### RN029

Clientes Ativos

Clientes que realizaram pelo menos uma compra dentro do período analisado.

---

### RN030

Clientes Inativos

Clientes sem compras há mais de 90 dias.

---

### RN031

Representantes Ativos

Representantes que realizaram vendas no período.

---

### RN032

Receita

Somatório dos pedidos faturados.

---

### RN033

Margem Bruta

```
Receita - Custo
```

---

### RN034

Margem %

```
Margem Bruta ÷ Receita
```

---

# 9. Comissão

### RN035

A comissão será calculada apenas sobre pedidos faturados.

---

### RN036

Pedidos cancelados não gerarão comissão.

---

### RN037

Cada representante possuirá um percentual de comissão próprio.

---

# 10. Filiais

### RN038

Cada pedido pertence a apenas uma filial.

---

### RN039

Cada filial atenderá uma região específica.

---

### RN040

Uma filial poderá atender diversos estados.

---

# 11. Auditoria

Todas as tabelas principais possuirão:

- Data de criação
- Data de atualização
- Status

---

# 12. Premissas

- Todos os dados utilizados serão fictícios.
- Não existirão pedidos sem cliente.
- Não existirão pedidos sem representante.
- Não existirão produtos sem categoria.
- Não existirão clientes sem cidade.
- Não existirão cidades sem estado.

---

# Histórico

| Versão | Data | Autor | Alterações |
|--------|------|--------|------------|
| 1.0 | Julho/2026 | Pedro Nascimento | Criação inicial |
