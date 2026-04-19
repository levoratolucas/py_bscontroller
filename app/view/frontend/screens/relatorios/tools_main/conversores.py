from datetime import datetime, timedelta

class Conversor:
    """Funções de conversão de dados"""
    
    @staticmethod
    def str_para_datetime(data_str, hora_str="00:00"):
        """Converte string para datetime"""
        try:
            datetime_str = f"{data_str} {hora_str}:00"
            return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def calcular_diferenca_dias(data1, data2):
        """Calcula a diferença em dias entre duas datas"""
        try:
            if isinstance(data1, str):
                data1 = datetime.strptime(data1, "%Y-%m-%d")
            if isinstance(data2, str):
                data2 = datetime.strptime(data2, "%Y-%m-%d")
            return abs((data2 - data1).days)
        except (ValueError, TypeError):
            return 0
    
    @staticmethod
    def calcular_tempo_total(data_inicio, hora_inicio, data_fim, hora_fim):
        """Calcula o tempo total entre duas datas/horas em horas"""
        try:
            dt_inicio = datetime.strptime(f"{data_inicio} {hora_inicio}:00", "%Y-%m-%d %H:%M:%S")
            dt_fim = datetime.strptime(f"{data_fim} {hora_fim}:00", "%Y-%m-%d %H:%M:%S")
            return (dt_fim - dt_inicio).total_seconds() / 3600
        except (ValueError, TypeError):
            return 0
    
    @staticmethod
    def mes_para_numero(mes_nome, meses_lista):
        """Converte nome do mês para número"""
        try:
            return meses_lista.index(mes_nome) + 1
        except ValueError:
            return None
    
    @staticmethod
    def numero_para_mes(mes_numero, meses_lista):
        """Converte número do mês para nome"""
        try:
            return meses_lista[mes_numero - 1]
        except IndexError:
            return None