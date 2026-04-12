from datetime import datetime

class OrdemServico:
    def __init__(self, numero, id_tecnico, wan_piloto=None, carimbo=None, 
                 tipo=2, status=1, data_criacao=None, data=None, 
                 inicio_execucao=None, fim_execucao=None, id_os=None):
        self.id_os = id_os
        self.numero = numero
        self.id_tecnico = id_tecnico
        self.wan_piloto = wan_piloto
        self.carimbo = carimbo
        self.tipo = tipo
        self.status = status
        self.data_criacao = data_criacao if data_criacao else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.data = data
        self.inicio_execucao = inicio_execucao
        self.fim_execucao = fim_execucao
    
    def __str__(self):
        status_texto = "Concluído" if self.status == 1 else "Suspenso"
        tipo_texto = {1: "Apoio", 2: "Reparo", 3: "Ativação"}.get(self.tipo, "Reparo")
        return f"OS {self.numero} - {tipo_texto} - {status_texto}"