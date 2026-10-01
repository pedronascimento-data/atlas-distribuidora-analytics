# Implementação PBIR — Página 01: Visão Executiva

> **Status:** definição PBIR criada; validação visual no Power BI Desktop pendente.

## Objetivo

Materializar em arquivos `visual.json` a primeira página do dashboard, reduzindo a dependência de montagem manual.

## Canvas

- 1280 × 720
- fundo `#F7F9FC`
- cards no topo
- dois gráficos no bloco intermediário
- dois gráficos no bloco inferior

## Visuais implementados

| Visual | Tipo PBIR | Campo / medida |
|---|---|---|
| Faturamento | cardVisual | `[Faturamento]` |
| Margem % | cardVisual | `[Margem %]` |
| Ticket Médio | cardVisual | `[Ticket Médio]` |
| Atingimento Meta % | cardVisual | `[Atingimento Meta %]` |
| Crescimento MoM % | cardVisual | `[Crescimento MoM %]` |
| Pedidos | cardVisual | `[Quantidade de Pedidos]` |
| Evolução mensal | lineChart | `dim_data[ano_mes]` + `[Faturamento]` |
| Faturamento x Meta | columnChart | `dim_data[ano_mes]` + `[Faturamento]` + `[Meta]` |
| Faturamento por categoria | barChart | `dim_produto[categoria]` + `[Faturamento]` |
| Representantes por faturamento | barChart | `dim_representante[representante]` + `[Faturamento]` |

## Arquitetura dos arquivos

Cada visual possui sua própria pasta:

```text
definition/pages/<pagina>/visuals/<visual-id>/visual.json
```

Isso permite que alterações de layout, campo ou formatação apareçam individualmente no diff do Git.

## Decisão sobre Top N

O visual de representantes foi criado inicialmente como **ranking por faturamento sem filtro Top N persistido**.

O Top 5 será aplicado após a primeira validação no Power BI Desktop. Essa escolha evita inserir um filtro PBIR complexo sem validação de renderização.

## Validação necessária no Desktop

Após abrir o `.pbip`:

- [ ] confirmar que os 10 visuais são reconhecidos;
- [ ] confirmar os seis cards;
- [ ] validar os papéis `Category`, `Y` e `Data`;
- [ ] verificar a ordenação de `ano_mes`;
- [ ] ordenar categoria e representante por faturamento decrescente;
- [ ] aplicar Top 5 em representantes;
- [ ] importar o tema Atlas;
- [ ] reconciliar Faturamento, Meta, Margem e Pedidos com SQL;
- [ ] revisar espaçamento e responsividade;
- [ ] salvar e revisar o diff gerado pelo Desktop.

## Critério de conclusão

A página só será marcada como finalizada após ser renderizada no Power BI Desktop e passar pelo checklist de QA.
