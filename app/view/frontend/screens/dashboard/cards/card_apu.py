import customtkinter as ctk
from app.view.frontend.styles import COLORS, FONTS

class CardAPU:
    def __init__(self, parent, col):
        self.parent = parent
        self.col = col
        self.card = None
        self.labels = {}
        self.ranking_labels = []
        self.criar_card()
    
    def criar_card(self):
        self.card = ctk.CTkFrame(self.parent, fg_color=COLORS['bg_card'], corner_radius=12, 
                                  border_width=1, border_color=COLORS['border'])
        self.card.grid(row=0, column=self.col, sticky="nsew", padx=5, pady=5)
        
        ctk.CTkLabel(self.card, text="⚡ APU", font=FONTS['subtitle'], 
                     text_color=COLORS['success']).pack(anchor="w", padx=15, pady=(10, 5))
        
        self.labels['media'] = ctk.CTkLabel(self.card, text="MÉDIA GERAL: 0,0", font=('Arial', 22, 'bold'), 
                                             text_color=COLORS['success'])
        self.labels['media'].pack(anchor="w", padx=15, pady=(0, 10))
        
        ranking_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        ranking_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        for i in range(3):
            label = ctk.CTkLabel(ranking_frame, text="", font=FONTS['normal'], anchor="w")
            label.pack(fill="x", pady=5)
            self.ranking_labels.append(label)
    
    def atualizar(self, media_apu, ranking_apu, medalhas):
        self.labels['media'].configure(text=f"MÉDIA GERAL: {media_apu}")
        
        for i, label in enumerate(self.ranking_labels):
            if i < len(ranking_apu):
                ap = ranking_apu[i]
                label.configure(text=f"{medalhas[i]} {ap['tecnico']}: {ap.get('apu', 0)}")
            else:
                label.configure(text="")
    
    def get_frame(self):
        return self.card