-- Script para criar o banco catalogo-produtos.db (SQLite)
-- Uso: sqlite3 db/catalogo-produtos.db < db/setup-catalogo.sql

CREATE TABLE IF NOT EXISTS produtos (
    id       INTEGER PRIMARY KEY,
    nome     TEXT    NOT NULL,
    categoria TEXT   NOT NULL,
    ativo    INTEGER NOT NULL DEFAULT 1
);

INSERT INTO produtos (id, nome, categoria, ativo) VALUES
 (1, 'Dipirona 500mg',          'Analgésico',      1),
 (2, 'Paracetamol 750mg',       'Analgésico',      1),
 (3, 'Soro Fisiológico 250ml',  'Solução',         1),
 (4, 'Vitamina C 1g',           'Suplemento',      1),
 (5, 'Protetor Solar FPS 60',   'Dermocosmético',  0); -- descontinuado: ativo = 0

-- Produto id=5 está INATIVO de propósito.
-- Usado no Bloco 3 para demonstrar o log de aviso quando o agente
-- tenta devolver estoque de um produto que não existe mais no catálogo.
