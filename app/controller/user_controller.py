from app.bd.user_repository import UserRepository
from app.model.user_model import User

class UserController:
    def __init__(self):
        self.repo = UserRepository()
        self.repo.criar_tabela()

    def criar_usuario_padrao(self):
        usuarios = self.repo.listar()
        if not usuarios:
            user = User("Lucas Levorato", 31, "Masculino")
            self.repo.inserir(user)

    def listar(self):
        return self.repo.listar()
