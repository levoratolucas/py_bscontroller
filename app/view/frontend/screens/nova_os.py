import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from app.view.frontend.styles import COLORS, FONTS
from app.bd.conexao import Conexao


class NovaOsScreen(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        # NÃO use pack aqui! O main_window fará o pack
        
        self.app = app
        self.con = Conexao()
        self.linhas_widgets = []
        self.tecnicos = []
        self.linha_atual_carimbo = None
        
        self.carregar_tecnicos()
        self.setup_ui()
        self.adicionar_linha()

    def carregar_tecnicos(self):
        """Carrega a lista de técnicos do banco"""
        try:
            conn = self.con.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, matricula FROM tecnicos ORDER BY nome")
            self.tecnicos = cursor.fetchall()
            conn.close()
        except Exception as e:
            print(f"Erro ao carregar técnicos: {e}")
            self.tecnicos = []

    def setup_ui(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        ctk.CTkLabel(
            main_frame,
            text="📝 Inserir OS (Modo Tabela)",
            font=FONTS['title'],
            text_color=COLORS['primary']
        ).pack(anchor="w", pady=(0, 20))

        # ================= BARRA DE FERRAMENTAS =================
        toolbar = ctk.CTkFrame(main_frame, fg_color="transparent")
        toolbar.pack(fill="x", pady=(0, 10))
        
        ctk.CTkButton(
            toolbar,
            text="➕ Adicionar Linha",
            fg_color=COLORS['success'],
            width=150,
            command=self.adicionar_linha
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            toolbar,
            text="🗑️ Remover Última Linha",
            fg_color=COLORS['warning'],
            width=180,
            command=self.remover_ultima_linha
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            toolbar,
            text="💾 Salvar Todas",
            fg_color=COLORS['primary'],
            width=150,
            command=self.salvar_todas
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            toolbar,
            text="🗑️ Limpar Tudo",
            fg_color=COLORS['danger'],
            width=150,
            command=self.limpar_tudo
        ).pack(side="left")
        
        # Label de total de linhas
        self.total_label = ctk.CTkLabel(
            toolbar,
            text="Total: 0 linha(s)",
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        self.total_label.pack(side="right", padx=10)

        # ================= ÁREA DA TABELA =================
        tabela_frame = ctk.CTkFrame(main_frame, fg_color=COLORS['bg_card'], corner_radius=12)
        tabela_frame.pack(fill="both", expand=True, pady=(0, 10))

        # Container para scroll
        self.container = ctk.CTkScrollableFrame(tabela_frame, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=10, pady=10)

        # Cabeçalho da tabela
        self.header_frame = ctk.CTkFrame(self.container, fg_color=COLORS['bg_hover'], corner_radius=8)
        self.header_frame.pack(fill="x", pady=(0, 5))
        
        # Definindo larguras das colunas
        colunas = [
            ("Nº OS", 100),
            ("Técnico", 180),
            ("WAN/Piloto", 130),
            ("Tipo", 80),
            ("Status", 100),
            ("Data", 110),
            ("Início", 70),
            ("Fim", 70),
            ("Carimbo", 60),
            ("Ações", 80)
        ]
        
        for texto, largura in colunas:
            ctk.CTkLabel(
                self.header_frame,
                text=texto,
                font=FONTS['small_bold'],
                text_color=COLORS['text_light'],
                width=largura
            ).pack(side="left", padx=5, pady=8)

        # Frame para as linhas
        self.linhas_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.linhas_frame.pack(fill="both", expand=True)

    def adicionar_linha(self, dados=None):
        """Adiciona uma nova linha na tabela"""
        linha = ctk.CTkFrame(self.linhas_frame, fg_color="transparent")
        linha.pack(fill="x", pady=2)
        
        # Nº OS
        numero_entry = ctk.CTkEntry(linha, width=100, placeholder_text="Nº OS")
        numero_entry.pack(side="left", padx=5)
        if dados and dados.get('numero'):
            numero_entry.insert(0, dados['numero'])
        
        # Técnico (Dropdown)
        tecnicos_nomes = [f"{t[1]}" for t in self.tecnicos]
        tecnico_combo = ctk.CTkComboBox(linha, values=tecnicos_nomes, width=180)
        tecnico_combo.pack(side="left", padx=5)
        if dados and dados.get('tecnico'):
            tecnico_combo.set(dados['tecnico'])
        elif tecnicos_nomes:
            tecnico_combo.set(tecnicos_nomes[0])
        
        # WAN/Piloto
        wan_entry = ctk.CTkEntry(linha, width=130, placeholder_text="IP ou identificador")
        wan_entry.pack(side="left", padx=5)
        if dados and dados.get('wan'):
            wan_entry.insert(0, dados['wan'])
        
        # Tipo (Dropdown)
        tipo_combo = ctk.CTkComboBox(linha, values=["1 - Apoio", "2 - Reparo", "3 - Ativação"], width=80)
        tipo_combo.pack(side="left", padx=5)
        if dados and dados.get('tipo'):
            tipo_combo.set(dados['tipo'])
        else:
            tipo_combo.set("2 - Reparo")
        
        # Status (Dropdown)
        status_combo = ctk.CTkComboBox(linha, values=["1 - Concluído", "0 - Suspenso"], width=100)
        status_combo.pack(side="left", padx=5)
        if dados and dados.get('status'):
            status_combo.set(dados['status'])
        else:
            status_combo.set("1 - Concluído")
        
        # Data
        data_entry = ctk.CTkEntry(linha, width=110, placeholder_text="YYYY-MM-DD")
        data_entry.pack(side="left", padx=5)
        if dados and dados.get('data'):
            data_entry.insert(0, dados['data'])
        else:
            data_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Início
        inicio_entry = ctk.CTkEntry(linha, width=70, placeholder_text="HH:MM")
        inicio_entry.pack(side="left", padx=5)
        if dados and dados.get('inicio'):
            inicio_entry.insert(0, dados['inicio'])
        else:
            inicio_entry.insert(0, "08:00")
        
        # Fim
        fim_entry = ctk.CTkEntry(linha, width=70, placeholder_text="HH:MM")
        fim_entry.pack(side="left", padx=5)
        if dados and dados.get('fim'):
            fim_entry.insert(0, dados['fim'])
        else:
            fim_entry.insert(0, "17:00")
        
        # Botão Carimbo
        carimbo_btn = ctk.CTkButton(
            linha, 
            text="📄", 
            width=40,
            fg_color=COLORS['info'],
            command=lambda l=linha, n=numero_entry: self.abrir_carimbo(l, n)
        )
        carimbo_btn.pack(side="left", padx=5)
        
        # Botão Remover
        remover_btn = ctk.CTkButton(
            linha, 
            text="❌", 
            width=40,
            fg_color=COLORS['danger'],
            command=lambda: self.remover_linha(linha)
        )
        remover_btn.pack(side="left", padx=5)
        
        # Armazenar widgets da linha
        self.linhas_widgets.append({
            'frame': linha,
            'numero': numero_entry,
            'tecnico': tecnico_combo,
            'wan': wan_entry,
            'tipo': tipo_combo,
            'status': status_combo,
            'data': data_entry,
            'inicio': inicio_entry,
            'fim': fim_entry,
            'carimbo': None
        })
        
        self.atualizar_total()

    def abrir_carimbo(self, linha_frame, numero_entry):
        """Abre uma janela para editar o carimbo da linha selecionada"""
        linha_dados = None
        for linha in self.linhas_widgets:
            if linha['frame'] == linha_frame:
                linha_dados = linha
                break
        
        if not linha_dados:
            return
        
        janela = ctk.CTkToplevel(self)
        janela.title(f"Carimbo da OS - {numero_entry.get() if numero_entry.get() else 'Nova'}")
        janela.geometry("800x600")
        janela.grab_set()
        
        main_frame = ctk.CTkFrame(janela, fg_color=COLORS['bg_dark'])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            main_frame,
            text="📄 Carimbo / Relatório da Atividade",
            font=FONTS['subtitle'],
            text_color=COLORS['primary']
        ).pack(anchor="w", pady=(0, 10))
        
        carimbo_text = ctk.CTkTextbox(
            main_frame, 
            font=('Consolas', 11),
            fg_color=COLORS['bg_input'],
            text_color=COLORS['text_light']
        )
        carimbo_text.pack(fill="both", expand=True, pady=(0, 10))
        
        if linha_dados['carimbo']:
            carimbo_text.insert("1.0", linha_dados['carimbo'])
        
        template_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        template_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            template_frame,
            text="Template rápido:",
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        ).pack(anchor="w")
        
        template_text = """⚠️Atualização Atividades B2B ⚠️*

Técnico: {tecnico}
OS: {numero}

Cliente: 
Endereço: 
Cidade: 
Estado: 
Validado por:

Dados de rede: 
OS/TA/DESIGNADOR: 

CAUSA RAIZ: 

Materiais Utilizados: 

Próxima Atualização:"""
        
        def aplicar_template():
            numero = linha_dados['numero'].get() if linha_dados['numero'].get() else "_____"
            tecnico = linha_dados['tecnico'].get() if linha_dados['tecnico'].get() else "_____"
            carimbo_text.delete("1.0", "end")
            carimbo_text.insert("1.0", template_text.format(tecnico=tecnico, numero=numero))
        
        ctk.CTkButton(
            template_frame,
            text="📋 Inserir Template",
            fg_color=COLORS['info'],
            width=150,
            command=aplicar_template
        ).pack(anchor="w", pady=5)
        
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        def salvar():
            linha_dados['carimbo'] = carimbo_text.get("1.0", "end-1c")
            janela.destroy()
            messagebox.showinfo("Sucesso", "Carimbo salvo!")
        
        ctk.CTkButton(
            btn_frame,
            text="💾 Salvar Carimbo",
            fg_color=COLORS['success'],
            command=salvar
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            fg_color=COLORS['danger'],
            command=janela.destroy
        ).pack(side="left", padx=5)

    def remover_linha(self, linha_frame):
        """Remove uma linha específica"""
        for i, linha in enumerate(self.linhas_widgets):
            if linha['frame'] == linha_frame:
                linha['frame'].destroy()
                self.linhas_widgets.pop(i)
                break
        self.atualizar_total()

    def remover_ultima_linha(self):
        """Remove a última linha da tabela"""
        if self.linhas_widgets:
            ultima_linha = self.linhas_widgets[-1]
            ultima_linha['frame'].destroy()
            self.linhas_widgets.pop()
        self.atualizar_total()

    def limpar_tudo(self):
        """Remove todas as linhas"""
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja limpar todas as linhas?"):
            for linha in self.linhas_widgets:
                linha['frame'].destroy()
            self.linhas_widgets.clear()
            self.adicionar_linha()
            self.atualizar_total()

    def atualizar_total(self):
        """Atualiza o label de total de linhas"""
        total = len(self.linhas_widgets)
        self.total_label.configure(text=f"Total: {total} linha(s)")


    def salvar_todas(self):
        """Salva todas as linhas no banco de dados"""
        if not self.linhas_widgets:
            messagebox.showwarning("Aviso", "Nenhuma linha para salvar!")
            return
        
        # Verificar se há linhas com dados mínimos
        linhas_validas = []
        for linha in self.linhas_widgets:
            numero = linha['numero'].get().strip()
            if not numero:
                continue  # Pula linhas sem número
            linhas_validas.append(linha)
        
        if not linhas_validas:
            messagebox.showwarning("Aviso", "Nenhuma linha com Nº OS preenchido!")
            return
        
        confirmar = messagebox.askyesno(
            "Confirmar", 
            f"Deseja salvar {len(linhas_validas)} OS(s)?"
        )
        
        if not confirmar:
            return
        
        inseridos = 0
        erros = []
        
        try:
            conn = self.con.conectar()
            cursor = conn.cursor()
            data_criacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            for linha in linhas_validas:
                numero = linha['numero'].get().strip()
                tecnico_nome = linha['tecnico'].get().strip()
                wan = linha['wan'].get().strip()
                tipo_texto = linha['tipo'].get().strip()
                status_texto = linha['status'].get().strip()
                data_exec = linha['data'].get().strip()
                inicio = linha['inicio'].get().strip()
                fim = linha['fim'].get().strip()
                carimbo = linha['carimbo'] if linha['carimbo'] else ""
                
                # Mapear tipo
                tipo_map = {"1 - Apoio": 1, "2 - Reparo": 2, "3 - Ativação": 3}
                tipo = tipo_map.get(tipo_texto, 2)
                
                # Mapear status
                status = 1 if "Concluído" in status_texto else 0
                
                # Buscar ou criar técnico
                cursor.execute("SELECT id FROM tecnicos WHERE nome = ?", (tecnico_nome,))
                tecnico = cursor.fetchone()
                
                if tecnico:
                    id_tecnico = tecnico[0]
                else:
                    cursor.execute("INSERT INTO tecnicos (nome, matricula) VALUES (?, ?)", 
                                (tecnico_nome, ""))
                    id_tecnico = cursor.lastrowid
                
                # ⚠️ VALIDAÇÃO MODIFICADA ⚠️
                # Só impede inserir se a OS já existe E está CONCLUÍDA (status = 1)
                # OS suspensas (status = 0) podem ter múltiplas entradas
                cursor.execute("""
                    SELECT status FROM ordem_servico WHERE numero = ? AND status = 1
                """, (numero,))
                
                if cursor.fetchone():
                    erros.append(f"OS {numero} já está CONCLUÍDA - não pode adicionar mais")
                    continue
                
                # Inserir OS (permite múltiplas entradas da mesma OS se não estiver concluída)
                cursor.execute("""
                    INSERT INTO ordem_servico 
                    (numero, id_tecnico, wan_piloto, carimbo, tipo, status, 
                    data_criacao, data, inicio_execucao, fim_execucao)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (numero, id_tecnico, wan, carimbo, tipo, status, 
                    data_criacao, data_exec, inicio, fim))
                
                inseridos += 1
            
            conn.commit()
            conn.close()
            
            if inseridos > 0:
                messagebox.showinfo("Sucesso", f"{inseridos} OS(s) inserida(s) com sucesso!")
                self.limpar_tudo()
            
            if erros:
                messagebox.showwarning("Atenção", "Erros:\n" + "\n".join(erros[:5]))
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")