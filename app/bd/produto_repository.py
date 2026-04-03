from app.bd.conexao import Conexao
from app.model.produto import Produto

class ProdutoRepository:
    def __init__(self):
        self.con = Conexao()
        self.criar_tabela()  # ← Adicionar esta linha

    def criar_tabela(self):
        conn = self.con.conectar()
        c = conn.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT,
            designador TEXT,
            wan_piloto TEXT,
            id_cliente_endereco INTEGER,
            FOREIGN KEY (id_cliente_endereco) REFERENCES cliente_endereco (id)
        )
        """)

        conn.commit()
        conn.close()

    def inserir(self, produto):
        conn = self.con.conectar()
        c = conn.cursor()

        c.execute(
            "INSERT INTO produtos (descricao, designador, wan_piloto, id_cliente_endereco) VALUES (?, ?, ?, ?)",
            (produto.descricao, produto.designador, produto.wan_piloto, produto.id_cliente_endereco)
        )
        
        # Pegar o ID gerado
        produto.id_produto = c.lastrowid

        conn.commit()
        conn.close()
        
        return produto

    def listar(self):
        conn = self.con.conectar()
        c = conn.cursor()

        c.execute("SELECT * FROM produtos")
        dados = c.fetchall()

        conn.close()

        return [Produto(id=row[0], descricao=row[1], designador=row[2], wan_piloto=row[3], id_cliente_endereco=row[4]) for row in dados]
    
    def buscar_por_id(self, id_produto):
        conn = self.con.conectar()
        c = conn.cursor()
        
        c.execute("SELECT * FROM produtos WHERE id = ?", (id_produto,))
        row = c.fetchone()
        
        conn.close()
        
        if row:
            return Produto(id=row[0], descricao=row[1], designador=row[2], wan_piloto=row[3], id_cliente_endereco=row[4])
        return None