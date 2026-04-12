from app.bd.conexao import Conexao
from app.bd.database import Database
from app.model.tecnico import Tecnico

class TecnicoController:
    def __init__(self):
        self.con = Conexao()
        self.db = Database()
    
    def listar(self):
        conn = self.con.conectar()
        c = conn.cursor()
        c.execute("SELECT id, nome, matricula FROM tecnicos ORDER BY nome")
        dados = c.fetchall()
        conn.close()
        return [Tecnico(id=row[0], nome=row[1], matricula=row[2]) for row in dados]
    
    def inserir(self, nome, matricula):
        conn = self.con.conectar()
        c = conn.cursor()
        c.execute("INSERT INTO tecnicos (nome, matricula) VALUES (?, ?)", (nome, matricula))
        id_tecnico = c.lastrowid
        conn.commit()
        conn.close()
        return Tecnico(id=id_tecnico, nome=nome, matricula=matricula)
    
    def buscar_por_nome(self, nome):
        conn = self.con.conectar()
        c = conn.cursor()
        c.execute("SELECT id, nome, matricula FROM tecnicos WHERE nome = ?", (nome,))
        row = c.fetchone()
        conn.close()
        if row:
            return Tecnico(id=row[0], nome=row[1], matricula=row[2])
        return None