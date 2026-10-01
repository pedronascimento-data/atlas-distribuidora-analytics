-- ============================================================
-- ATLAS DISTRIBUIDORA ANALYTICS
-- 02 - VIEWS ANALÍTICAS
-- Pré-requisito: executar 01_schema_operacional.sql
-- ============================================================

USE atlas_distribuidora;

-- ------------------------------------------------------------
-- Vendas faturadas no grão de item
-- ------------------------------------------------------------

CREATE OR REPLACE VIEW vw_vendas_faturadas AS
SELECT
    p.id_pedido,
    p.numero_pedido,
    DATE(p.data_faturamento) AS data_faturamento,
    p.id_cliente,
    p.id_representante,
    p.id_filial,
    pi.id_produto,
    pi.quantidade,
    pi.preco_unitario,
    pi.custo_unitario,
    pi.desconto_item,
    (pi.quantidade * pi.preco_unitario) AS valor_bruto_item,
    ((pi.quantidade * pi.preco_unitario) - pi.desconto_item) AS faturamento_liquido_item,
    (pi.quantidade * pi.custo_unitario) AS custo_total_item,
    (
        ((pi.quantidade * pi.preco_unitario) - pi.desconto_item)
        - (pi.quantidade * pi.custo_unitario)
    ) AS margem_bruta_item
FROM pedido p
INNER JOIN pedido_item pi
    ON pi.id_pedido = p.id_pedido
WHERE p.status IN ('FATURADO', 'ENTREGUE')
  AND p.data_faturamento IS NOT NULL;

-- ------------------------------------------------------------
-- Estoque abaixo do mínimo
-- ------------------------------------------------------------

CREATE OR REPLACE VIEW vw_estoque_critico AS
SELECT
    e.id_filial,
    f.codigo AS codigo_filial,
    f.nome AS filial,
    e.id_produto,
    pr.sku,
    pr.descricao AS produto,
    e.estoque_atual,
    e.estoque_minimo,
    e.estoque_maximo,
    (e.estoque_minimo - e.estoque_atual) AS quantidade_abaixo_minimo
FROM estoque e
INNER JOIN filial f
    ON f.id_filial = e.id_filial
INNER JOIN produto pr
    ON pr.id_produto = e.id_produto
WHERE e.estoque_atual < e.estoque_minimo;

-- ------------------------------------------------------------
-- Faturamento mensal por representante
-- ------------------------------------------------------------

CREATE OR REPLACE VIEW vw_faturamento_mensal_representante AS
SELECT
    DATE_FORMAT(v.data_faturamento, '%Y-%m-01') AS competencia,
    v.id_representante,
    r.codigo AS codigo_representante,
    r.nome AS representante,
    s.nome AS supervisor,
    g.nome AS gerente,
    SUM(v.faturamento_liquido_item) AS faturamento
FROM vw_vendas_faturadas v
INNER JOIN representante r
    ON r.id_representante = v.id_representante
INNER JOIN supervisor s
    ON s.id_supervisor = r.id_supervisor
INNER JOIN gerente g
    ON g.id_gerente = s.id_gerente
GROUP BY
    DATE_FORMAT(v.data_faturamento, '%Y-%m-01'),
    v.id_representante,
    r.codigo,
    r.nome,
    s.nome,
    g.nome;

-- ------------------------------------------------------------
-- Atingimento de meta por representante
-- ------------------------------------------------------------

CREATE OR REPLACE VIEW vw_atingimento_meta AS
SELECT
    m.competencia,
    m.id_representante,
    r.codigo AS codigo_representante,
    r.nome AS representante,
    s.nome AS supervisor,
    g.nome AS gerente,
    m.valor_meta,
    COALESCE(f.faturamento, 0) AS faturamento,
    CASE
        WHEN m.valor_meta = 0 THEN NULL
        ELSE COALESCE(f.faturamento, 0) / m.valor_meta
    END AS percentual_atingimento
FROM meta_representante m
INNER JOIN representante r
    ON r.id_representante = m.id_representante
INNER JOIN supervisor s
    ON s.id_supervisor = r.id_supervisor
INNER JOIN gerente g
    ON g.id_gerente = s.id_gerente
LEFT JOIN vw_faturamento_mensal_representante f
    ON f.id_representante = m.id_representante
   AND f.competencia = DATE_FORMAT(m.competencia, '%Y-%m-01');

-- ------------------------------------------------------------
-- Última compra e classificação analítica do cliente
-- A referência usa CURRENT_DATE; em análises históricas,
-- a data de referência deverá vir do contexto do relatório.
-- ------------------------------------------------------------

CREATE OR REPLACE VIEW vw_ultima_compra_cliente AS
SELECT
    c.id_cliente,
    c.codigo AS codigo_cliente,
    c.razao_social,
    c.status AS status_cadastral,
    MAX(v.data_faturamento) AS data_ultima_compra,
    CASE
        WHEN MAX(v.data_faturamento) IS NULL THEN 'SEM_COMPRA'
        WHEN MAX(v.data_faturamento) < CURRENT_DATE - INTERVAL 90 DAY THEN 'INATIVO_90_DIAS'
        ELSE 'ATIVO_90_DIAS'
    END AS status_analitico
FROM cliente c
LEFT JOIN vw_vendas_faturadas v
    ON v.id_cliente = c.id_cliente
GROUP BY
    c.id_cliente,
    c.codigo,
    c.razao_social,
    c.status;
