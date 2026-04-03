from app.bd.conexao import Conexao
from app.model.user_model import User

class UserRepository:
    def __init__(self):
        self.con = Conexao()

    def criar_tabela(self):
        conn = self.con.conectar()
        c = conn.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            idade INTEGER,
            sexo TEXT
        )
        """)

        conn.commit()
        conn.close()

    def inserir(self, user):
        conn = self.con.conectar()
        c = conn.cursor()

        c.execute(
            "INSERT INTO users (nome, idade, sexo) VALUES (?, ?, ?)",
            (user.nome, user.idade, user.sexo)
        )

        conn.commit()
        conn.close()

    def listar(self):
        conn = self.con.conectar()
        c = conn.cursor()

        c.execute("SELECT * FROM users")
        dados = c.fetchall()

        conn.close()

        return [User(id=row[0], nome=row[1], idade=row[2], sexo=row[3]) for row in dados]
