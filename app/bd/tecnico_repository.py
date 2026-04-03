from app.bd.conexao import Conexao
from app.model.tecnico import Tecnico

class TecnicoRepository:
    def __init__(self):
        self.con = Conexao()

    def criar_tabela(self):
        conn = self.con.conectar()
        c = conn.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS tecnicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            matricula TEXT
        )
        """)

        conn.commit()
        conn.close()

    def inserir(self, tecnico):
        conn = self.con.conectar()
        c = conn.cursor()

        # verifica se já existe pela matrícula
        c.execute("SELECT id FROM tecnicos WHERE matricula = ?", (tecnico.matricula,))
        existente = c.fetchone()

        if existente is None:
            c.execute(
                "INSERT INTO tecnicos (nome, matricula) VALUES (?, ?)",
                (tecnico.nome, tecnico.matricula)
            )
            conn.commit()
            tecnico.id = c.lastrowid
            conn.close()
            return "Técnico inserido com sucesso"
        else:
            tecnico.id = existente[0]  # já existente
            conn.close()
            return "\nJA EXISTE ESSE TECNICO"

        

    def listar(self):
        conn = self.con.conectar()
        c = conn.cursor()

        c.execute("SELECT * FROM tecnicos")
        dados = c.fetchall()

        conn.close()

        return [Tecnico(id=row[0], nome=row[1], matricula=row[2]) for row in dados]