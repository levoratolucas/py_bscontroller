from app.bd.conexao import Conexao
from app.model.endereco import Endereco

class EnderecoRepository:
    def __init__(self):
        self.con = Conexao()

    def criar_tabela(self):
        conn = self.con.conectar()
        c = conn.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS enderecos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            logradouro TEXT,
            cidade TEXT,
            estado TEXT
        )
        """)

        conn.commit()
        conn.close()

    def inserir(self, endereco):
        conn = self.con.conectar()
        c = conn.cursor()

        c.execute(
            "INSERT INTO enderecos (logradouro, cidade, estado) VALUES (?, ?, ?)",
            (endereco.logradouro, endereco.cidade, endereco.estado)
        )

        conn.commit()
        conn.close()

    def listar(self):
        conn = self.con.conectar()
        c = conn.cursor()

        c.execute("SELECT * FROM enderecos")
        dados = c.fetchall()

        conn.close()

        return [Endereco(id=row[0], logradouro=row[1], cidade=row[2], estado=row[3]) for row in dados]