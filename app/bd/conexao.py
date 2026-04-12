import sqlite3
import os

class Conexao:
    def __init__(self, banco='sistema.db'):
        # Garantir que o banco seja criado na raiz do projeto
        self.banco = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), banco)
    
    def conectar(self):
        return sqlite3.connect(self.banco)