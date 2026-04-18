import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

class PopupAnalise:
    def __init__(self, parent, dados_os, repetido_controller, callback_atualizar, mes_referencia=None):
        """
        Popup para análise de repetido
        
        Parâmetros:
            parent: widget pai
            dados_os: {
                'os_selecionada': {...},
                'os_referencia': {...}
            }
            repetido_controller: instância do RepetidoController
            callback_atualizar: função para recarregar dados após análise
            mes_referencia: mês de referência (se None, usa mês atual)
        """
        self.parent = parent
        self.os_selecionada = dados_os['os_selecionada']
        self.os_referencia = dados_os['os_referencia']
        self.repetido_controller = repetido_controller
        self.callback_atualizar = callback_atualizar
        self.mes_referencia = mes_referencia if mes_referencia else datetime.now().strftime("%Y-%m")
        self.dialog = None
        
        self.abrir()
    
    def abrir(self):
        # Criar popup
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title("Análise de Repetido")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        frame = ctk.CTkFrame(self.dialog, fg_color="#0a0a0a")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            frame,
            text="🔁 Analisar Repetido",
            font=('Arial', 18, 'bold'),
            text_color="#ff6b00"
        ).pack(pady=(0, 15))
        
        # Informações - usar grid para melhor controle
        info_frame = ctk.CTkFrame(frame, fg_color="#1a1a2e", corner_radius=10)
        info_frame.pack(fill="x", pady=5)
        
        # Usar grid para organizar as informações
        info_frame.grid_columnconfigure(0, weight=1)
        info_frame.grid_columnconfigure(1, weight=1)
        
        # Cabeçalho da tabela
        ctk.CTkLabel(
            info_frame, 
            text="🔴 OS REPETIDA", 
            font=('Arial', 12, 'bold'), 
            text_color="#ff6666"
        ).grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        
        ctk.CTkLabel(
            info_frame, 
            text="🟢 OS REFERÊNCIA", 
            font=('Arial', 12, 'bold'), 
            text_color="#66ff66"
        ).grid(row=0, column=1, padx=10, pady=(10, 5), sticky="w")
        
        # WAN/Piloto (linha 1)
        ctk.CTkLabel(
            info_frame, 
            text=f"WAN: {self.os_selecionada.get('wan_piloto', '-')}", 
            font=('Arial', 11), 
            text_color="#cccccc"
        ).grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="w")
        
        # Número (linha 2)
        ctk.CTkLabel(
            info_frame, 
            text=f"Nº: {self.os_selecionada.get('numero', '-')}", 
            font=('Arial', 11), 
            text_color="#ffffff"
        ).grid(row=2, column=0, padx=10, pady=2, sticky="w")
        
        ctk.CTkLabel(
            info_frame, 
            text=f"Nº: {self.os_referencia.get('numero', '-')}", 
            font=('Arial', 11), 
            text_color="#ffffff"
        ).grid(row=2, column=1, padx=10, pady=2, sticky="w")
        
        # Data (linha 3)
        ctk.CTkLabel(
            info_frame, 
            text=f"Data: {self.os_selecionada.get('data', '-')} {self.os_selecionada.get('inicio_execucao', '-')}", 
            font=('Arial', 11), 
            text_color="#aaaaaa"
        ).grid(row=3, column=0, padx=10, pady=2, sticky="w")
        
        ctk.CTkLabel(
            info_frame, 
            text=f"Data: {self.os_referencia.get('data', '-')} {self.os_referencia.get('inicio_execucao', '-')}", 
            font=('Arial', 11), 
            text_color="#aaaaaa"
        ).grid(row=3, column=1, padx=10, pady=2, sticky="w")
        
        # Técnico (linha 4)
        ctk.CTkLabel(
            info_frame, 
            text=f"Técnico: {self.os_selecionada.get('tecnico', '-')}", 
            font=('Arial', 11), 
            text_color="#aaaaaa"
        ).grid(row=4, column=0, padx=10, pady=(2, 10), sticky="w")
        
        ctk.CTkLabel(
            info_frame, 
            text=f"Técnico: {self.os_referencia.get('tecnico', '-')}", 
            font=('Arial', 11), 
            text_color="#aaaaaa"
        ).grid(row=4, column=1, padx=10, pady=(2, 10), sticky="w")
        
        # Mês de referência (info)
        ctk.CTkLabel(
            info_frame,
            text=f"📅 Mês Referência: {self.mes_referencia}",
            font=('Arial', 10, 'italic'),
            text_color="#ffaa00"
        ).grid(row=5, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="w")
        
        # Separador
        ctk.CTkFrame(frame, height=1, fg_color="#2a2a2a").pack(fill="x", pady=10)
        
        # Pergunta
        ctk.CTkLabel(
            frame,
            text="Esta repetição PROCEDE?",
            font=('Arial', 14, 'bold'),
            text_color="#ffffff"
        ).pack(pady=10)
        
        # Botões
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        ctk.CTkButton(
            btn_frame,
            text="✅ PROCEDE",
            fg_color="#00cc66",
            hover_color="#009944",
            font=('Arial', 13, 'bold'),
            width=120,
            command=self.on_procede
        ).pack(side="left", padx=8)
        
        ctk.CTkButton(
            btn_frame,
            text="❌ NÃO PROCEDE",
            fg_color="#ff3333",
            hover_color="#cc0000",
            font=('Arial', 13, 'bold'),
            width=120,
            command=self.on_nao_procede
        ).pack(side="left", padx=8)
        
        ctk.CTkButton(
            btn_frame,
            text="⏳ CANCELAR",
            fg_color="#555555",
            hover_color="#333333",
            font=('Arial', 13, 'bold'),
            width=120,
            command=self.fechar
        ).pack(side="left", padx=8)
        
        # Forçar atualização do tamanho do diálogo
        self.dialog.update_idletasks()
        
        # Calcular tamanho ideal baseado no conteúdo
        largura = frame.winfo_reqwidth() + 40
        altura = frame.winfo_reqheight() + 40
        
        # Garantir tamanho mínimo
        largura = max(largura, 500)
        altura = max(altura, 350)
        
        self.dialog.geometry(f"{largura}x{altura}")
        
        # Centralizar
        x = (self.dialog.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (altura // 2)
        self.dialog.geometry(f"+{x}+{y}")
    
    def on_procede(self):
        """Salva como PROCEDE"""
        self.repetido_controller.salvar_repetido(
            id_os=self.os_selecionada.get('id_os'),
            id_os_referencia=self.os_referencia.get('id_os'),
            procedente=1,
            mes_referencia=self.mes_referencia
        )
        messagebox.showinfo("Sucesso", "Repetido marcado como PROCEDE!")
        self.fechar()
        if self.callback_atualizar:
            self.callback_atualizar()
    
    def on_nao_procede(self):
        """Salva como NÃO PROCEDE"""
        self.repetido_controller.salvar_repetido(
            id_os=self.os_selecionada.get('id_os'),
            id_os_referencia=self.os_referencia.get('id_os'),
            procedente=2,
            mes_referencia=self.mes_referencia
        )
        messagebox.showinfo("Sucesso", "Repetido marcado como NÃO PROCEDE!")
        self.fechar()
        if self.callback_atualizar:
            self.callback_atualizar()
    
    def fechar(self):
        if self.dialog:
            self.dialog.destroy()