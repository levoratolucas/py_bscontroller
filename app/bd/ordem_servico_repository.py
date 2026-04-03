from app.bd.conexao import Conexao
from app.model.ordem_servico import OrdemServico
from datetime import datetime

class OrdemServicoRepository:
    def __init__(self):
        self.con = Conexao()
        self.criar_tabela()

    def criar_tabela(self):
        conn = self.con.conectar()
        c = conn.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS ordem_servico (
            id_os INTEGER PRIMARY KEY AUTOINCREMENT,
            id_tecnico INTEGER,
            id_produto INTEGER,
            causa_raiz TEXT,
            materiais_utilizados TEXT,
            acao TEXT,
            contato_responsavel TEXT,
            observacoes TEXT,
            data_criacao TEXT,
            concluida INTEGER,
            data_conclusao TEXT,
            FOREIGN KEY (id_tecnico) REFERENCES tecnicos (id),
            FOREIGN KEY (id_produto) REFERENCES produtos (id)
        )
        """)

        conn.commit()
        conn.close()

    def inserir(self, ordem_servico):
        conn = self.con.conectar()
        c = conn.cursor()

        c.execute(
            """INSERT INTO ordem_servico 
               (id_tecnico, id_produto, causa_raiz, materiais_utilizados, acao, 
                contato_responsavel, observacoes, data_criacao, concluida, data_conclusao) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (ordem_servico.id_tecnico, ordem_servico.id_produto, ordem_servico.causa_raiz,
             ordem_servico.materiais_utilizados, ordem_servico.acao, ordem_servico.contato_responsavel,
             ordem_servico.observacoes, ordem_servico.data_criacao, 
             1 if ordem_servico.concluida else 0, 
             ordem_servico.data_conclusao)
        )

        ordem_servico.id_os = c.lastrowid
        conn.commit()
        conn.close()
        
        return ordem_servico

    def listar(self):
        conn = self.con.conectar()
        c = conn.cursor()

        c.execute("SELECT * FROM ordem_servico ORDER BY data_criacao DESC")
        dados = c.fetchall()

        conn.close()

        return [OrdemServico(
            id_os=row[0],
            id_tecnico=row[1],
            id_produto=row[2],
            causa_raiz=row[3],
            materiais_utilizados=row[4],
            acao=row[5],
            contato_responsavel=row[6],
            observacoes=row[7],
            data_criacao=row[8],
            concluida=bool(row[9]),
            data_conclusao=row[10]
        ) for row in dados]
    
    def buscar_por_id(self, id_os):
        conn = self.con.conectar()
        c = conn.cursor()
        
        c.execute("SELECT * FROM ordem_servico WHERE id_os = ?", (id_os,))
        row = c.fetchone()
        
        conn.close()
        
        if row:
            return OrdemServico(
                id_os=row[0],
                id_tecnico=row[1],
                id_produto=row[2],
                causa_raiz=row[3],
                materiais_utilizados=row[4],
                acao=row[5],
                contato_responsavel=row[6],
                observacoes=row[7],
                data_criacao=row[8],
                concluida=bool(row[9]),
                data_conclusao=row[10]
            )
        return None
    
    def atualizar_status(self, id_os, concluida, data_conclusao=None):
        conn = self.con.conectar()
        c = conn.cursor()
        
        c.execute(
            "UPDATE ordem_servico SET concluida = ?, data_conclusao = ? WHERE id_os = ?",
            (1 if concluida else 0, data_conclusao, id_os)
        )
        
        conn.commit()
        conn.close()
    
    def buscar_por_tecnico(self, id_tecnico):
        conn = self.con.conectar()
        c = conn.cursor()
        
        c.execute("SELECT * FROM ordem_servico WHERE id_tecnico = ? ORDER BY data_criacao DESC", (id_tecnico,))
        dados = c.fetchall()
        
        conn.close()
        
        return [OrdemServico(
            id_os=row[0],
            id_tecnico=row[1],
            id_produto=row[2],
            causa_raiz=row[3],
            materiais_utilizados=row[4],
            acao=row[5],
            contato_responsavel=row[6],
            observacoes=row[7],
            data_criacao=row[8],
            concluida=bool(row[9]),
            data_conclusao=row[10]
        ) for row in dados]
    
    def buscar_por_periodo(self, data_inicio, data_fim):
        """Buscar OS entre duas datas"""
        conn = self.con.conectar()
        c = conn.cursor()
        
        c.execute("""
            SELECT * FROM ordem_servico 
            WHERE data_criacao BETWEEN ? AND ? 
            ORDER BY data_criacao DESC
        """, (data_inicio, data_fim))
        
        dados = c.fetchall()
        conn.close()
        
        return [OrdemServico(
            id_os=row[0],
            id_tecnico=row[1],
            id_produto=row[2],
            causa_raiz=row[3],
            materiais_utilizados=row[4],
            acao=row[5],
            contato_responsavel=row[6],
            observacoes=row[7],
            data_criacao=row[8],
            concluida=bool(row[9]),
            data_conclusao=row[10]
        ) for row in dados]