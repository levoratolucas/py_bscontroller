from app.bd.conexao import Conexao

class Database:
    def __init__(self):
        self.con = Conexao()
        self.criar_tabelas()
    
    def criar_tabelas(self):
        conn = self.con.conectar()
        c = conn.cursor()
        
        # Tabela de técnicos
        c.execute("""
        CREATE TABLE IF NOT EXISTS tecnicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            matricula TEXT NOT NULL
        )
        """)
        
        # Tabela de OS
        c.execute("""
        CREATE TABLE IF NOT EXISTS ordem_servico (
            id_os INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT NOT NULL ,
            id_tecnico INTEGER,
            wan_piloto TEXT,
            carimbo TEXT,
            tipo INTEGER DEFAULT 2,
            status INTEGER DEFAULT 1,
            data_criacao TEXT,
            data TEXT,
            inicio_execucao TEXT,
            fim_execucao TEXT,
            FOREIGN KEY (id_tecnico) REFERENCES tecnicos (id)
        )
        """)
        
        # Tabela de repetidos
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
        print("✅ Tabelas criadas/verificadas com sucesso!")