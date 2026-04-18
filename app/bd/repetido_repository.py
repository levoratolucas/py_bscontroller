from app.bd.conexao import Conexao
from app.model.repetido import Repetido

class RepetidoRepository:
    def __init__(self):
        self.con = Conexao()
        self.criar_tabela()
    
    def criar_tabela(self):
        conn = self.con.conectar()
        c = conn.cursor()
        
        c.execute("""
        CREATE TABLE IF NOT EXISTS repetidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_os INTEGER NOT NULL,
            procedente INTEGER NOT NULL,
            carimbo_referencia TEXT NOT NULL,
            carimbo_repetido TEXT NOT NULL,
            mes_referencia TEXT NOT NULL
        )
        """)
        
        conn.commit()
        conn.close()
    
    def inserir(self, repetido):
        conn = self.con.conectar()
        c = conn.cursor()
        
        c.execute("""
            INSERT INTO repetidos (id_os, procedente, carimbo_referencia, carimbo_repetido, mes_referencia)
            VALUES (?, ?, ?, ?, ?)
        """, (repetido.id_os, repetido.procedente, 
              repetido.carimbo_referencia, repetido.carimbo_repetido, repetido.mes_referencia))
        
        repetido.id = c.lastrowid
        conn.commit()
        conn.close()
        
        return repetido
    
    def listar(self):
        conn = self.con.conectar()
        c = conn.cursor()
        
        c.execute("SELECT * FROM repetidos")
        dados = c.fetchall()
        
        conn.close()
        
        return [Repetido(
            id=row[0],
            id_os=row[1],
            procedente=row[2],
            carimbo_referencia=row[3],
            carimbo_repetido=row[4],
            mes_referencia=row[5]
        ) for row in dados]
    
    def buscar_por_id_os(self, id_os):
        conn = self.con.conectar()
        c = conn.cursor()
        
        c.execute("SELECT * FROM repetidos WHERE id_os = ?", (id_os,))
        row = c.fetchone()
        
        conn.close()
        
        if row:
            return Repetido(
                id=row[0],
                id_os=row[1],
                procedente=row[2],
                carimbo_referencia=row[3],
                carimbo_repetido=row[4],
                mes_referencia=row[5]
            )
        return None
    
    def buscar_por_mes_referencia(self, mes_referencia):
        """Busca registros por mês de referência"""
        conn = self.con.conectar()
        c = conn.cursor()
        
        c.execute("SELECT * FROM repetidos WHERE mes_referencia = ?", (mes_referencia,))
        dados = c.fetchall()
        
        conn.close()
        
        return [Repetido(
            id=row[0],
            id_os=row[1],
            procedente=row[2],
            carimbo_referencia=row[3],
            carimbo_repetido=row[4],
            mes_referencia=row[5]
        ) for row in dados]
    
    def deletar(self, id_os):
        conn = self.con.conectar()
        c = conn.cursor()
        
        c.execute("DELETE FROM repetidos WHERE id_os = ?", (id_os,))
        
        conn.commit()
        conn.close()