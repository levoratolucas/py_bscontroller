import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta
from app.view.frontend.styles import COLORS, FONTS

class SeletorPeriodoDialog:
    def __init__(self, parent, callback):
        self.parent = parent
        self.callback = callback
        self.dialog = None
        self.periodos = self._get_periodos()
        self.abrir()
    
    def _get_periodos(self):
        """Retorna lista de períodos de produção (21 de um mês a 20 do próximo)"""
        periodos = []
        hoje = datetime.now()
        
        for i in range(12):
            data_fim = datetime(hoje.year, hoje.month, 1) - timedelta(days=i * 30)
            
            if data_fim.day >= 21:
                data_inicio = datetime(data_fim.year, data_fim.month, 21)
            else:
                if data_fim.month > 1:
                    data_inicio = datetime(data_fim.year, data_fim.month - 1, 21)
                else:
                    data_inicio = datetime(data_fim.year - 1, 12, 21)
            
            data_fim = data_inicio + timedelta(days=30)
            data_fim = datetime(data_fim.year, data_fim.month, 20)
            
            nome = f"{data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}"
            periodos.append({
                'nome': nome,
                'inicio': data_inicio.strftime("%Y-%m-%d"),
                'fim': data_fim.strftime("%Y-%m-%d")
            })
        
        return periodos
    
    def abrir(self):
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title("Selecionar Período de Produção")
        self.dialog.geometry("500x300")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Centralizar
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (300 // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            frame,
            text="Selecione o Período de Produção",
            font=FONTS['title'],
            text_color=COLORS['primary']
        ).pack(pady=(0, 20))
        
        # Período
        ctk.CTkLabel(frame, text="Período:", font=FONTS['subtitle']).pack(anchor="w")
        self.periodo_combo = ctk.CTkComboBox(frame, values=[p['nome'] for p in self.periodos], width=350)
        self.periodo_combo.pack(pady=(5, 20))
        self.periodo_combo.set(self.periodos[0]['nome'])
        
        # Botões
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        ctk.CTkButton(btn_frame, text="Confirmar", fg_color=COLORS['success'], 
                     command=self.confirmar).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Cancelar", fg_color=COLORS['danger'], 
                     command=self.fechar).pack(side="left", padx=5)
    
    def confirmar(self):
        nome = self.periodo_combo.get()
        periodo = None
        for p in self.periodos:
            if p['nome'] == nome:
                periodo = p
                break
        
        if periodo:
            self.callback(periodo['inicio'], periodo['fim'], nome)
        self.fechar()
    
    def fechar(self):
        if self.dialog:
            self.dialog.destroy()