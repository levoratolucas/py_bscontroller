import customtkinter as ctk
from app.view.frontend.styles import COLORS, FONTS

class CardRepetidos:
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
        
        ctk.CTkLabel(self.card, text="🔄 REPETIDOS", font=FONTS['subtitle'], 
                     text_color=COLORS['warning']).pack(anchor="w", padx=15, pady=(10, 5))
        
        self.labels['total'] = ctk.CTkLabel(self.card, text="TOTAL: 0", font=('Arial', 24, 'bold'), 
                                             text_color=COLORS['warning'])
        self.labels['total'].pack(anchor="w", padx=15, pady=(0, 5))
        
        self.labels['percent'] = ctk.CTkLabel(self.card, text="", font=FONTS['normal'], 
                                               text_color=COLORS['text_secondary'])
        self.labels['percent'].pack(anchor="w", padx=15, pady=(0, 10))
        
        ranking_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        ranking_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        for i in range(3):
            label = ctk.CTkLabel(ranking_frame, text="", font=FONTS['normal'], anchor="w")
            label.pack(fill="x", pady=5)
            self.ranking_labels.append(label)
    
    def atualizar(self, total_repeticoes, percentual, ranking_ofensores, medalhas):
        self.labels['total'].configure(text=f"TOTAL: {total_repeticoes}  ({percentual}% do total)")
        
        for i, label in enumerate(self.ranking_labels):
            if i < len(ranking_ofensores):
                of = ranking_ofensores[i]
                percentual_of = of.get('percentual_ofensor', 0)
                if percentual_of > 0:
                    label.configure(text=f"{medalhas[i]} {of['tecnico']}: {percentual_of}% ({of.get('ofensor', 0)} repetições)")
                else:
                    label.configure(text=f"{medalhas[i]} {of['tecnico']}: 0%")
            else:
                label.configure(text="")
    
    def get_frame(self):
        return self.card