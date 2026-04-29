import customtkinter as ctk
from app.view.frontend.styles import COLORS, FONTS

class CardOS:
    def __init__(self, parent, col):
        self.parent = parent
        self.col = col
        self.card = None
        self.labels = {}
        self.criar_card()
    
    def criar_card(self):
        self.card = ctk.CTkFrame(self.parent, fg_color=COLORS['bg_card'], corner_radius=12, 
                                  border_width=1, border_color=COLORS['border'])
        self.card.grid(row=0, column=self.col, sticky="nsew", padx=5, pady=5)
        
        ctk.CTkLabel(self.card, text="📋 ORDEM DE SERVIÇO", font=FONTS['subtitle'], 
                     text_color=COLORS['primary']).pack(anchor="w", padx=15, pady=(10, 5))
        
        self.labels['total'] = ctk.CTkLabel(self.card, text="TOTAL: 0", font=('Arial', 28, 'bold'), 
                                             text_color=COLORS['primary'])
        self.labels['total'].pack(anchor="w", padx=15, pady=(0, 10))
        
        # Ativação
        self.labels['ativacao'] = self._criar_linha_tipo("🚀 ATIVAÇÃO:", "ativacao")
        
        # Reparo
        self.labels['reparo'] = self._criar_linha_tipo("🔧 REPARO:", "reparo")
        
        # Apoio
        self.labels['apoio'] = self._criar_linha_tipo("🛟 APOIO:", "apoio")
    
    def _criar_linha_tipo(self, texto, prefixo):
        frame = ctk.CTkFrame(self.card, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=2)
        
        ctk.CTkLabel(frame, text=texto, font=FONTS['normal'], width=90).pack(side="left")
        
        total_label = ctk.CTkLabel(frame, text="0", font=FONTS['normal'], width=30)
        total_label.pack(side="left")
        
        ok_label = ctk.CTkLabel(frame, text=" ✅ OK: 0", font=FONTS['small'], text_color=COLORS['success'])
        ok_label.pack(side="left", padx=(5, 0))
        
        pend_label = ctk.CTkLabel(frame, text=" ⏸️ Pend: 0", font=FONTS['small'], text_color=COLORS['warning'])
        pend_label.pack(side="left", padx=(5, 0))
        
        return {'total': total_label, 'ok': ok_label, 'pend': pend_label}
    
    def atualizar(self, stats):
        total = stats.get('total', 0)
        self.labels['total'].configure(text=f"TOTAL: {total}")
        
        self._atualizar_linha('ativacao', stats.get('ativacao', 0), 
                               stats.get('ativacao_concluidos', 0), stats.get('ativacao_suspensos', 0))
        self._atualizar_linha('reparo', stats.get('reparo', 0), 
                               stats.get('reparo_concluidos', 0), stats.get('reparo_suspensos', 0))
        self._atualizar_linha('apoio', stats.get('apoio', 0), 
                               stats.get('apoio_concluidos', 0), stats.get('apoio_suspensos', 0))
    
    def _atualizar_linha(self, prefixo, total, ok, pend):
        self.labels[prefixo]['total'].configure(text=str(total))
        self.labels[prefixo]['ok'].configure(text=f" ✅ OK: {ok}")
        self.labels[prefixo]['pend'].configure(text=f" ⏸️ Pend: {pend}")
    
    def get_frame(self):
        return self.card