-- ============================================================
-- ATLAS DISTRIBUIDORA ANALYTICS
-- 05 - ETL DIMENSIONAL
-- Origem: atlas_distribuidora
-- Destino: atlas_dw
-- Pré-requisitos:
--   01_schema_operacional.sql
--   02_views_analiticas.sql
--   carga dos dados operacionais
--   04_schema_dimensional.sql
-- ============================================================

SET SESSION cte_max_recursion_depth = 5000;

-- ============================================================
-- 1. DIMENSÃO DATA
-- ============================================================

INSERT INTO atlas_dw.dim_data (
    data_key,
    data_completa,
    dia,
    mes,
    nome_mes,
    trimestre,
    ano,
    ano_mes,
    dia_semana,
    nome_dia_semana,
    fim_de_semana
)
WITH RECURSIVE datas AS (
    SELECT DATE('2024-01-01') AS data_completa
    UNION ALL
    SELECT data_completa + INTERVAL 1 DAY
    FROM datas
    WHERE data_completa < DATE('2030-12-31')
)
SELECT
    CAST(DATE_FORMAT(data_completa, '%Y%m%d') AS UNSIGNED),
    data_completa,
    DAY(data_completa),
    MONTH(data_completa),
    CASE MONTH(data_completa)
        WHEN 1 THEN 'Janeiro'
        WHEN 2 THEN 'Fevereiro'
        WHEN 3 THEN 'Março'
        WHEN 4 THEN 'Abril'
        WHEN 5 THEN 'Maio'
        WHEN 6 THEN 'Junho'
        WHEN 7 THEN 'Julho'
        WHEN 8 THEN 'Agosto'
        WHEN 9 THEN 'Setembro'
        WHEN 10 THEN 'Outubro'
        WHEN 11 THEN 'Novembro'
        WHEN 12 THEN 'Dezembro'
    END,
    QUARTER(data_completa),
    YEAR(data_completa),
    DATE_FORMAT(data_completa, '%Y-%m'),
    DAYOFWEEK(data_completa),
    CASE DAYOFWEEK(data_completa)
        WHEN 1 THEN 'Domingo'
        WHEN 2 THEN 'Segunda-feira'
        WHEN 3 THEN 'Terça-feira'
        WHEN 4 THEN 'Quarta-feira'
        WHEN 5 THEN 'Quinta-feira'
        WHEN 6 THEN 'Sexta-feira'
        WHEN 7 THEN 'Sábado'
    END,
    DAYOFWEEK(data_completa) IN (1, 7)
FROM datas;

-- ============================================================
-- 2. DIMENSÃO CLIENTE
-- ============================================================

INSERT INTO atlas_dw.dim_cliente (
    id_cliente_origem,
    codigo_cliente,
    razao_social,
    nome_fantasia,
    status_cadastral,
    cidade,
    estado,
    uf
)
SELECT
    c.id_cliente,
    c.codigo,
    c.razao_social,
    c.nome_fantasia,
    c.status,
    ci.nome,
    e.nome,
    e.uf
FROM atlas_distribuidora.cliente c
INNER JOIN atlas_distribuidora.cidade ci
    ON ci.id_cidade = c.id_cidade
INNER JOIN atlas_distribuidora.estado e
    ON e.id_estado = ci.id_estado;

-- ============================================================
-- 3. DIMENSÃO PRODUTO
-- ============================================================

INSERT INTO atlas_dw.dim_produto (
    id_produto_origem,
    sku,
    produto,
    categoria,
    marca,
    fornecedor,
    status_produto
)
SELECT
    p.id_produto,
    p.sku,
    p.descricao,
    c.nome,
    m.nome,
    COALESCE(f.nome_fantasia, f.razao_social),
    CASE WHEN p.ativo THEN 'ATIVO' ELSE 'INATIVO' END
FROM atlas_distribuidora.produto p
INNER JOIN atlas_distribuidora.categoria c
    ON c.id_categoria = p.id_categoria
INNER JOIN atlas_distribuidora.marca m
    ON m.id_marca = p.id_marca
INNER JOIN atlas_distribuidora.fornecedor f
    ON f.id_fornecedor = p.id_fornecedor;

-- ============================================================
-- 4. DIMENSÃO REPRESENTANTE
-- ============================================================

INSERT INTO atlas_dw.dim_representante (
    id_representante_origem,
    codigo_representante,
    representante,
    supervisor,
    gerente,
    status_representante
)
SELECT
    r.id_representante,
    r.codigo,
    r.nome,
    s.nome,
    g.nome,
    CASE WHEN r.ativo THEN 'ATIVO' ELSE 'INATIVO' END
