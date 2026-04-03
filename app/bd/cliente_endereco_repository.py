from app.bd.conexao import Conexao
from app.model.cliente_endereco import ClienteEndereco

class ClienteEnderecoRepository:
    def __init__(self):
        self.con = Conexao()

    def criar_tabela(self):
        conn = self.con.conectar()
        c = conn.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS cliente_endereco (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER,
            id_endereco INTEGER,
            FOREIGN KEY (id_cliente) REFERENCES clientes (id),
            FOREIGN KEY (id_endereco) REFERENCES enderecos (id)
        )
        """)

        conn.commit()
        conn.close()

    def inserir(self, cliente_endereco):
        conn = self.con.conectar()
        c = conn.cursor()

        c.execute(
            "INSERT INTO cliente_endereco (id_cliente, id_endereco) VALUES (?, ?)",
            (cliente_endereco.id_cliente, cliente_endereco.id_endereco)
        )

        conn.commit()
        conn.close()

    def listar(self):
        conn = self.con.conectar()
        c = conn.cursor()

        c.execute("SELECT * FROM cliente_endereco")
        dados = c.fetchall()

        conn.close()

        return [ClienteEndereco(id=row[0], id_cliente=row[1], id_endereco=row[2]) for row in dados]