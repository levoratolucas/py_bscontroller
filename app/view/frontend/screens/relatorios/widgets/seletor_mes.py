import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from app.view.frontend.styles import COLORS, FONTS

class SeletorMesDialog:
    def __init__(self, parent, callback):
        self.parent = parent
        self.callback = callback
        self.dialog = None
        self.meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
                     "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        self.abrir()
    
    def abrir(self):
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title("Selecionar Período")
        self.dialog.geometry("400x250")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Centralizar
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (250 // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            frame,
            text="Selecione o Mês e Ano",
            font=FONTS['title'],
            text_color=COLORS['primary']
        ).pack(pady=(0, 20))
        
        # Mês
        ctk.CTkLabel(frame, text="Mês:", font=FONTS['subtitle']).pack(anchor="w")
        self.mes_combo = ctk.CTkComboBox(frame, values=self.meses, width=200)
        self.mes_combo.pack(pady=(5, 15))
        self.mes_combo.set(self.meses[datetime.now().month - 1])
        
        # Ano
        ctk.CTkLabel(frame, text="Ano:", font=FONTS['subtitle']).pack(anchor="w")
        ano_atual = datetime.now().year
        anos = [str(ano_atual - 2), str(ano_atual - 1), str(ano_atual), str(ano_atual + 1)]
        self.ano_combo = ctk.CTkComboBox(frame, values=anos, width=200)
        self.ano_combo.pack(pady=(5, 20))
        self.ano_combo.set(str(ano_atual))
        
        # Botões
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        ctk.CTkButton(btn_frame, text="Confirmar", fg_color=COLORS['success'], 
                     command=self.confirmar).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Cancelar", fg_color=COLORS['danger'], 
                     command=self.fechar).pack(side="left", padx=5)
    
    def confirmar(self):
        mes = self.mes_combo.get()
        ano = self.ano_combo.get()
        mes_numero = self.meses.index(mes) + 1
        
        self.callback(mes_numero, int(ano))
        self.fechar()
    
    def fechar(self):
        if self.dialog:
            self.dialog.destroy()