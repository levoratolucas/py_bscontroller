import sqlite3

class Conexao:
    def __init__(self, db_name="banco2.db"):
        self.db_name = db_name

    def conectar(self):
        return sqlite3.connect(self.db_name)
