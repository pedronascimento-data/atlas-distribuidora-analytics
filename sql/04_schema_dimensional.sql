-- ============================================================
-- ATLAS DISTRIBUIDORA ANALYTICS
-- 04 - SCHEMA DIMENSIONAL
-- Banco alvo: MySQL 8+
-- ============================================================

DROP DATABASE IF EXISTS atlas_dw;
CREATE DATABASE atlas_dw
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE atlas_dw;

CREATE TABLE dim_data (
    data_key INT PRIMARY KEY,
    data_completa DATE NOT NULL UNIQUE,
    dia TINYINT NOT NULL,
    mes TINYINT NOT NULL,
    nome_mes VARCHAR(20) NOT NULL,
    trimestre TINYINT NOT NULL,
    ano SMALLINT NOT NULL,
    ano_mes CHAR(7) NOT NULL,
    dia_semana TINYINT NOT NULL,
    nome_dia_semana VARCHAR(20) NOT NULL,
    fim_de_semana BOOLEAN NOT NULL
);

CREATE TABLE dim_cliente (
    cliente_key INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente_origem INT NOT NULL UNIQUE,
    codigo_cliente VARCHAR(20) NOT NULL,
    razao_social VARCHAR(150) NOT NULL,
    nome_fantasia VARCHAR(150),
    status_cadastral VARCHAR(20) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    estado VARCHAR(60) NOT NULL,
    uf CHAR(2) NOT NULL
);

CREATE TABLE dim_produto (
    produto_key INT AUTO_INCREMENT PRIMARY KEY,
    id_produto_origem INT NOT NULL UNIQUE,
    sku VARCHAR(30) NOT NULL,
    produto VARCHAR(180) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    marca VARCHAR(100) NOT NULL,
    fornecedor VARCHAR(150) NOT NULL,
    status_produto VARCHAR(10) NOT NULL
);

CREATE TABLE dim_representante (
    representante_key INT AUTO_INCREMENT PRIMARY KEY,
    id_representante_origem INT NOT NULL UNIQUE,
    codigo_representante VARCHAR(20) NOT NULL,
    representante VARCHAR(120) NOT NULL,
    supervisor VARCHAR(120) NOT NULL,
    gerente VARCHAR(120) NOT NULL,
    status_representante VARCHAR(10) NOT NULL
);

CREATE TABLE dim_filial (
    filial_key INT AUTO_INCREMENT PRIMARY KEY,
    id_filial_origem INT NOT NULL UNIQUE,
    codigo_filial VARCHAR(10) NOT NULL,
    filial VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    estado VARCHAR(60) NOT NULL,
    uf CHAR(2) NOT NULL,
    status_filial VARCHAR(10) NOT NULL
);

CREATE TABLE fato_vendas (
    venda_key BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_pedido_item_origem BIGINT NOT NULL UNIQUE,
    data_key INT NOT NULL,
    cliente_key INT NOT NULL,
    produto_key INT NOT NULL,
    representante_key INT NOT NULL,
    filial_key INT NOT NULL,
    numero_pedido VARCHAR(30) NOT NULL,
    quantidade DECIMAL(12,3) NOT NULL,
    valor_bruto DECIMAL(14,2) NOT NULL,
    desconto DECIMAL(14,2) NOT NULL,
    faturamento_liquido DECIMAL(14,2) NOT NULL,
    custo_total DECIMAL(14,2) NOT NULL,
    margem_bruta DECIMAL(14,2) NOT NULL,
    CONSTRAINT fk_vendas_data FOREIGN KEY (data_key) REFERENCES dim_data(data_key),
    CONSTRAINT fk_vendas_cliente FOREIGN KEY (cliente_key) REFERENCES dim_cliente(cliente_key),
    CONSTRAINT fk_vendas_produto FOREIGN KEY (produto_key) REFERENCES dim_produto(produto_key),
    CONSTRAINT fk_vendas_representante FOREIGN KEY (representante_key) REFERENCES dim_representante(representante_key),
    CONSTRAINT fk_vendas_filial FOREIGN KEY (filial_key) REFERENCES dim_filial(filial_key)
);

CREATE TABLE fato_metas (
    meta_key BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_meta_origem BIGINT NOT NULL UNIQUE,
    data_key INT NOT NULL,
    representante_key INT NOT NULL,
    valor_meta DECIMAL(14,2) NOT NULL,
    CONSTRAINT fk_metas_data FOREIGN KEY (data_key) REFERENCES dim_data(data_key),
    CONSTRAINT fk_metas_representante FOREIGN KEY (representante_key) REFERENCES dim_representante(representante_key)
);

CREATE TABLE fato_estoque (
    estoque_key BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_estoque_origem BIGINT NOT NULL,
    data_key INT NOT NULL,
    filial_key INT NOT NULL,
    produto_key INT NOT NULL,
    estoque_atual DECIMAL(12,3) NOT NULL,
    estoque_minimo DECIMAL(12,3) NOT NULL,
    estoque_maximo DECIMAL(12,3) NOT NULL,
    valor_estoque DECIMAL(16,2) NOT NULL,
    CONSTRAINT uq_snapshot_estoque UNIQUE (data_key, filial_key, produto_key),
    CONSTRAINT fk_estoque_data FOREIGN KEY (data_key) REFERENCES dim_data(data_key),
    CONSTRAINT fk_estoque_filial FOREIGN KEY (filial_key) REFERENCES dim_filial(filial_key),
    CONSTRAINT fk_estoque_produto FOREIGN KEY (produto_key) REFERENCES dim_produto(produto_key)
);

CREATE INDEX idx_fato_vendas_data ON fato_vendas(data_key);
CREATE INDEX idx_fato_vendas_cliente ON fato_vendas(cliente_key);
CREATE INDEX idx_fato_vendas_produto ON fato_vendas(produto_key);
CREATE INDEX idx_fato_vendas_representante ON fato_vendas(representante_key);
CREATE INDEX idx_fato_vendas_filial ON fato_vendas(filial_key);
CREATE INDEX idx_fato_metas_data_rep ON fato_metas(data_key, representante_key);
CREATE INDEX idx_fato_estoque_data_filial ON fato_estoque(data_key, filial_key);
