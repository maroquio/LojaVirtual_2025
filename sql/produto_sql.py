CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS produto (
id INTEGER PRIMARY KEY AUTOINCREMENT,
nome TEXT NOT NULL,
descricao TEXT NOT NULL,
preco REAL NOT NULL,
quantidade INTEGER NOT NULL,
categoria_id INTEGER NOT NULL,
FOREIGN KEY (categoria_id) REFERENCES categoria(id))
"""

INSERIR = """
INSERT INTO produto (nome, descricao, preco, quantidade, categoria_id) 
VALUES (?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT 
p.id, p.nome, p.descricao, p.preco, p.quantidade, 
COALESCE(p.categoria_id, 1) as categoria_id, 
COALESCE(c.nome, 'Sem Categoria') as categoria_nome 
FROM produto p
LEFT JOIN categoria c ON p.categoria_id = c.id
ORDER BY p.nome
""" 

OBTER_POR_ID = """
SELECT 
p.id, p.nome, p.descricao, p.preco, p.quantidade, 
COALESCE(p.categoria_id, 1) as categoria_id, 
COALESCE(c.nome, 'Sem Categoria') as categoria_nome 
FROM produto p
LEFT JOIN categoria c ON p.categoria_id = c.id
WHERE p.id = ?
""" 

EXCLUIR_POR_ID = """
DELETE FROM produto WHERE id = ?
"""

ALTERAR = """
UPDATE produto 
SET nome = ?, descricao = ?, preco = ?, quantidade = ?, categoria_id = ?
WHERE id = ?
"""

ALTERAR_TABELA_ADD_CATEGORIA = """
ALTER TABLE produto ADD COLUMN categoria_id INTEGER REFERENCES categoria(id)
"""