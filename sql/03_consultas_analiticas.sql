-- ============================================================
-- ATLAS DISTRIBUIDORA ANALYTICS
-- 03 - CONSULTAS ANALÍTICAS DE PORTFÓLIO
-- Conceitos: JOIN, CTE, agregação, subquery e window functions
-- ============================================================

USE atlas_distribuidora;

-- ============================================================
-- 1. KPIs EXECUTIVOS
-- ============================================================

SELECT
    ROUND(SUM(faturamento_liquido_item), 2) AS faturamento_total,
    COUNT(DISTINCT id_pedido) AS quantidade_pedidos,
    COUNT(DISTINCT id_cliente) AS clientes_compradores,
    ROUND(
        SUM(faturamento_liquido_item) / NULLIF(COUNT(DISTINCT id_pedido), 0),
        2
    ) AS ticket_medio,
    ROUND(SUM(margem_bruta_item), 2) AS margem_bruta,
    ROUND(
        SUM(margem_bruta_item) / NULLIF(SUM(faturamento_liquido_item), 0) * 100,
        2
    ) AS margem_percentual
FROM vw_vendas_faturadas;

-- ============================================================
-- 2. EVOLUÇÃO MENSAL E CRESCIMENTO MÊS CONTRA MÊS
-- Window function: LAG
-- ============================================================

WITH faturamento_mensal AS (
    SELECT
        DATE_FORMAT(data_faturamento, '%Y-%m-01') AS competencia,
        SUM(faturamento_liquido_item) AS faturamento
    FROM vw_vendas_faturadas
    GROUP BY DATE_FORMAT(data_faturamento, '%Y-%m-01')
),
comparativo AS (
    SELECT
        competencia,
        faturamento,
        LAG(faturamento) OVER (ORDER BY competencia) AS faturamento_mes_anterior
    FROM faturamento_mensal
)
SELECT
    competencia,
    ROUND(faturamento, 2) AS faturamento,
    ROUND(faturamento_mes_anterior, 2) AS faturamento_mes_anterior,
    ROUND(
        (faturamento - faturamento_mes_anterior)
        / NULLIF(faturamento_mes_anterior, 0) * 100,
        2
    ) AS crescimento_percentual
FROM comparativo
ORDER BY competencia;

-- ============================================================
-- 3. RANKING DE REPRESENTANTES POR FATURAMENTO
-- Window functions: RANK e participação percentual
-- ============================================================

WITH vendas_rep AS (
    SELECT
        r.id_representante,
        r.nome AS representante,
        s.nome AS supervisor,
        SUM(v.faturamento_liquido_item) AS faturamento
    FROM vw_vendas_faturadas v
    INNER JOIN representante r
        ON r.id_representante = v.id_representante
    INNER JOIN supervisor s
        ON s.id_supervisor = r.id_supervisor
    GROUP BY
        r.id_representante,
        r.nome,
        s.nome
)
SELECT
    representante,
    supervisor,
    ROUND(faturamento, 2) AS faturamento,
    RANK() OVER (ORDER BY faturamento DESC) AS ranking,
    ROUND(
        faturamento / NULLIF(SUM(faturamento) OVER (), 0) * 100,
        2
    ) AS participacao_percentual
FROM vendas_rep
ORDER BY ranking, representante;

-- ============================================================
-- 4. TOP 10 CLIENTES E CONCENTRAÇÃO DE RECEITA
-- ============================================================

WITH receita_cliente AS (
    SELECT
        c.id_cliente,
        c.razao_social,
        ci.nome AS cidade,
        e.uf,
        SUM(v.faturamento_liquido_item) AS faturamento
    FROM vw_vendas_faturadas v
    INNER JOIN cliente c
        ON c.id_cliente = v.id_cliente
    INNER JOIN cidade ci
        ON ci.id_cidade = c.id_cidade
    INNER JOIN estado e
        ON e.id_estado = ci.id_estado
    GROUP BY
        c.id_cliente,
        c.razao_social,
        ci.nome,
        e.uf
),
ranking AS (
    SELECT
        *,
        ROW_NUMBER() OVER (ORDER BY faturamento DESC) AS posicao,
        SUM(faturamento) OVER () AS faturamento_total
    FROM receita_cliente
)
SELECT
    posicao,
    razao_social,
    cidade,
    uf,
    ROUND(faturamento, 2) AS faturamento,
    ROUND(faturamento / NULLIF(faturamento_total, 0) * 100, 2)
        AS participacao_percentual
FROM ranking
WHERE posicao <= 10
ORDER BY posicao;

-- ============================================================
-- 5. PERFORMANCE POR CATEGORIA
-- ============================================================