FROM atlas_distribuidora.representante r
INNER JOIN atlas_distribuidora.supervisor s
    ON s.id_supervisor = r.id_supervisor
INNER JOIN atlas_distribuidora.gerente g
    ON g.id_gerente = s.id_gerente;

-- ============================================================
-- 5. DIMENSÃO FILIAL
-- ============================================================

INSERT INTO atlas_dw.dim_filial (
    id_filial_origem,
    codigo_filial,
    filial,
    cidade,
    estado,
    uf,
    status_filial
)
SELECT
    f.id_filial,
    f.codigo,
    f.nome,
    ci.nome,
    e.nome,
    e.uf,
    CASE WHEN f.ativa THEN 'ATIVA' ELSE 'INATIVA' END
FROM atlas_distribuidora.filial f
INNER JOIN atlas_distribuidora.cidade ci
    ON ci.id_cidade = f.id_cidade
INNER JOIN atlas_distribuidora.estado e
    ON e.id_estado = ci.id_estado;

-- ============================================================
-- 6. FATO VENDAS
-- Grão: item de pedido faturado/entregue
-- ============================================================

INSERT INTO atlas_dw.fato_vendas (
    id_pedido_item_origem,
    data_key,
    cliente_key,
    produto_key,
    representante_key,
    filial_key,
    numero_pedido,
    quantidade,
    valor_bruto,
    desconto,
    faturamento_liquido,
    custo_total,
    margem_bruta
)
SELECT
    pi.id_pedido_item,
    CAST(DATE_FORMAT(p.data_faturamento, '%Y%m%d') AS UNSIGNED),
    dc.cliente_key,
    dp.produto_key,
    dr.representante_key,
    df.filial_key,
    p.numero_pedido,
    pi.quantidade,
    ROUND(pi.quantidade * pi.preco_unitario, 2),
    pi.desconto_item,
    ROUND((pi.quantidade * pi.preco_unitario) - pi.desconto_item, 2),
    ROUND(pi.quantidade * pi.custo_unitario, 2),
    ROUND(
        ((pi.quantidade * pi.preco_unitario) - pi.desconto_item)
        - (pi.quantidade * pi.custo_unitario),
        2
    )
FROM atlas_distribuidora.pedido p
INNER JOIN atlas_distribuidora.pedido_item pi
    ON pi.id_pedido = p.id_pedido
INNER JOIN atlas_dw.dim_cliente dc
    ON dc.id_cliente_origem = p.id_cliente
INNER JOIN atlas_dw.dim_produto dp
    ON dp.id_produto_origem = pi.id_produto
INNER JOIN atlas_dw.dim_representante dr
    ON dr.id_representante_origem = p.id_representante
INNER JOIN atlas_dw.dim_filial df
    ON df.id_filial_origem = p.id_filial
WHERE p.status IN ('FATURADO', 'ENTREGUE')
  AND p.data_faturamento IS NOT NULL;

-- ============================================================
-- 7. FATO METAS
-- Grão: representante por competência mensal
-- ============================================================

INSERT INTO atlas_dw.fato_metas (
    id_meta_origem,
    data_key,
    representante_key,
    valor_meta
)
SELECT
    m.id_meta,
    CAST(DATE_FORMAT(m.competencia, '%Y%m%d') AS UNSIGNED),
    dr.representante_key,
    m.valor_meta
FROM atlas_distribuidora.meta_representante m
INNER JOIN atlas_dw.dim_representante dr
    ON dr.id_representante_origem = m.id_representante;

-- ============================================================
-- 8. FATO ESTOQUE
-- Grão: snapshot produto x filial x data
-- ============================================================

INSERT INTO atlas_dw.fato_estoque (
    id_estoque_origem,
    data_key,
    filial_key,
    produto_key,
    estoque_atual,
    estoque_minimo,
    estoque_maximo,
    valor_estoque
)
SELECT
    e.id_estoque,
    CAST(DATE_FORMAT(DATE(e.atualizado_em), '%Y%m%d') AS UNSIGNED),
    df.filial_key,
    dp.produto_key,
    e.estoque_atual,
    e.estoque_minimo,
    e.estoque_maximo,
    ROUND(e.estoque_atual * p.custo_atual, 2)
FROM atlas_distribuidora.estoque e
INNER JOIN atlas_distribuidora.produto p
    ON p.id_produto = e.id_produto
INNER JOIN atlas_dw.dim_produto dp
    ON dp.id_produto_origem = e.id_produto
INNER JOIN atlas_dw.dim_filial df
    ON df.id_filial_origem = e.id_filial;
