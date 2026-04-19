from app.view.frontend.screens.relatorios.popup_analise import PopupAnalise
from datetime import datetime

class EventoController:
    def __init__(self, parent, repetido_controller, relatorio_controller, 
                 os_controller, aplicar_filtro_callback):
        """
        Controlador de eventos da tabela
        
        Parâmetros:
            parent: widget pai (para popups)
            repetido_controller: controlador de repetidos
            relatorio_controller: controlador de relatórios
            os_controller: controlador de OS
            aplicar_filtro_callback: função para recarregar dados
        """
        self.parent = parent
        self.repetido_controller = repetido_controller
        self.relatorio_controller = relatorio_controller
        self.os_controller = os_controller
        self.aplicar_filtro_callback = aplicar_filtro_callback
        self.dados_atuais = []
        self.obter_periodo_callback = None
    
    def set_dados(self, dados):
        """Define os dados atuais da tabela"""
        self.dados_atuais = dados
    
    def set_obter_periodo_callback(self, callback):
        """Define callback para obter período atual"""
        self.obter_periodo_callback = callback
    
    def on_selecionar(self, valores):
        """Callback ao selecionar uma linha na tabela"""
        if not valores:
            return
        
        # Buscar a OS selecionada nos dados
        os_selecionada = None
        for os in self.dados_atuais:
            if str(os.get('numero')) == str(valores[0]):
                os_selecionada = os
                break
        
        if not os_selecionada:
            return
        
        data_inicio, data_fim = self.obter_periodo_callback() if self.obter_periodo_callback else (None, None)
        is_pendente = os_selecionada.get('pendente', False)
        
        if is_pendente:
            # Buscar OS de referência para pendentes
            wan = os_selecionada.get('wan_piloto')
            os_referencia = self.relatorio_controller.get_os_anterior(
                wan, 
                os_selecionada.get('data'), 
                os_selecionada.get('inicio_execucao', '00:00'),
                data_inicio, 
                data_fim
            )
            
            carimbo = self._buscar_carimbo(os_selecionada.get('numero'))
            texto_selecionada = f"📝 CARIMBO:\n{carimbo}"
            
            if os_referencia:
                carimbo_ref = self._buscar_carimbo(os_referencia.get('numero'))
                texto_referencia = f"📌 OS: {os_referencia['numero']} | 👤 {os_referencia['tecnico']} | 📅 {os_referencia['data']}\n\n📝 CARIMBO:\n{carimbo_ref}"
            else:
                texto_referencia = "Nenhuma OS de referência encontrada"
        else:
            # OS já analisada
            carimbo = os_selecionada.get('carimbo_repetido', 'Carimbo não disponível')
            texto_selecionada = f"📝 CARIMBO:\n{carimbo}"
            
            if os_selecionada.get('numero_referencia'):
                texto_referencia = f"📌 OS: {os_selecionada.get('numero_referencia', '-')} | 👤 {os_selecionada.get('tecnico_referencia', '-')} | 📅 {os_selecionada.get('data_referencia', '-')}\n\n📝 CARIMBO:\n{os_selecionada.get('carimbo_referencia', 'Carimbo não disponível')}"
            else:
                texto_referencia = "Nenhuma OS de referência encontrada"
        
        return texto_selecionada, texto_referencia
    
    def on_duplo_clique(self, valores):
        """Callback ao dar duplo clique na tabela"""
        if not valores:
            return
        
        # Buscar a OS selecionada
        os_selecionada = None
        for os in self.dados_atuais:
            if str(os.get('numero')) == str(valores[0]):
                os_selecionada = os
                break
        
        if not os_selecionada:
            return
        
        # Verificar se é pendente
        if not os_selecionada.get('pendente', False):
            from tkinter import messagebox
            messagebox.showwarning("Aviso", "Esta OS já foi analisada! Apenas OS pendentes podem ser analisadas.")
            return
        
        if not os_selecionada.get('id_os'):
            return
        
        data_inicio, data_fim = self.obter_periodo_callback() if self.obter_periodo_callback else (None, None)
        wan = os_selecionada.get('wan_piloto')
        
        os_referencia = self.relatorio_controller.get_os_anterior(
            wan, 
            os_selecionada.get('data'), 
            os_selecionada.get('inicio_execucao', '00:00'),
            data_inicio, 
            data_fim
        )
        
        if not os_referencia:
            return
        
        if not os_referencia.get('id_os'):
            return
        
        mes_referencia = datetime.strptime(data_inicio, "%Y-%m-%d").strftime("%Y-%m") if data_inicio else datetime.now().strftime("%Y-%m")
        
        # Abrir popup
        PopupAnalise(
            parent=self.parent,
            dados_os={
                'os_selecionada': os_selecionada,
                'os_referencia': os_referencia
            },
            repetido_controller=self.repetido_controller,
            callback_atualizar=self.aplicar_filtro_callback,
            mes_referencia=mes_referencia
        )
    
    def _buscar_carimbo(self, numero):
        """Busca o carimbo de uma OS pelo número"""
        os = self.os_controller.buscar_por_numero(numero)
        if os:
            return os['carimbo']
        return f"Carimbo não encontrado para OS {numero}"