import customtkinter as ctk
from app.view.frontend.styles import COLORS


class CardsOrdemServico:
    def __init__(self, parent):
        self.parent = parent
        self.card_esquerdo = None
        self.card_direito = None
        self.criar_cards()
    
    def criar_cards(self):
        main_container = ctk.CTkFrame(self.parent, fg_color="transparent")
        main_container.pack(fill="both", expand=True)
        
        # 2 colunas: 50% e 50%
        main_container.grid_columnconfigure(0, weight=50)
        main_container.grid_columnconfigure(1, weight=50)
        main_container.grid_rowconfigure(0, weight=1)
        
        # Card Esquerdo (50%)
        self.card_esquerdo = ctk.CTkFrame(main_container, fg_color="#0f0f0f", corner_radius=12, border_width=1, border_color="#2a2a2a")
        self.card_esquerdo.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)
        
        # Placeholder vazio
        placeholder_esq = ctk.CTkFrame(self.card_esquerdo, fg_color="#1a1a2e", corner_radius=12)
        placeholder_esq.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            placeholder_esq,
            text="📊",
            font=('Arial', 48),
            text_color="#666666"
        ).pack(pady=(50, 10))
        
        ctk.CTkLabel(
            placeholder_esq,
            text="EM DESENVOLVIMENTO",
            font=('Arial', 16, 'bold'),
            text_color="#ff6b00"
        ).pack()
        
        ctk.CTkLabel(
            placeholder_esq,
            text="Em breve...",
            font=('Arial', 12),
            text_color="#666666"
        ).pack(pady=(5, 50))
        
        # Card Direito (50%)
        self.card_direito = ctk.CTkFrame(main_container, fg_color="#0f0f0f", corner_radius=12, border_width=1, border_color="#2a2a2a")
        self.card_direito.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=0)
        
        # Placeholder vazio
        placeholder_dir = ctk.CTkFrame(self.card_direito, fg_color="#1a1a2e", corner_radius=12)
        placeholder_dir.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            placeholder_dir,
            text="📋",
            font=('Arial', 48),
            text_color="#666666"
        ).pack(pady=(50, 10))
        
        ctk.CTkLabel(
            placeholder_dir,
            text="EM DESENVOLVIMENTO",
            font=('Arial', 16, 'bold'),
            text_color="#ff6b00"
        ).pack()
        
        ctk.CTkLabel(
            placeholder_dir,
            text="Em breve...",
            font=('Arial', 12),
            text_color="#666666"
        ).pack(pady=(5, 50))
    
    def get_card_esquerdo(self):
        return self.card_esquerdo
    
    def get_card_direito(self):
        return self.card_direito