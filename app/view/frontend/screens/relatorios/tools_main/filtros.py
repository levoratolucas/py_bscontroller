from datetime import datetime, timedelta

class FiltroHelper:
    """Gerencia a lógica de filtros de período"""
    
    @staticmethod
    def get_periodo_mes(mes_numero, ano):
        """Retorna data_inicio e data_fim do mês"""
        primeiro_dia = datetime(ano, mes_numero, 1)
        
        if mes_numero == 12:
            ultimo_dia = datetime(ano + 1, 1, 1) - timedelta(days=1)
        else:
            ultimo_dia = datetime(ano, mes_numero + 1, 1) - timedelta(days=1)
        
        return primeiro_dia.strftime("%Y-%m-%d"), ultimo_dia.strftime("%Y-%m-%d")
    
    @staticmethod
    def get_periodo_producao(periodos, nome_periodo):
        """Retorna data_inicio e data_fim de um período de produção"""
        for p in periodos:
            if p['nome'] == nome_periodo:
                return p['inicio'], p['fim']
        return None, None
    
    @staticmethod
    def get_id_tecnico_por_nome(tecnicos, nome):
        """Retorna o ID do técnico pelo nome"""
        for t in tecnicos:
            if t['nome'] == nome:
                return t['id']
        return None
    
    @staticmethod
    def get_nome_tecnico_por_id(tecnicos, id_tecnico):
        """Retorna o nome do técnico pelo ID"""
        for t in tecnicos:
            if t['id'] == id_tecnico:
                return t['nome']
        return None