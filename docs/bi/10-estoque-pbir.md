# Implementação PBIR — Página 05: Estoque

> **Status:** definição PBIR criada; validação visual no Power BI Desktop pendente.

## Objetivo

Monitorar o valor financeiro do estoque, limites mínimo/máximo e riscos operacionais por filial e produto.

## Ajustes no modelo

Durante a implementação, duas medidas já existentes no catálogo DAX foram sincronizadas com o TMDL:

- `Estoque Mínimo`;
- `Estoque Máximo`.

Também foram adicionadas:

### Posições Abaixo do Mínimo

Conta linhas produto × filial em que o estoque atual está abaixo do mínimo.

### Posições Acima do Máximo

Conta linhas produto × filial acima do estoque máximo.

### Gap para Estoque Mínimo

```text
Estoque Atual - Estoque Mínimo
```

Valores negativos indicam necessidade de reposição.

## Por que "posição" além de "produto"

`Produtos Abaixo do Mínimo` utiliza produto distinto. Isso responde quantos SKUs estão em risco em pelo menos uma filial.

`Posições Abaixo do Mínimo` preserva a granularidade operacional **produto × filial**, permitindo identificar se um mesmo produto está crítico em várias unidades.

As duas métricas são úteis e respondem perguntas diferentes.

## Visuais implementados

| Visual | Tipo PBIR | Campo / medida |
|---|---|---|
| Valor em Estoque | cardVisual | `[Valor em Estoque]` |
| Estoque Atual | cardVisual | `[Estoque Atual]` |
| Produtos Abaixo do Mínimo | cardVisual | `[Produtos Abaixo do Mínimo]` |
| Produtos Acima do Máximo | cardVisual | `[Produtos Acima do Máximo]` |
| Valor por filial | barChart | filial + valor em estoque |
| Valor por categoria | barChart | categoria + valor em estoque |
| Posições críticas por filial | columnChart | filial + posições abaixo do mínimo |
| Diagnóstico produto × filial | tableEx | filial, categoria, SKU, produto e limites |

## Tabela de diagnóstico

A tabela apresenta:

- filial;
- categoria;
- SKU;
- produto;
- estoque atual;
- estoque mínimo;
- estoque máximo;
- gap para o mínimo;
- valor em estoque.

A ordenação inicial é pelo **Gap para Estoque Mínimo crescente**, fazendo as maiores faltas aparecerem primeiro.

## Leitura de negócio

A página permite responder:

1. qual capital está imobilizado em estoque;
2. quais filiais concentram maior valor;
3. quais categorias concentram estoque;
4. quantos produtos possuem risco de ruptura;
5. quantas posições produto × filial estão abaixo do mínimo;
6. quais itens precisam de reposição prioritária;
7. onde há excesso acima do máximo.

## Validação no Desktop

- [ ] reconhecer os 8 visuais;
- [ ] validar Estoque Atual/Mínimo/Máximo;
- [ ] validar Produtos Abaixo/Acima dos limites;
- [ ] validar Posições Abaixo do Mínimo;
- [ ] conferir ordenação do gap;
- [ ] testar filtro por filial;
- [ ] testar filtro por categoria;
- [ ] verificar snapshot/data do estoque;
- [ ] reconciliar valor em estoque com o DW;
- [ ] revisar largura das colunas da tabela.

## Critério de conclusão

A autoria PBIR da quinta página está concluída. Com isso, todas as páginas planejadas possuem definições de visuais versionadas.

O dashboard completo ainda precisa ser renderizado, validado e refinado no Power BI Desktop antes de ser considerado final.
