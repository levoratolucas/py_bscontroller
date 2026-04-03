import os
import sys

# -------------------------
# DEFAULT USER
# -------------------------
DEFAULT_NOME = "Lucas Levorato"
DEFAULT_IDADE = 31
DEFAULT_SEXO = "Masculino"

# -------------------------
# ESTRUTURA
# -------------------------
BASE_ESTRUTURA = {
    "app": ["model", "view", "controller", "bd"]
}

ARQUIVOS_BASE = [
    "main.py",
    "app/model/__init__.py",
    "app/view/__init__.py",
    "app/controller/__init__.py",
    "app/bd/__init__.py"
]

# -------------------------
# DADOS USUÁRIO
# -------------------------
def obter_dados():
    if len(sys.argv) == 4:
        nome = sys.argv[1]
        idade = int(sys.argv[2])
        sexo = sys.argv[3]
    else:
        nome = DEFAULT_NOME
        idade = DEFAULT_IDADE
        sexo = DEFAULT_SEXO

    return nome, idade, sexo

# -------------------------
# CRIAR PASTAS
# -------------------------
def criar_pastas(base):
    for pasta, subs in BASE_ESTRUTURA.items():
        for sub in subs:
            os.makedirs(os.path.join(base, pasta, sub), exist_ok=True)

# -------------------------
# CRIAR ARQUIVOS BASE
# -------------------------
def criar_arquivos_base(base):
    for arq in ARQUIVOS_BASE:
        caminho = os.path.join(base, arq)
        with open(caminho, "w") as f:
            f.write("")

# -------------------------
# CONEXÃO DB
# -------------------------
def criar_conexao(base):
    conteudo = '''import sqlite3

class Conexao:
    def __init__(self, db_name="banco.db"):
        self.db_name = db_name

    def conectar(self):
        return sqlite3.connect(self.db_name)
'''
    path = os.path.join(base, "app/bd/conexao.py")
    with open(path, "w") as f:
        f.write(conteudo)

# -------------------------
# MODEL
# -------------------------
def criar_model(base):
    conteudo = '''class User:
    def __init__(self, nome, idade, sexo, id=None):
        self.id = id
        self.nome = nome
        self.idade = idade
        self.sexo = sexo
'''
    path = os.path.join(base, "app/model/user_model.py")
    with open(path, "w") as f:
        f.write(conteudo)

# -------------------------
# REPOSITORY
# -------------------------
def criar_repository(base):
    conteudo = '''from app.bd.conexao import Conexao
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
'''
    path = os.path.join(base, "app/bd/user_repository.py")
    with open(path, "w") as f:
        f.write(conteudo)

# -------------------------
# CONTROLLER
# -------------------------
def criar_controller(base, nome, idade, sexo):
    conteudo = f'''from app.bd.user_repository import UserRepository
from app.model.user_model import User

class UserController:
    def __init__(self):
        self.repo = UserRepository()
        self.repo.criar_tabela()

    def criar_usuario_padrao(self):
        usuarios = self.repo.listar()
        if not usuarios:
            user = User("{nome}", {idade}, "{sexo}")
            self.repo.inserir(user)

    def listar(self):
        return self.repo.listar()
'''
    path = os.path.join(base, "app/controller/user_controller.py")
    with open(path, "w") as f:
        f.write(conteudo)

# -------------------------
# VIEW
# -------------------------
def criar_view(base):
    conteudo = '''class UserView:
    def mostrar(self, usuarios):
        for u in usuarios:
            print(f"Bom dia {u.nome}! Idade: {u.idade} Sexo: {u.sexo}")
'''
    path = os.path.join(base, "app/view/user_view.py")
    with open(path, "w") as f:
        f.write(conteudo)

# -------------------------
# MAIN
# -------------------------
def criar_main(base):
    conteudo = '''from app.controller.user_controller import UserController
from app.view.user_view import UserView

def main():
    controller = UserController()
    view = UserView()

    controller.criar_usuario_padrao()
    usuarios = controller.listar()

    view.mostrar(usuarios)

if __name__ == "__main__":
    main()
'''
    path = os.path.join(base, "main.py")
    with open(path, "w") as f:
        f.write(conteudo)

# -------------------------
# EXECUÇÃO
# -------------------------
if __name__ == "__main__":
    base = os.getcwd()

    nome, idade, sexo = obter_dados()

    criar_pastas(base)
    criar_arquivos_base(base)
    criar_conexao(base)
    criar_model(base)
    criar_repository(base)
    criar_controller(base, nome, idade, sexo)
    criar_view(base)
    criar_main(base)

    print("🚀 Projeto MVC criado com sucesso!")
    print(f"👤 Usuário padrão: {nome}")
    print("👉 Execute: python main.py")