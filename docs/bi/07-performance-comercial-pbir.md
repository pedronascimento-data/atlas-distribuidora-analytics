# Implementação PBIR — Página 02: Performance Comercial

> **Status:** definição PBIR criada; validação visual no Power BI Desktop pendente.

## Objetivo

Transformar a página comercial em um espaço de análise de desempenho, metas e hierarquia de equipe.

## Visuais implementados

| Visual | Tipo PBIR | Campo / medida |
|---|---|---|
| Faturamento | cardVisual | `[Faturamento]` |
| Meta | cardVisual | `[Meta]` |
| Atingimento Meta % | cardVisual | `[Atingimento Meta %]` |
| Gap para Meta | cardVisual | `[Gap para Meta]` |
| Ranking de representantes | barChart | representante + `[Faturamento]` |
| Faturamento x Meta | columnChart | representante + `[Faturamento]` + `[Meta]` |
| Evolução mensal da equipe | lineChart | ano/mês + faturamento + meta |
| Hierarquia comercial | tableEx | gerente, supervisor, representante e KPIs |

## Hierarquia

A tabela detalhada apresenta:

`Gerente → Supervisor → Representante`

junto com:

- ranking;
- faturamento;
- meta;
- atingimento;
- clientes compradores;
- ticket médio.

## Decisões

### Ranking

O ranking é ordenado por faturamento decrescente. O filtro Top N será aplicado após validação no Power BI Desktop.

### Comparação de meta

A página usa as mesmas medidas do modelo semântico. Percentuais não são somados: o atingimento é recalculado pelo contexto do filtro.

### Evolução

A linha mensal combina faturamento e meta, permitindo que filtros de gerente, supervisor ou representante transformem o visual em uma análise de equipe específica.

## Validação no Desktop

- [ ] reconhecer os 8 visuais;
- [ ] validar cards de faturamento, meta, atingimento e gap;
- [ ] conferir ordenação do ranking;
- [ ] testar filtro por gerente;
- [ ] testar filtro por supervisor;
- [ ] testar filtro por representante;
- [ ] verificar faturamento x meta;
- [ ] validar totais da tabela;
- [ ] aplicar Top N após renderização;
- [ ] revisar espaçamento e legibilidade;
- [ ] reconciliar totais com SQL.

## Critério de conclusão

A autoria PBIR está concluída. A página será considerada finalizada somente após renderização e QA no Power BI Desktop.
