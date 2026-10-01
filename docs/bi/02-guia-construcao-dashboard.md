# Guia de Construção do Dashboard Power BI

> **Projeto:** Atlas Distribuidora Analytics  
> **Formato:** 16:9  
> **Objetivo:** transformar a camada analítica em uma experiência executiva clara e consistente.

## 1. Direção visual

O dashboard deve parecer uma ferramenta de gestão, não uma apresentação cheia de elementos decorativos.

### Paleta

| Função | Cor |
|---|---|
| Primária | Azul profundo `#16324F` |
| Destaque positivo | Verde petróleo `#2A9D8F` |
| Destaque secundário | Dourado `#E9C46A` |
| Informação | Azul `#457B9D` |
| Alerta | Coral `#E76F51` |
| Fundo | `#F7F9FC` |
| Texto principal | `#172B4D` |

O tema está disponível em:

`powerbi/tema-atlas.json`

## 2. Canvas

Configuração recomendada:

- proporção: 16:9;
- referência de construção: 1280 × 720;
- margem externa: 24 px;
- espaçamento entre blocos: 16 px;
- cards com alturas consistentes;
- no máximo 7–8 elementos analíticos principais por página.

## 3. Estrutura compartilhada

Todas as páginas devem manter:

```text
┌─────────────────────────────────────────────────────────────┐
│ ATLAS ANALYTICS                  Página / contexto          │
│ Período | Filial | UF | Categoria                          │
├─────────────────────────────────────────────────────────────┤
│ conteúdo específico da página                              │
│                                                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Cabeçalho

À esquerda:

**ATLAS DISTRIBUIDORA ANALYTICS**

À direita:

- nome da página;
- indicador discreto de última atualização, quando disponível.

### Navegação

Ordem fixa:

1. Visão Executiva
2. Performance Comercial
3. Clientes
4. Produtos e Categorias
5. Estoque

Usar botões discretos ou Page Navigator.

## 4. Página 01 — Visão Executiva

### Objetivo

Responder em poucos segundos:

**quanto vendemos, com que rentabilidade, contra qual meta e com qual tendência?**

### Wireframe

```text
┌─────────────────────────────────────────────────────────────┐
│ Cabeçalho + filtros                                         │
├──────────┬──────────┬──────────┬──────────┬──────────┬───────┤
│ Receita  │ Margem % │ Ticket   │ Meta %   │ MoM %    │Pedidos│
├────────────────────────────────┬────────────────────────────┤
│ Faturamento mensal             │ Faturamento x Meta         │
│ linha / área                   │ colunas + linha            │
├────────────────────────────────┼────────────────────────────┤
│ Receita por Categoria          │ Top 5 Representantes       │
│ barras                         │ barras horizontais         │
└────────────────────────────────┴────────────────────────────┘
```

### Cards

1. `[Faturamento]`
2. `[Margem %]`
3. `[Ticket Médio]`
4. `[Atingimento Meta %]`
5. `[Crescimento MoM %]`
6. `[Quantidade de Pedidos]`

### Faturamento mensal

- visual: linha;
- eixo: `dim_data[ano_mes]`;
- valor: `[Faturamento]`;
- tooltip: `[Margem Bruta]`, `[Margem %]`, `[Quantidade de Pedidos]`.

### Faturamento x Meta

- visual: linha e colunas agrupadas;
- eixo: `dim_data[ano_mes]`;
- coluna: `[Faturamento]`;
- linha: `[Meta]`.

### Receita por categoria

- visual: barras horizontais;
- categoria: `dim_produto[categoria]`;
- valor: `[Faturamento]`;
- ordenar por faturamento decrescente.

### Top 5 representantes

- visual: barras horizontais;
- categoria: `dim_representante[representante]`;
- valor: `[Faturamento]`;
- filtro Top N = 5.

## 5. Página 02 — Performance Comercial

### Wireframe

```text
┌─────────────────────────────────────────────────────────────┐
│ Cabeçalho + filtros                                         │
├───────────┬───────────┬───────────┬───────────┐             │
│ Receita   │ Meta      │ Meta %    │ Gap       │             │
├───────────────────────────────┬─────────────────────────────┤
│ Ranking Representantes        │ Receita x Meta por Rep      │
├───────────────────────────────┼─────────────────────────────┤
│ Evolução por Equipe           │ Matriz Hierárquica         │
└───────────────────────────────┴─────────────────────────────┘
```

### Hierarquia

`gerente → supervisor → representante`

Ativar drill-down na matriz e nos visuais que usam a hierarquia.

### Ranking

- representante;
- faturamento;
- meta;
- atingimento;
- posição;
- clientes compradores.

Aplicar formatação condicional somente em atingimento.

## 6. Página 03 — Clientes

### Objetivo

Mostrar concentração e composição da carteira.

### Wireframe

```text
┌─────────────────────────────────────────────────────────────┐
│ Cabeçalho + filtros                                         │
├──────────────┬──────────────┬──────────────┐                │
│ Clientes     │ Ticket Médio │ Fat./Cliente │                │
├─────────────────────────────┬───────────────────────────────┤
│ Top Clientes                │ Participação acumulada        │
├─────────────────────────────┼───────────────────────────────┤
│ Receita por UF              │ Tabela detalhada             │
└─────────────────────────────┴───────────────────────────────┘
```

### Tabela detalhada

- cliente;
- cidade;
- UF;
- faturamento;
- pedidos;
- ticket médio;
- participação.

## 7. Página 04 — Produtos e Categorias

### KPIs

- faturamento;
- margem bruta;
- margem %;
- quantidade vendida;
- preço médio unitário.

### Visuais

- faturamento por categoria;
- margem % por categoria;
- Top 10 produtos;
- dispersão faturamento × margem %;
- matriz categoria → produto.

### Dispersão

- eixo X: `[Faturamento]`;
- eixo Y: `[Margem %]`;
- detalhes: produto;
- tamanho: `[Quantidade Vendida]`.

Objetivo: distinguir produtos de grande receita e baixa rentabilidade daqueles com desempenho equilibrado.

## 8. Página 05 — Estoque

### KPIs

- valor em estoque;
- estoque atual;
- produtos abaixo do mínimo;
- produtos acima do máximo.

### Wireframe

```text
┌─────────────────────────────────────────────────────────────┐
│ Cabeçalho + filtros                                         │
├──────────────┬──────────────┬──────────────┬────────────────┤
│ Valor Estoque│ Estoque Atual│ Abaixo Mín.  │ Acima Máx.     │
├───────────────────────────────┬─────────────────────────────┤
│ Situação por Filial           │ Valor por Categoria        │
├───────────────────────────────┼─────────────────────────────┤
│ Produtos críticos             │ Matriz Produto x Filial    │
└───────────────────────────────┴─────────────────────────────┘
```

## 9. Interações

### Filtros sincronizados

Sincronizar entre páginas:

- período;
- filial;
- UF.

Categoria pode ser sincronizada apenas entre páginas onde fizer sentido.

### Cross-filter

Manter cross-filter ativo quando o clique ajudar a investigar a causa de um resultado.

Desativar interações em casos em que um visual de referência precise continuar mostrando o total.

## 10. Tooltips

Criar tooltip apenas quando houver ganho real de contexto.

Sugestões:

### Produto

- faturamento;
- margem %;
- quantidade;
- pedidos.

### Representante

- faturamento;
- meta;
- atingimento;
- clientes;
- ticket médio.

## 11. Formatação

### Moeda

`R$ #,##0` ou `R$ #,##0.00` conforme a granularidade.

### Percentuais

`0.0%`

### Quantidades

`#,##0`

### Valores grandes

Preferir unidades de exibição automáticas em cards e eixos, sem sacrificar entendimento.

## 12. O que evitar

- gráficos de pizza com muitas categorias;
- velocímetros para todo KPI;
- sombras pesadas;
- excesso de bordas;
- muitas cores concorrentes;
- títulos como "Soma de faturamento líquido";
- tabelas gigantes na página executiva;
- texto técnico de banco de dados exposto ao usuário final.

## 13. Critério visual de conclusão

A página está pronta quando:

- a pergunta de negócio é evidente;
- o usuário entende a hierarquia visual em menos de alguns segundos;
- nenhum elemento compete desnecessariamente com o KPI principal;
- cores possuem significado consistente;
- os mesmos filtros se comportam de forma previsível;
- o resultado pode ser explicado sem falar de nomes técnicos das tabelas.
