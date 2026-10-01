# Configuração do Modelo Semântico no Power BI

> **Fonte:** MySQL — banco `atlas_dw`

## 1. Tabelas a carregar

Carregar apenas as tabelas analíticas:

### Dimensões

- `dim_data`
- `dim_cliente`
- `dim_produto`
- `dim_representante`
- `dim_filial`

### Fatos

- `fato_vendas`
- `fato_metas`
- `fato_estoque`

O banco operacional `atlas_distribuidora` não deve ser conectado ao mesmo modelo do dashboard.

## 2. Relacionamentos

Criar os relacionamentos abaixo com cardinalidade **1:N** e direção de filtro **Single**.

| Dimensão | Campo | Fato | Campo |
|---|---|---|---|
| dim_data | data_key | fato_vendas | data_key |
| dim_cliente | cliente_key | fato_vendas | cliente_key |
| dim_produto | produto_key | fato_vendas | produto_key |
| dim_representante | representante_key | fato_vendas | representante_key |
| dim_filial | filial_key | fato_vendas | filial_key |
| dim_data | data_key | fato_metas | data_key |
| dim_representante | representante_key | fato_metas | representante_key |
| dim_data | data_key | fato_estoque | data_key |
| dim_produto | produto_key | fato_estoque | produto_key |
| dim_filial | filial_key | fato_estoque | filial_key |

Não criar relacionamento entre tabelas fato.

## 3. Configuração da tabela calendário

Selecionar `dim_data` e:

1. marcar como **Date table**;
2. selecionar `data_completa` como coluna de data;
3. selecionar `ano_mes`;
4. usar **Sort by column → ano_mes_ordem**.

Isso garante sequência correta:

```text
2024-01
2024-02
2024-03
...
2025-01
```

em vez de ordenação textual inadequada.

## 4. Tipos de dados

### dim_data

| Campo | Tipo |
|---|---|
| data_key | inteiro |
| data_completa | data |
| dia | inteiro |
| mes | inteiro |
| trimestre | inteiro |
| ano | inteiro |
| ano_mes | texto |
| ano_mes_ordem | inteiro |
| fim_de_semana | verdadeiro/falso |

### Dimensões de negócio

Chaves: número inteiro.

Códigos, nomes, cidade, estado, UF, categoria, marca e fornecedor: texto.

### Fatos

- chaves: inteiro;
- quantidade/estoque: número decimal;
- valores monetários: decimal fixo/moeda;
- número do pedido: texto.

## 5. Campos ocultos

Ocultar da exibição do relatório:

### Todas as tabelas

- chaves técnicas `*_key`;
- IDs de origem.

### fato_vendas

Manter `numero_pedido` visível porque é usado em `DISTINCTCOUNT`.

Demais métricas numéricas podem ser ocultadas após a criação das medidas explícitas caso o objetivo seja impedir agregações automáticas.

## 6. Medidas

Criar uma tabela exclusiva para medidas, por exemplo:

`_Medidas`

Mover ou atribuir todas as medidas de `powerbi/medidas.dax` a essa tabela.

Sugestão de pastas de exibição:

- 01 Vendas
- 02 Tempo
- 03 Metas
- 04 Comercial
- 05 Estoque
- 06 Participação

## 7. Hierarquias

### Tempo

```text
Ano
  ↓
Trimestre
  ↓
Mês
  ↓
Data
```

### Comercial

```text
Gerente
  ↓
Supervisor
  ↓
Representante
```

### Produto

```text
Categoria
  ↓
Produto
```

### Geografia

```text
Estado / UF
  ↓
Cidade
```

## 8. Formatos

| Medida | Formato |
|---|---|
| Faturamento | R$ #,##0 |
| Margem Bruta | R$ #,##0 |
| Margem % | 0.0% |
| Ticket Médio | R$ #,##0.00 |
| Meta | R$ #,##0 |
| Atingimento Meta % | 0.0% |
| Crescimento MoM % | 0.0% |
| Crescimento YoY % | 0.0% |
| Quantidade de Pedidos | #,##0 |
| Quantidade Vendida | #,##0 |
| Valor em Estoque | R$ #,##0 |

## 9. Configuração de carga

Para um projeto de portfólio, **Import mode** é a escolha recomendada:

- melhor desempenho visual;
- suporte completo a DAX;
- volume compatível com o projeto;
- independência da conexão MySQL durante a navegação do relatório publicado como arquivo.

DirectQuery não agrega valor suficiente neste cenário.

## 10. Validação inicial

Antes de criar os visuais:

1. criar `[Faturamento]`;
2. comparar o total com `sql/06_validacoes_pipeline.sql`;
3. criar `[Quantidade de Pedidos]`;
4. validar filtros por mês;
5. testar um representante;
6. testar uma categoria;
7. somente então seguir para as páginas.

Isso reduz o risco de descobrir problemas de relacionamento depois que o dashboard já estiver diagramado.
