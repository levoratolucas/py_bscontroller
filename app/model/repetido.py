# app/model/repetido.py
class Repetido:
    def __init__(self, id_os, id_os_referencia, mes_referencia, procedente=0, id=None):
        self.id = id
        self.id_os = id_os
        self.id_os_referencia = id_os_referencia
        self.procedente = procedente  # 0 = pendente, 1 = procede, 2 = não procede
        self.mes_referencia = mes_referencia
    
    def __str__(self):
        status = {0: "Pendente", 1: "Procede", 2: "Não Procede"}
        return f"Repetido {self.id}: OS {self.id_os} → Referência {self.id_os_referencia} ({status.get(self.procedente, 'Desconhecido')})"