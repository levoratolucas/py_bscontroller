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

    # def inserir(self, cliente):
    #     conn = self.con.conectar()
    #     c = conn.cursor()
        
    #     c.execute("SELECT ID FROM clientes WHERE nome = ?", (cliente.nome,))
    #     existente = c.fetchone()
        
    #     if existente is None:

    #         c.execute(
    #             "INSERT INTO clientes (nome) VALUES (?)",
    #             (cliente.nome,)
    #         )

    #         conn.commit()
    #         conn.close()
    #         return "cliente inserido com sucesso"
    #     else:
    #         conn.close()
    #         return "\n CLIENTE JA CADASTRADO"

    def listar(self):
        conn = self.con.conectar()
        c = conn.cursor()

        c.execute("SELECT * FROM clientes")
        dados = c.fetchall()

        conn.close()

        return [Cliente(row[1], id=row[0]) for row in dados]
    
    def inserir_cliente(self, nome):
        cliente = Cliente(nome=nome, id_cliente=None)
        self.repo.inserir(cliente)
        # Buscar o cliente recém-inserido para retornar com ID
        clientes = self.repo.listar()
        for c in clientes:
            if c.nome == nome:  # Pode não ser único, ideal seria retornar o último ID
                return c
        return None
    
    def inserir(self, cliente):
        conn = self.con.conectar()
        c = conn.cursor()
        
        c.execute(
            "INSERT INTO clientes (nome) VALUES (?)",
            (cliente.nome,)
        )
        
        # Pegar o ID gerado
        cliente.id_cliente = c.lastrowid
        
        conn.commit()
        conn.close()
        
        return cliente


