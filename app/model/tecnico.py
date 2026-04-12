class Tecnico:
    def __init__(self, nome, matricula, id=None):
        self.id = id
        self.nome = nome
        self.matricula = matricula
    
    def __str__(self):
        return f"{self.id} - {self.nome} ({self.matricula})"