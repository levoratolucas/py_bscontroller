class RankingsHelper:
    """Funções para rankings de técnicos"""
    
    @staticmethod
    def ranking_ofensores(metricas, limite=3):
        """Retorna ranking dos técnicos com maior percentual de ofensor"""
        ofensores = sorted(metricas, key=lambda x: x.get('percentual_ofensor', 0), reverse=True)
        return ofensores[:limite]
    
    @staticmethod
    def ranking_apu(metricas, limite=3):
        """Retorna ranking dos técnicos com menor APU (melhores)"""
        apu_lista = sorted(metricas, key=lambda x: x.get('apu', 999))
        return apu_lista[:limite]
    
    @staticmethod
    def medalhas():
        """Retorna lista de emojis de medalhas"""
        return ["🥇", "🥈", "🥉"]
    
    @staticmethod
    def formatar_ranking_item(medalha, tecnico, valor, unidade="", sufixo=""):
        """Formata um item do ranking"""
        if valor > 0:
            return f"{medalha} {tecnico}: {valor}{unidade}{sufixo}"
        return f"{medalha} {tecnico}: 0%"