from app.bd.conexao import Conexao
from app.model.cliente import Cliente

class ClienteRepository:
    def __init__(self):
        self.con = Conexao()

    def criar_tabela(self):
        conn = self.con.conectar()
        c = conn.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT
        )
        """)

        conn.commit()
        conn.close()

    def inserir(self, cliente):
        conn = self.con.conectar()
        c = conn.cursor()

        c.execute(
            "INSERT INTO clientes (nome) VALUES (?)",
            (cliente.nome,)
        )

        conn.commit()
        conn.close()

    def listar(self):
        conn = self.con.conectar()
        c = conn.cursor()

        c.execute("SELECT * FROM clientes")
        dados = c.fetchall()

        conn.close()

        return [Cliente(row[1], id=row[0]) for row in dados]