class Endereco:
    def __init__(self,  logradouro, cidade, estado,id = None):
        self.id_endereco = id
        self.logradouro = logradouro
        self.cidade = cidade
        self.estado = estado