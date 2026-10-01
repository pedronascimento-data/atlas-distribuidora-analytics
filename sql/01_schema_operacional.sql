-- ============================================================
-- ATLAS DISTRIBUIDORA ANALYTICS
-- 01 - SCHEMA OPERACIONAL
-- Banco alvo: MySQL 8+
-- Autor: Pedro Nascimento
-- ============================================================

DROP DATABASE IF EXISTS atlas_distribuidora;
CREATE DATABASE atlas_distribuidora
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE atlas_distribuidora;

-- ============================================================
-- GEOGRAFIA E FILIAIS
-- ============================================================

CREATE TABLE estado (
    id_estado INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(60) NOT NULL,
    uf CHAR(2) NOT NULL UNIQUE
);

CREATE TABLE cidade (
    id_cidade INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    id_estado INT NOT NULL,
    CONSTRAINT uq_cidade_estado UNIQUE (nome, id_estado),
    CONSTRAINT fk_cidade_estado
        FOREIGN KEY (id_estado) REFERENCES estado(id_estado)
);

CREATE TABLE filial (
    id_filial INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(10) NOT NULL UNIQUE,
    nome VARCHAR(100) NOT NULL,
    id_cidade INT NOT NULL,
    ativa BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT fk_filial_cidade
        FOREIGN KEY (id_cidade) REFERENCES cidade(id_cidade)
);

-- ============================================================
-- ESTRUTURA COMERCIAL
-- ============================================================

