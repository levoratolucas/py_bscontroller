import customtkinter as ctk
from app.view.frontend.styles import COLORS


class BotoesOrdemServico:
    def __init__(self, parent, on_todos_click=None, on_ativacao_click=None, 
                 on_reparo_click=None, on_apu_click=None):
        self.parent = parent
        self.botoes = {}
        self.on_todos_click = on_todos_click
        self.on_ativacao_click = on_ativacao_click
        self.on_reparo_click = on_reparo_click
        self.on_apu_click = on_apu_click
        self.criar_botoes()
    
    def criar_botoes(self):
        botoes_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        botoes_frame.pack(fill="x", pady=(0, 25))
        
        for i in range(4):
            botoes_frame.grid_columnconfigure(i, weight=1)
        
        # Botão 1 - TODOS
        btn1 = ctk.CTkFrame(botoes_frame, fg_color="#1a1a2e", corner_radius=12, 
                            border_width=1, border_color="#ff6b00", cursor="hand2")
        btn1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        btn1.bind("<Button-1>", lambda e: self.on_todos_click() if self.on_todos_click else None)
        
        ctk.CTkLabel(btn1, text="📋", font=('Arial', 28), text_color="#ff6b00").pack(pady=(10, 5))
        ctk.CTkLabel(btn1, text="TODOS", font=('Arial', 12, 'bold'), text_color="#ffffff").pack()
        
        self.todos_valor = ctk.CTkLabel(btn1, text="0", font=('Arial', 18, 'bold'), text_color="#ff6b00")
        self.todos_valor.pack(pady=(5, 10))
        self.botoes['todos'] = btn1
        
        # Botão 2 - ATIVAÇÃO
        btn2 = ctk.CTkFrame(botoes_frame, fg_color="#1a1a2e", corner_radius=12, 
                            border_width=1, border_color="#0088ff", cursor="hand2")
        btn2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        btn2.bind("<Button-1>", lambda e: self.on_ativacao_click() if self.on_ativacao_click else None)
        
        ctk.CTkLabel(btn2, text="🚀", font=('Arial', 28), text_color="#0088ff").pack(pady=(10, 5))
        ctk.CTkLabel(btn2, text="ATIVAÇÃO", font=('Arial', 12, 'bold'), text_color="#ffffff").pack()
        
        self.ativacao_valor = ctk.CTkLabel(btn2, text="0", font=('Arial', 18, 'bold'), text_color="#0088ff")
        self.ativacao_valor.pack(pady=(5, 10))
        self.botoes['ativacao'] = btn2
        
        # Botão 3 - REPARO
        btn3 = ctk.CTkFrame(botoes_frame, fg_color="#1a1a2e", corner_radius=12, 
                            border_width=1, border_color="#00cc66", cursor="hand2")
        btn3.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        btn3.bind("<Button-1>", lambda e: self.on_reparo_click() if self.on_reparo_click else None)
        
        ctk.CTkLabel(btn3, text="🔧", font=('Arial', 28), text_color="#00cc66").pack(pady=(10, 5))
        ctk.CTkLabel(btn3, text="REPARO", font=('Arial', 12, 'bold'), text_color="#ffffff").pack()
        
        self.reparo_valor = ctk.CTkLabel(btn3, text="0", font=('Arial', 18, 'bold'), text_color="#00cc66")
        self.reparo_valor.pack(pady=(5, 10))
        self.botoes['reparo'] = btn3
        
        # Botão 4 - APU
        btn4 = ctk.CTkFrame(botoes_frame, fg_color="#1a1a2e", corner_radius=12, 
                            border_width=1, border_color="#ff3333", cursor="hand2")
        btn4.grid(row=0, column=3, sticky="nsew", padx=5, pady=5)
        btn4.bind("<Button-1>", lambda e: self.on_apu_click() if self.on_apu_click else None)
        
        ctk.CTkLabel(btn4, text="📊", font=('Arial', 28), text_color="#ff3333").pack(pady=(10, 5))
        ctk.CTkLabel(btn4, text="APU", font=('Arial', 12, 'bold'), text_color="#ffffff").pack()
        
        self.apu_valor_label = ctk.CTkLabel(btn4, text="0.0", font=('Arial', 18, 'bold'), text_color="#ff3333")
        self.apu_valor_label.pack(pady=(5, 10))
        self.botoes['apu'] = btn4
    
    def set_valores(self, todos, ativacao, reparo):
        """Atualiza os valores nos botões"""
        self.todos_valor.configure(text=str(todos))
        self.ativacao_valor.configure(text=str(ativacao))
        self.reparo_valor.configure(text=str(reparo))
    
    def set_apu_valor(self, valor):
        self.apu_valor_label.configure(text=f"{valor}")