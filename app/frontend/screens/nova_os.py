import customtkinter as ctk
from tkinter import messagebox
from app.frontend.styles import COLORS, FONTS


class NovaOsScreen(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)

        self.app = app

        self.setup_ui()

    def setup_ui(self):
        # ================= MAIN =================
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Título
        ctk.CTkLabel(
            main_frame,
            text="Nova Ordem de Serviço",
            font=FONTS['title'],
            text_color=COLORS['text_light']
        ).pack(pady=(0, 10))

        # ================= GRID PRINCIPAL =================
        grid_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True)

        grid_frame.grid_columnconfigure(0, weight=1)
        grid_frame.grid_columnconfigure(1, weight=1)
        grid_frame.grid_columnconfigure(2, weight=1)

        # ================= CARD CLIENTE =================
        self.criar_card_cliente(grid_frame)

        # ================= CARD PRODUTO =================
        self.criar_card_produto(grid_frame)

        # ================= CARD OS =================
        self.criar_card_os(grid_frame)

        # ================= STATUS =================
        self.criar_status(main_frame)

        # ================= BOTÕES =================
        self.criar_botoes(main_frame)

    # ================= CARDS =================

    def criar_card_base(self, parent, titulo, col):
        card = ctk.CTkFrame(
            parent,
            fg_color=COLORS['bg_card'],
            corner_radius=12,
            border_width=1,
            border_color=COLORS['border']
        )
        card.grid(row=0, column=col, sticky="nsew", padx=5, pady=5)

        ctk.CTkLabel(
            card,
            text=titulo,
            font=FONTS['subtitle'],
            text_color=COLORS['primary']
        ).pack(anchor="w", padx=15, pady=(10, 5))

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=15, pady=10)

        return content

    def input(self, parent, label):
        ctk.CTkLabel(parent, text=label, font=FONTS['small'],
                     text_color=COLORS['text_secondary']).pack(anchor="w")

        entry = ctk.CTkEntry(parent)
        entry.pack(fill="x", pady=(0, 10))

        return entry

    # ================= CLIENTE =================
    def criar_card_cliente(self, parent):
        content = self.criar_card_base(parent, "CLIENTE", 0)

        self.cliente = self.input(content, "Cliente")
        self.rua = self.input(content, "Endereço")
        self.cidade = self.input(content, "Cidade")
        self.estado = self.input(content, "Estado")

        self.tecnico = self.input(content, "Técnico")
        self.matricula = self.input(content, "Matrícula")

        self.contato = self.input(content, "Contato")
        self.telefone = self.input(content, "Telefone")

    # ================= PRODUTO =================
    def criar_card_produto(self, parent):
        content = self.criar_card_base(parent, "PRODUTO", 1)

        self.produto = self.input(content, "Produto")

        ctk.CTkLabel(content, text="Tipo", font=FONTS['small'],
                     text_color=COLORS['text_secondary']).pack(anchor="w")

        self.tipo_var = ctk.StringVar(value="Reparo")

        tipo_frame = ctk.CTkFrame(content, fg_color="transparent")
        tipo_frame.pack(anchor="w", pady=(0, 10))

        ctk.CTkRadioButton(tipo_frame, text="Reparo",
                           variable=self.tipo_var, value="Reparo").pack(side="left", padx=5)

        ctk.CTkRadioButton(tipo_frame, text="Ativação",
                           variable=self.tipo_var, value="Ativação").pack(side="left", padx=5)

        self.descricao = self.input(content, "Descrição")
        self.designador = self.input(content, "Designador")
        self.wan = self.input(content, "WAN/Piloto")

    # ================= OS =================
    def criar_card_os(self, parent):
        content = self.criar_card_base(parent, "DADOS DA OS", 2)

        self.numero_bd = self.input(content, "Nº do BD")
        self.causa = self.input(content, "Causa Raiz")
        self.materiais = self.input(content, "Materiais")
        self.acao = self.input(content, "Ação")

        ctk.CTkLabel(content, text="Observações",
                     font=FONTS['small'],
                     text_color=COLORS['text_secondary']).pack(anchor="w")

        self.obs = ctk.CTkTextbox(content, height=80)
        self.obs.pack(fill="x")

    # ================= STATUS =================
    def criar_status(self, parent):
        status_card = ctk.CTkFrame(
            parent,
            fg_color=COLORS['bg_card'],
            corner_radius=12,
            border_width=1,
            border_color=COLORS['border']
        )
        status_card.pack(fill="x", pady=(15, 10))

        ctk.CTkLabel(
            status_card,
            text="📅 STATUS E DATAS",
            font=FONTS['subtitle'],
            text_color=COLORS['primary']
        ).pack(anchor="w", padx=15, pady=(10, 5))

        content = ctk.CTkFrame(status_card, fg_color="transparent")
        content.pack(fill="x", padx=15, pady=10)

        # Status
        self.status_var = ctk.StringVar(value="Em andamento")

        row = ctk.CTkFrame(content, fg_color="transparent")
        row.pack(fill="x")

        ctk.CTkRadioButton(row, text="Em andamento",
                           variable=self.status_var,
                           value="Em andamento").pack(side="left", padx=5)

        ctk.CTkRadioButton(row, text="Concluída",
                           variable=self.status_var,
                           value="Concluída").pack(side="left", padx=5)

        # Data abertura
        data_row = ctk.CTkFrame(content, fg_color="transparent")
        data_row.pack(fill="x", pady=5)

        self.data_abertura = ctk.CTkEntry(data_row, placeholder_text="Data abertura")
        self.data_abertura.pack(side="left", padx=5)

        self.hora_abertura = ctk.CTkEntry(data_row, width=60, placeholder_text="HH")
        self.hora_abertura.pack(side="left", padx=2)

        self.min_abertura = ctk.CTkEntry(data_row, width=60, placeholder_text="MM")
        self.min_abertura.pack(side="left", padx=2)

        # Mesmo dia
        self.mesmo_dia = ctk.BooleanVar(value=True)

        ctk.CTkCheckBox(
            content,
            text="Mesmo dia",
            variable=self.mesmo_dia,
            command=self.toggle_data
        ).pack(anchor="w")

        # Data conclusão
        self.data_conclusao = ctk.CTkEntry(content, placeholder_text="Data conclusão")
        self.data_conclusao.pack(fill="x", pady=5)

        self.toggle_data()

    def toggle_data(self):
        state = "disabled" if self.mesmo_dia.get() else "normal"
        self.data_conclusao.configure(state=state)

    # ================= BOTÕES =================
    def criar_botoes(self, parent):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(pady=10)

        ctk.CTkButton(
            frame,
            text="💾 Salvar",
            fg_color=COLORS['primary'],
            command=self.salvar
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            frame,
            text="🧹 Limpar",
            fg_color=COLORS['warning'],
            command=self.limpar
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            frame,
            text="⬅ Voltar",
            fg_color=COLORS['danger'],
            command=lambda: self.app.mostrar_tela("dashboard")
        ).pack(side="left", padx=10)

    # ================= AÇÕES =================
    def salvar(self):
        if not self.numero_bd.get():
            messagebox.showwarning("Aviso", "Informe o Nº do BD")
            return

        messagebox.showinfo("Sucesso", "OS salva com sucesso!")

    def limpar(self):
        for widget in self.winfo_children():
            pass  # pode melhorar depois