from datetime import datetime

class Formatador:
    """Funções de formatação de dados"""
    
    @staticmethod
    def formatar_data(data_str, formato_entrada="%Y-%m-%d", formato_saida="%d/%m/%Y"):
        """Formata uma data de um formato para outro"""
        try:
            dt = datetime.strptime(data_str, formato_entrada)
            return dt.strftime(formato_saida)
        except (ValueError, TypeError):
            return data_str
    
    @staticmethod
    def formatar_data_hora(data_str, hora_str, formato_saida="%d/%m/%Y %H:%M"):
        """Formata data e hora juntas"""
        try:
            datetime_str = f"{data_str} {hora_str}:00"
            dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            return dt.strftime(formato_saida)
        except (ValueError, TypeError):
            return f"{data_str} {hora_str}"
    
    @staticmethod
    def formatar_wan(wan_str, limite=20):
        """Formata o WAN/Piloto para exibição"""
        if not wan_str:
            return "-"
        if len(wan_str) > limite:
            return wan_str[:limite] + "..."
        return wan_str
    
    @staticmethod
    def formatar_status(status, tipo="texto"):
        """Formata o status para exibição"""
        if tipo == "texto":
            return "Concluído" if status == 1 else "Suspenso"
        elif tipo == "icone":
            return "✅" if status == 1 else "❌"
        return str(status)
    
    @staticmethod
    def formatar_tipo(tipo):
        """Formata o tipo de OS para exibição"""
        tipos = {1: "Apoio", 2: "Reparo", 3: "Ativação"}
        return tipos.get(tipo, "Desconhecido")
    
    @staticmethod
    def formatar_tempo(horas):
        """Formata horas para exibição (ex: 2.5 horas -> 2h30)"""
        if horas is None:
            return "-"
        horas_int = int(horas)
        minutos = int((horas - horas_int) * 60)
        if minutos > 0:
            return f"{horas_int}h{minutos:02d}"
        return f"{horas_int}h"