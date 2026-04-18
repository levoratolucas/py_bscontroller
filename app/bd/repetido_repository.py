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
            id_os_referencia INTEGER NOT NULL,
            procedente INTEGER DEFAULT 0,
            mes_referencia TEXT NOT NULL,
            FOREIGN KEY (id_os) REFERENCES ordem_servico (id_os),
            FOREIGN KEY (id_os_referencia) REFERENCES ordem_servico (id_os)
        )
        """)
        
        conn.commit()
        conn.close()
    
    def inserir(self, repetido):
        conn = self.con.conectar()
        c = conn.cursor()
        
        # Verificar se os IDs não são None
        if repetido.id_os is None:
            print("ERRO: id_os é None!")
            conn.close()
            return None
        
        if repetido.id_os_referencia is None:
            print("ERRO: id_os_referencia é None!")
            conn.close()
            return None
        
        # Verificar se já existe para evitar duplicidade
        c.execute("""
            SELECT id FROM repetidos 
            WHERE id_os = ? AND id_os_referencia = ?
        """, (repetido.id_os, repetido.id_os_referencia))
        
        if c.fetchone():
            conn.close()
            return repetido
        
        c.execute("""
            INSERT INTO repetidos (id_os, id_os_referencia, procedente, mes_referencia)
            VALUES (?, ?, ?, ?)
        """, (repetido.id_os, repetido.id_os_referencia, repetido.procedente, repetido.mes_referencia))
        
        repetido.id = c.lastrowid
        conn.commit()
        conn.close()
        
        return repetido
    
    def listar(self):
        conn = self.con.conectar()
        c = conn.cursor()
        
        c.execute("SELECT * FROM repetidos ORDER BY mes_referencia DESC, id DESC")
        dados = c.fetchall()
        
        conn.close()
        
        return [Repetido(
            id=row[0],
            id_os=row[1],
            id_os_referencia=row[2],
            procedente=row[3],
            mes_referencia=row[4]
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
                id_os_referencia=row[2],
                procedente=row[3],
                mes_referencia=row[4]
            )
        return None
    
    def buscar_por_mes_referencia(self, mes_referencia):
        """Busca registros por mês de referência"""
        conn = self.con.conectar()
        c = conn.cursor()
        
        c.execute("SELECT * FROM repetidos WHERE mes_referencia = ? ORDER BY id DESC", (mes_referencia,))
        dados = c.fetchall()
        
        conn.close()
        
        return [Repetido(
            id=row[0],
            id_os=row[1],
            id_os_referencia=row[2],
            procedente=row[3],
            mes_referencia=row[4]
        ) for row in dados]
    
    def atualizar_procedente(self, id_repetido, procedente):
        """Atualiza o status de procedência"""
        conn = self.con.conectar()
        c = conn.cursor()
        
        c.execute("UPDATE repetidos SET procedente = ? WHERE id = ?", (procedente, id_repetido))
        
        conn.commit()
        conn.close()
    
    def deletar_por_id_os(self, id_os):
        conn = self.con.conectar()
        c = conn.cursor()
        
        c.execute("DELETE FROM repetidos WHERE id_os = ?", (id_os,))
        
        conn.commit()
        conn.close()
    
    def limpar_todos(self):
        """Remove todos os registros da tabela"""
        conn = self.con.conectar()
        c = conn.cursor()
        
        c.execute("DELETE FROM repetidos")
        
        conn.commit()
        conn.close()
    
    def get_ids_os_analisados(self):
        """Retorna os IDs das OS que já foram analisadas"""
        conn = self.con.conectar()
        c = conn.cursor()
        c.execute("SELECT DISTINCT id_os FROM repetidos")
        dados = c.fetchall()
        conn.close()
        return [row[0] for row in dados]
    
    
    
    