import re
from datetime import datetime

class Validacoes:
    """Funções de validação de dados"""
    
    @staticmethod
    def validar_data(data_str, formato="%Y-%m-%d"):
        """Valida se a string é uma data válida"""
        try:
            datetime.strptime(data_str, formato)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validar_hora(hora_str):
        """Valida se a string é uma hora válida (HH:MM)"""
        padrao = re.compile(r'^([0-1][0-9]|2[0-3]):[0-5][0-9]$')
        return bool(padrao.match(hora_str))
    
    @staticmethod
    def validar_wan(wan_str):
        """Valida se o WAN/Piloto é válido (não vazio)"""
        return wan_str and wan_str.strip() != ""
    
    @staticmethod
    def validar_campos_obrigatorios(dados, campos):
        """Valida se todos os campos obrigatórios estão preenchidos"""
        for campo in campos:
            if not dados.get(campo):
                return False, f"Campo {campo} é obrigatório!"
        return True, ""
    
    @staticmethod
    def is_numero(valor):
        """Verifica se o valor é um número"""
        try:
            float(valor)
            return True
        except (ValueError, TypeError):
            return False