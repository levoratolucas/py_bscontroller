class MetricasHelper:
    """Funções para cálculo de métricas"""
    
    @staticmethod
    def calcular_percentual_ofensor(metricas):
        """Calcula percentual de ofensor para cada técnico"""
        for m in metricas:
            total_tecnico = m.get('total_os', 0)
            ofensor = m.get('ofensor', 0)
            percentual = round((ofensor / total_tecnico * 100), 1) if total_tecnico > 0 else 0
            m['percentual_ofensor'] = percentual
        return metricas
    
    @staticmethod
    def calcular_media_apu(metricas):
        """Calcula média geral de APU"""
        apu_validos = [m.get('apu', 0) for m in metricas if m.get('apu', 0) > 0]
        return round(sum(apu_validos) / len(apu_validos), 2) if apu_validos else 0
    
    @staticmethod
    def calcular_total_repeticoes(metricas):
        """Calcula total de repetições e percentual"""
        total_repeticoes = sum(m.get('ofensor', 0) for m in metricas)
        return total_repeticoes
    
    @staticmethod
    def calcular_percentual_repeticoes(total_repeticoes, total_os):
        """Calcula percentual de repetições sobre total de OS"""
        return round((total_repeticoes / total_os * 100), 1) if total_os > 0 else 0