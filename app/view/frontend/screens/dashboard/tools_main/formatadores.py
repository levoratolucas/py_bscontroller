class FormatadorDashboard:
    """Funções de formatação para o dashboard"""
    
    @staticmethod
    def formatar_nome_tecnico(nome, limite=25):
        """Formata nome do técnico para exibição"""
        if len(nome) > limite:
            return nome[:limite-3] + "..."
        return nome
    
    @staticmethod
    def formatar_info_tecnico(tecnico):
        """Formata informações adicionais do técnico"""
        return f"Total OS: {tecnico['total_os']} | Concluídos: {tecnico['concluidos']} | TMR: {tecnico['tmr']}h"
    
    @staticmethod
    def get_cor_por_valor(valor, max_valor=None):
        """Retorna cor baseada no valor"""
        from app.view.frontend.styles import COLORS
        if max_valor:
            percentual = (valor / max_valor) * 100
            if percentual >= 80:
                return COLORS['success']
            elif percentual >= 50:
                return COLORS['warning']
            return COLORS['danger']
        return COLORS['primary']