CREATE TABLE gerente (
    id_gerente INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(20) NOT NULL UNIQUE,
    nome VARCHAR(120) NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE supervisor (
    id_supervisor INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(20) NOT NULL UNIQUE,
    nome VARCHAR(120) NOT NULL,
    id_gerente INT NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT fk_supervisor_gerente
        FOREIGN KEY (id_gerente) REFERENCES gerente(id_gerente)
);

CREATE TABLE representante (
    id_representante INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(20) NOT NULL UNIQUE,
    nome VARCHAR(120) NOT NULL,
    id_supervisor INT NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT fk_representante_supervisor
        FOREIGN KEY (id_supervisor) REFERENCES supervisor(id_supervisor)
);

-- ============================================================
-- CLIENTES
-- ============================================================

CREATE TABLE cliente (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(20) NOT NULL UNIQUE,
    razao_social VARCHAR(150) NOT NULL,
    nome_fantasia VARCHAR(150),
    documento VARCHAR(18) UNIQUE,
    id_cidade INT NOT NULL,
    id_representante INT NOT NULL,
    status ENUM('ATIVO', 'INATIVO', 'BLOQUEADO') NOT NULL DEFAULT 'ATIVO',
    data_cadastro DATE NOT NULL,
    CONSTRAINT fk_cliente_cidade
        FOREIGN KEY (id_cidade) REFERENCES cidade(id_cidade),
    CONSTRAINT fk_cliente_representante
        FOREIGN KEY (id_representante) REFERENCES representante(id_representante)
);

-- ============================================================
-- PRODUTOS E FORNECEDORES
-- ============================================================

CREATE TABLE categoria (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE marca (
    id_marca INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE fornecedor (
    id_fornecedor INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(20) NOT NULL UNIQUE,
    razao_social VARCHAR(150) NOT NULL,
    nome_fantasia VARCHAR(150),
    documento VARCHAR(18) UNIQUE,
    ativo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE produto (
    id_produto INT AUTO_INCREMENT PRIMARY KEY,
    sku VARCHAR(30) NOT NULL UNIQUE,
    descricao VARCHAR(180) NOT NULL,
    id_categoria INT NOT NULL,
    id_marca INT NOT NULL,
    id_fornecedor INT NOT NULL,
    custo_atual DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    preco_atual DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT chk_produto_custo CHECK (custo_atual >= 0),
    CONSTRAINT chk_produto_preco CHECK (preco_atual >= 0),
    CONSTRAINT fk_produto_categoria
        FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria),
    CONSTRAINT fk_produto_marca
        FOREIGN KEY (id_marca) REFERENCES marca(id_marca),
    CONSTRAINT fk_produto_fornecedor
        FOREIGN KEY (id_fornecedor) REFERENCES fornecedor(id_fornecedor)
);

-- ============================================================
-- PEDIDOS
-- ============================================================

CREATE TABLE pedido (
    id_pedido BIGINT AUTO_INCREMENT PRIMARY KEY,
    numero_pedido VARCHAR(30) NOT NULL UNIQUE,
    data_pedido DATETIME NOT NULL,
    data_faturamento DATETIME,
    id_cliente INT NOT NULL,
    id_representante INT NOT NULL,
    id_filial INT NOT NULL,
    status ENUM(
        'EM_DIGITACAO',
        'APROVADO',
        'FATURADO',
        'CANCELADO',
        'ENTREGUE'
    ) NOT NULL DEFAULT 'EM_DIGITACAO',
    valor_frete DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    valor_desconto DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    CONSTRAINT chk_pedido_frete CHECK (valor_frete >= 0),
    CONSTRAINT chk_pedido_desconto CHECK (valor_desconto >= 0),
    CONSTRAINT fk_pedido_cliente
        FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
    CONSTRAINT fk_pedido_representante
        FOREIGN KEY (id_representante) REFERENCES representante(id_representante),
    CONSTRAINT fk_pedido_filial
        FOREIGN KEY (id_filial) REFERENCES filial(id_filial)
);

CREATE TABLE pedido_item (
    id_pedido_item BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_pedido BIGINT NOT NULL,
    id_produto INT NOT NULL,
    quantidade DECIMAL(12,3) NOT NULL,
    preco_unitario DECIMAL(12,2) NOT NULL,
    custo_unitario DECIMAL(12,2) NOT NULL,
    desconto_item DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    CONSTRAINT uq_pedido_produto UNIQUE (id_pedido, id_produto),
    CONSTRAINT chk_item_quantidade CHECK (quantidade > 0),
    CONSTRAINT chk_item_preco CHECK (preco_unitario >= 0),
    CONSTRAINT chk_item_custo CHECK (custo_unitario >= 0),
    CONSTRAINT chk_item_desconto CHECK (desconto_item >= 0),
    CONSTRAINT fk_item_pedido
        FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido)
        ON DELETE CASCADE,
    CONSTRAINT fk_item_produto
        FOREIGN KEY (id_produto) REFERENCES produto(id_produto)
);

-- ============================================================
-- ESTOQUE
-- ============================================================

CREATE TABLE estoque (
    id_estoque BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_filial INT NOT NULL,
    id_produto INT NOT NULL,
    estoque_atual DECIMAL(12,3) NOT NULL DEFAULT 0,
    estoque_minimo DECIMAL(12,3) NOT NULL DEFAULT 0,
    estoque_maximo DECIMAL(12,3) NOT NULL DEFAULT 0,
    atualizado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT uq_estoque_filial_produto UNIQUE (id_filial, id_produto),
    CONSTRAINT chk_estoque_atual CHECK (estoque_atual >= 0),
    CONSTRAINT chk_estoque_minimo CHECK (estoque_minimo >= 0),
    CONSTRAINT chk_estoque_maximo CHECK (estoque_maximo >= estoque_minimo),
    CONSTRAINT fk_estoque_filial
        FOREIGN KEY (id_filial) REFERENCES filial(id_filial),
    CONSTRAINT fk_estoque_produto
        FOREIGN KEY (id_produto) REFERENCES produto(id_produto)
);

-- ============================================================
-- METAS
-- ============================================================

CREATE TABLE meta_representante (
    id_meta BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_representante INT NOT NULL,
    competencia DATE NOT NULL,
    valor_meta DECIMAL(14,2) NOT NULL,
    CONSTRAINT uq_meta_representante_mes
        UNIQUE (id_representante, competencia),
    CONSTRAINT chk_meta_valor CHECK (valor_meta > 0),
    CONSTRAINT chk_meta_competencia
        CHECK (DAY(competencia) = 1),
    CONSTRAINT fk_meta_representante
        FOREIGN KEY (id_representante) REFERENCES representante(id_representante)
);

-- ============================================================
-- ÍNDICES PARA CONSULTAS FREQUENTES
-- ============================================================

CREATE INDEX idx_cliente_representante
    ON cliente (id_representante);

CREATE INDEX idx_pedido_data_status
    ON pedido (data_pedido, status);

CREATE INDEX idx_pedido_faturamento
    ON pedido (data_faturamento);

CREATE INDEX idx_pedido_cliente
    ON pedido (id_cliente);

CREATE INDEX idx_pedido_representante
    ON pedido (id_representante);

CREATE INDEX idx_item_produto
    ON pedido_item (id_produto);

CREATE INDEX idx_meta_competencia
    ON meta_representante (competencia);

-- ============================================================
-- FIM DO SCHEMA
-- ============================================================
