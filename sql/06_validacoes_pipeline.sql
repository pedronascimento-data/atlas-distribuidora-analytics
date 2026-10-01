-- ============================================================
-- ATLAS DISTRIBUIDORA ANALYTICS
-- 06 - VALIDAÇÕES DO PIPELINE
-- ============================================================

-- 1. Linhas faturadas na origem x fato de vendas
SELECT
    (
        SELECT COUNT(*)
        FROM atlas_distribuidora.pedido p
        INNER JOIN atlas_distribuidora.pedido_item pi
            ON pi.id_pedido = p.id_pedido
        WHERE p.status IN ('FATURADO', 'ENTREGUE')
          AND p.data_faturamento IS NOT NULL
    ) AS linhas_origem,
    (
        SELECT COUNT(*)
        FROM atlas_dw.fato_vendas
    ) AS linhas_dw;

-- 2. Reconciliação do faturamento
SELECT
    ROUND((
        SELECT SUM((pi.quantidade * pi.preco_unitario) - pi.desconto_item)
        FROM atlas_distribuidora.pedido p
        INNER JOIN atlas_distribuidora.pedido_item pi
            ON pi.id_pedido = p.id_pedido
        WHERE p.status IN ('FATURADO', 'ENTREGUE')
          AND p.data_faturamento IS NOT NULL
    ), 2) AS faturamento_origem,
    ROUND((
        SELECT SUM(faturamento_liquido)
        FROM atlas_dw.fato_vendas
    ), 2) AS faturamento_dw;

-- 3. Metas na origem x fato de metas
SELECT
    (SELECT COUNT(*) FROM atlas_distribuidora.meta_representante) AS metas_origem,
    (SELECT COUNT(*) FROM atlas_dw.fato_metas) AS metas_dw;

-- 4. Dimensões com chaves de negócio duplicadas
SELECT 'dim_cliente' AS teste, COUNT(*) AS duplicidades
FROM (
    SELECT id_cliente_origem
    FROM atlas_dw.dim_cliente
    GROUP BY id_cliente_origem
    HAVING COUNT(*) > 1
) x
UNION ALL
SELECT 'dim_produto', COUNT(*)
FROM (
    SELECT id_produto_origem
    FROM atlas_dw.dim_produto
    GROUP BY id_produto_origem
    HAVING COUNT(*) > 1
) x
UNION ALL
SELECT 'dim_representante', COUNT(*)
FROM (
    SELECT id_representante_origem
    FROM atlas_dw.dim_representante
    GROUP BY id_representante_origem
    HAVING COUNT(*) > 1
) x
UNION ALL
SELECT 'dim_filial', COUNT(*)
FROM (
    SELECT id_filial_origem
    FROM atlas_dw.dim_filial
    GROUP BY id_filial_origem
    HAVING COUNT(*) > 1
) x;

-- 5. Fatos sem correspondência dimensional
SELECT
    SUM(dd.data_key IS NULL) AS sem_data,
    SUM(dc.cliente_key IS NULL) AS sem_cliente,
    SUM(dp.produto_key IS NULL) AS sem_produto,
    SUM(dr.representante_key IS NULL) AS sem_representante,
    SUM(df.filial_key IS NULL) AS sem_filial
FROM atlas_dw.fato_vendas fv
LEFT JOIN atlas_dw.dim_data dd ON dd.data_key = fv.data_key
LEFT JOIN atlas_dw.dim_cliente dc ON dc.cliente_key = fv.cliente_key
LEFT JOIN atlas_dw.dim_produto dp ON dp.produto_key = fv.produto_key
LEFT JOIN atlas_dw.dim_representante dr ON dr.representante_key = fv.representante_key
LEFT JOIN atlas_dw.dim_filial df ON df.filial_key = fv.filial_key;

-- 6. Regras básicas de qualidade
SELECT
    SUM(faturamento_liquido < 0) AS vendas_negativas,
    SUM(quantidade <= 0) AS quantidades_invalidas,
    SUM(custo_total < 0) AS custos_negativos
FROM atlas_dw.fato_vendas;

-- Resultado esperado:
-- * contagens origem e DW iguais;
-- * faturamento reconciliado;
-- * zero duplicidades;
-- * zero FKs sem dimensão;
-- * zero valores inválidos.
