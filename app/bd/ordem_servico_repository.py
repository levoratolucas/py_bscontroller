from app.bd.conexao import Conexao
from app.model.ordem_servico import OrdemServico

class OrdemServicoRepository:
    def __init__(self):
        self.con = Conexao()

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
            concluida BOOLEAN,
            data_conclusao TEXT,
            FOREIGN KEY (id_tecnico) REFERENCES tecnicos (id_tecnico),
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
             ordem_servico.observacoes, ordem_servico.data_criacao, ordem_servico.concluida, 
             ordem_servico.data_conclusao)
        )

        conn.commit()
        conn.close()

    def listar(self):
        conn = self.con.conectar()
        c = conn.cursor()

        c.execute("SELECT * FROM ordem_servico")
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
            concluida=row[9],
            data_conclusao=row[10]
        ) for row in dados]