SELECT
    c.nome AS categoria,
    ROUND(SUM(v.faturamento_liquido_item), 2) AS faturamento,
    ROUND(SUM(v.margem_bruta_item), 2) AS margem_bruta,
    ROUND(
        SUM(v.margem_bruta_item)
        / NULLIF(SUM(v.faturamento_liquido_item), 0) * 100,
        2
    ) AS margem_percentual,
    SUM(v.quantidade) AS quantidade_vendida
FROM vw_vendas_faturadas v
INNER JOIN produto p
    ON p.id_produto = v.id_produto
INNER JOIN categoria c
    ON c.id_categoria = p.id_categoria
GROUP BY c.id_categoria, c.nome
ORDER BY faturamento DESC;

-- ============================================================
-- 6. PRODUTOS COM BAIXO GIRO
-- Produtos ativos sem venda nos últimos 90 dias ou nunca vendidos
-- ============================================================

WITH ultima_venda AS (
    SELECT
        id_produto,
        MAX(data_faturamento) AS data_ultima_venda,
        SUM(quantidade) AS quantidade_historica
    FROM vw_vendas_faturadas
    GROUP BY id_produto
)
SELECT
    p.sku,
    p.descricao,
    c.nome AS categoria,
    uv.data_ultima_venda,
    COALESCE(uv.quantidade_historica, 0) AS quantidade_historica,
    CASE
        WHEN uv.data_ultima_venda IS NULL THEN 'SEM_VENDA'
        WHEN uv.data_ultima_venda < CURRENT_DATE - INTERVAL 90 DAY
            THEN 'SEM_VENDA_90_DIAS'
        ELSE 'COM_GIRO'
    END AS classificacao_giro
FROM produto p
INNER JOIN categoria c
    ON c.id_categoria = p.id_categoria
LEFT JOIN ultima_venda uv
    ON uv.id_produto = p.id_produto
WHERE p.ativo = TRUE
  AND (
      uv.data_ultima_venda IS NULL
      OR uv.data_ultima_venda < CURRENT_DATE - INTERVAL 90 DAY
  )
ORDER BY uv.data_ultima_venda, p.descricao;

-- ============================================================
-- 7. CLIENTES INATIVOS HÁ MAIS DE 90 DIAS
-- ============================================================

SELECT
    codigo_cliente,
    razao_social,
    data_ultima_compra,
    status_analitico
FROM vw_ultima_compra_cliente
WHERE status_analitico IN ('INATIVO_90_DIAS', 'SEM_COMPRA')
ORDER BY data_ultima_compra;

-- ============================================================
-- 8. ATINGIMENTO DE META E FAIXA DE PERFORMANCE
-- ============================================================

SELECT
    competencia,
    representante,
    supervisor,
    ROUND(valor_meta, 2) AS meta,
    ROUND(faturamento, 2) AS faturamento,
    ROUND(percentual_atingimento * 100, 2) AS atingimento_percentual,
    CASE
        WHEN percentual_atingimento >= 1 THEN 'META_ATINGIDA'
        WHEN percentual_atingimento >= 0.80 THEN 'PROXIMO_DA_META'
        ELSE 'ABAIXO_DA_META'
    END AS faixa_performance
FROM vw_atingimento_meta
ORDER BY competencia, percentual_atingimento DESC;

-- ============================================================
-- 9. META CONSOLIDADA POR SUPERVISOR
-- Regra: meta do supervisor = soma das metas de sua equipe
-- ============================================================

SELECT
    m.competencia,
    s.id_supervisor,
    s.nome AS supervisor,
    ROUND(SUM(m.valor_meta), 2) AS meta_supervisor,
    ROUND(SUM(COALESCE(a.faturamento, 0)), 2) AS faturamento_equipe,
    ROUND(
        SUM(COALESCE(a.faturamento, 0))
        / NULLIF(SUM(m.valor_meta), 0) * 100,
        2
    ) AS atingimento_percentual
FROM meta_representante m
INNER JOIN representante r
    ON r.id_representante = m.id_representante
INNER JOIN supervisor s
    ON s.id_supervisor = r.id_supervisor
LEFT JOIN vw_atingimento_meta a
    ON a.id_representante = m.id_representante
   AND a.competencia = m.competencia
GROUP BY
    m.competencia,
    s.id_supervisor,
    s.nome
ORDER BY m.competencia, atingimento_percentual DESC;

-- ============================================================
-- 10. ESTOQUE CRÍTICO POR FILIAL
-- ============================================================

SELECT
    filial,
    COUNT(*) AS produtos_abaixo_minimo,
    ROUND(SUM(quantidade_abaixo_minimo), 3) AS unidades_para_minimo
FROM vw_estoque_critico
GROUP BY id_filial, filial
ORDER BY produtos_abaixo_minimo DESC;
