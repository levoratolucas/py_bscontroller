import customtkinter as ctk
from tkinter import messagebox, ttk
from app.view.frontend.styles import COLORS, FONTS
from app.bd.conexao import Conexao
from datetime import datetime


class QueryTesterScreen(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        
        self.app = app
        self.con = Conexao()
        
        self.setup_ui()

    def setup_ui(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        ctk.CTkLabel(
            main_frame,
            text="🔍 Teste de Queries SQL",
            font=FONTS['title'],
            text_color=COLORS['primary']
        ).pack(anchor="w", pady=(0, 20))

        # ================= ABAS =================
        self.tabview = ctk.CTkTabview(main_frame)
        self.tabview.pack(fill="both", expand=True)
        
        # Aba Executar Query
        self.tab_query = self.tabview.add("📝 Executar Query")
        self.setup_tab_query()
        
        # Aba Inserir OS
        self.tab_inserir = self.tabview.add("➕ Inserir OS")
        self.setup_tab_inserir()
        
        # Aba Inserir CSV
        self.tab_csv = self.tabview.add("📁 Inserir CSV")
        self.setup_tab_csv()

    def setup_tab_query(self):
        """Aba para executar queries SQL"""
        query_frame = ctk.CTkFrame(self.tab_query, fg_color=COLORS['bg_card'], corner_radius=12)
        query_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            query_frame,
            text="📝 Query SQL",
            font=FONTS['subtitle'],
            text_color=COLORS['primary']
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        self.query_text = ctk.CTkTextbox(query_frame, height=150, font=('Consolas', 12))
        self.query_text.pack(fill="x", padx=15, pady=(0, 10))
        
        # Query exemplo
        query_exemplo = """-- ==================== EXEMPLOS DE QUERIES ====================

-- 1. Ver todas as OS
SELECT * FROM ordem_servico;

-- 2. OS com TMR (Tempo Médio de Reparo)
SELECT 
    numero,
    data,
    inicio_execucao,
    fim_execucao,
    ROUND((strftime('%s', data || ' ' || fim_execucao) - 
           strftime('%s', data || ' ' || inicio_execucao)) / 3600.0, 2) as horas_trabalhadas
FROM ordem_servico
WHERE tipo = 2 AND status = 1;

-- 3. WANs repetidos
SELECT o.numero, o.wan_piloto, t.nome as tecnico, o.data_criacao
FROM ordem_servico o
LEFT JOIN tecnicos t ON t.id = o.id_tecnico
WHERE o.wan_piloto IN (
    SELECT wan_piloto 
    FROM ordem_servico 
    WHERE wan_piloto IS NOT NULL AND wan_piloto != ''
    GROUP BY wan_piloto
    HAVING COUNT(*) > 1
)
ORDER BY o.wan_piloto, o.data_criacao;

-- 4. Estatísticas por técnico
SELECT 
    t.nome,
    COUNT(o.id_os) as total_os,
    SUM(CASE WHEN o.tipo = 1 THEN 1 ELSE 0 END) as apoio,
    SUM(CASE WHEN o.tipo = 2 THEN 1 ELSE 0 END) as reparo,
    SUM(CASE WHEN o.tipo = 3 THEN 1 ELSE 0 END) as ativacao,
    SUM(CASE WHEN o.status = 1 THEN 1 ELSE 0 END) as concluidos,
    ROUND(AVG((strftime('%s', o.data || ' ' || o.fim_execucao) - 
               strftime('%s', o.data || ' ' || o.inicio_execucao)) / 3600.0), 2) as tmr_medio
FROM tecnicos t
LEFT JOIN ordem_servico o ON t.id = o.id_tecnico
GROUP BY t.id;

-- 5. Resumo por mês
SELECT 
    strftime('%Y-%m', data_criacao) as mes,
    COUNT(*) as total_os,
    SUM(CASE WHEN status = 1 THEN 1 ELSE 0 END) as concluidos,
    SUM(CASE WHEN status = 0 THEN 1 ELSE 0 END) as suspensos
FROM ordem_servico
GROUP BY strftime('%Y-%m', data_criacao)
ORDER BY mes DESC;"""
        
        self.query_text.insert("1.0", query_exemplo)
        
        # Botões
        btn_frame = ctk.CTkFrame(query_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkButton(btn_frame, text="▶ Executar", fg_color=COLORS['success'], 
                     command=self.executar_query).pack(side="left", padx=(0, 10))
        ctk.CTkButton(btn_frame, text="🗑️ Limpar", fg_color=COLORS['warning'], 
                     command=self.limpar_query).pack(side="left")
        
        # Resultado
        result_frame = ctk.CTkFrame(self.tab_query, fg_color=COLORS['bg_card'], corner_radius=12)
        result_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        ctk.CTkLabel(
            result_frame,
            text="📊 Resultado",
            font=FONTS['subtitle'],
            text_color=COLORS['primary']
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        # Treeview
        table_container = ctk.CTkFrame(result_frame, fg_color="transparent")
        table_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tree = ttk.Treeview(table_container, show="headings", height=15)
        vsb = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)
        
        self.status_label = ctk.CTkLabel(result_frame, text="Aguardando query...", 
                                         font=FONTS['small'], text_color=COLORS['text_secondary'])
        self.status_label.pack(anchor="w", padx=15, pady=(0, 10))

    def setup_tab_inserir(self):
        """Aba para inserir OS manualmente"""
        form_frame = ctk.CTkFrame(self.tab_inserir, fg_color=COLORS['bg_card'], corner_radius=12)
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            form_frame,
            text="➕ Inserir Nova OS",
            font=FONTS['subtitle'],
            text_color=COLORS['primary']
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        form_content = ctk.CTkFrame(form_frame, fg_color="transparent")
        form_content.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Nº OS
        row1 = ctk.CTkFrame(form_content, fg_color="transparent")
        row1.pack(fill="x", pady=5)
        ctk.CTkLabel(row1, text="Nº OS:", width=120).pack(side="left", padx=5)
        self.numero_entry = ctk.CTkEntry(row1, width=200)
        self.numero_entry.pack(side="left", padx=5)
        
        # WAN/Piloto
        row2 = ctk.CTkFrame(form_content, fg_color="transparent")
        row2.pack(fill="x", pady=5)
        ctk.CTkLabel(row2, text="WAN/Piloto:", width=120).pack(side="left", padx=5)
        self.wan_entry = ctk.CTkEntry(row2, width=200)
        self.wan_entry.pack(side="left", padx=5)
        
        # Técnico
        row3 = ctk.CTkFrame(form_content, fg_color="transparent")
        row3.pack(fill="x", pady=5)
        ctk.CTkLabel(row3, text="Técnico:", width=120).pack(side="left", padx=5)
        self.tecnico_entry = ctk.CTkEntry(row3, width=200)
        self.tecnico_entry.pack(side="left", padx=5)
        
        # Matrícula
        row4 = ctk.CTkFrame(form_content, fg_color="transparent")
        row4.pack(fill="x", pady=5)
        ctk.CTkLabel(row4, text="Matrícula:", width=120).pack(side="left", padx=5)
        self.matricula_entry = ctk.CTkEntry(row4, width=200)
        self.matricula_entry.pack(side="left", padx=5)
        
        # Data
        row5 = ctk.CTkFrame(form_content, fg_color="transparent")
        row5.pack(fill="x", pady=5)
        ctk.CTkLabel(row5, text="Data (YYYY-MM-DD):", width=120).pack(side="left", padx=5)
        self.data_entry = ctk.CTkEntry(row5, width=200)
        self.data_entry.pack(side="left", padx=5)
        self.data_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Início Execução
        row6 = ctk.CTkFrame(form_content, fg_color="transparent")
        row6.pack(fill="x", pady=5)
        ctk.CTkLabel(row6, text="Início (HH:MM):", width=120).pack(side="left", padx=5)
        self.inicio_entry = ctk.CTkEntry(row6, width=200)
        self.inicio_entry.pack(side="left", padx=5)
        self.inicio_entry.insert(0, "08:00")
        
        # Fim Execução
        row7 = ctk.CTkFrame(form_content, fg_color="transparent")
        row7.pack(fill="x", pady=5)
        ctk.CTkLabel(row7, text="Fim (HH:MM):", width=120).pack(side="left", padx=5)
        self.fim_entry = ctk.CTkEntry(row7, width=200)
        self.fim_entry.pack(side="left", padx=5)
        self.fim_entry.insert(0, "17:00")
        
        # Tipo
        row8 = ctk.CTkFrame(form_content, fg_color="transparent")
        row8.pack(fill="x", pady=5)
        ctk.CTkLabel(row8, text="Tipo:", width=120).pack(side="left", padx=5)
        self.tipo_combo = ctk.CTkComboBox(row8, values=["Apoio", "Reparo", "Ativação"], width=200)
        self.tipo_combo.pack(side="left", padx=5)
        self.tipo_combo.set("Reparo")
        
        # Status
        row9 = ctk.CTkFrame(form_content, fg_color="transparent")
        row9.pack(fill="x", pady=5)
        ctk.CTkLabel(row9, text="Status:", width=120).pack(side="left", padx=5)
        self.status_combo = ctk.CTkComboBox(row9, values=["Concluído", "Suspenso"], width=200)
        self.status_combo.pack(side="left", padx=5)
        self.status_combo.set("Concluído")
        
        # Carimbo
        row10 = ctk.CTkFrame(form_content, fg_color="transparent")
        row10.pack(fill="x", pady=5)
        ctk.CTkLabel(row10, text="Carimbo:", width=120).pack(side="left", padx=5)
        self.carimbo_text = ctk.CTkTextbox(row10, height=80, width=400)
        self.carimbo_text.pack(side="left", padx=5, fill="x", expand=True)
        
        # Botões
        btn_frame = ctk.CTkFrame(form_content, fg_color="transparent")
        btn_frame.pack(fill="x", pady=15)
        
        ctk.CTkButton(btn_frame, text="💾 Salvar OS", fg_color=COLORS['success'], 
                     command=self.inserir_os).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🗑️ Limpar", fg_color=COLORS['warning'], 
                     command=self.limpar_formulario).pack(side="left", padx=5)
        
        self.inserir_status = ctk.CTkLabel(form_content, text="", font=FONTS['small'])
        self.inserir_status.pack(anchor="w", pady=5)

    def setup_tab_csv(self):
        """Aba para inserir CSV rápido"""
        csv_frame = ctk.CTkFrame(self.tab_csv, fg_color=COLORS['bg_card'], corner_radius=12)
        csv_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            csv_frame,
            text="📁 Inserir CSV Rápido",
            font=FONTS['subtitle'],
            text_color=COLORS['primary']
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        ctk.CTkLabel(
            csv_frame,
            text="Formato: numero;tecnico_nome;tecnico_matricula;wan_piloto;carimbo;tipo;status;data;inicio;fim",
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        ).pack(anchor="w", padx=15, pady=(0, 10))
        
        self.csv_text = ctk.CTkTextbox(csv_frame, height=250, font=('Consolas', 11))
        self.csv_text.pack(fill="both", expand=True, padx=15, pady=10)
        
        csv_exemplo = """7001;JONATHAN E LUCIANO;123456;187.50.117.1;Ativação de novo cliente;3;1;2026-04-01;08:00;10:30
7002;ANDER SILVA;123457;187.50.117.2;Reparo de roteador;2;1;2026-04-01;09:30;11:15
7003;PEDRO COSTA;123458;187.50.117.3;Manutenção preventiva;2;1;2026-04-01;10:15;12:00
7004;LUCAS SANTOS;123459;187.50.117.4;Apoio técnico;1;1;2026-04-02;08:45;09:30
7005;JONATHAN E LUCIANO;123456;187.50.117.9;Ativação de rede;3;1;2026-04-03;13:45;15:30
7006;ANDER SILVA;123457;187.50.117.9;Reparo de cabo;2;1;2026-04-06;11:00;12:30
7007;PEDRO COSTA;123458;187.50.117.9;Troca de roteador;2;1;2026-04-07;08:30;10:00"""
        
        self.csv_text.insert("1.0", csv_exemplo)
        
        btn_frame = ctk.CTkFrame(csv_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkButton(btn_frame, text="📤 Inserir CSV", fg_color=COLORS['success'], 
                     command=self.inserir_csv).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🗑️ Limpar", fg_color=COLORS['warning'], 
                     command=self.limpar_csv).pack(side="left", padx=5)
        
        self.csv_status = ctk.CTkLabel(csv_frame, text="", font=FONTS['small'])
        self.csv_status.pack(anchor="w", padx=15, pady=5)

    # ================= MÉTODOS DA QUERY =================
    
    def executar_query(self):
        query = self.query_text.get("1.0", "end").strip()
        if not query:
            messagebox.showwarning("Aviso", "Digite uma query SQL!")
            return
        
        try:
            conn = self.con.conectar()
            cursor = conn.cursor()
            cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                dados = cursor.fetchall()
                colunas = [description[0] for description in cursor.description]
                self.mostrar_resultados(colunas, dados)
                self.status_label.configure(text=f"✅ {len(dados)} registros retornados.", 
                                           text_color=COLORS['success'])
            else:
                conn.commit()
                self.status_label.configure(text=f"✅ Query executada! {cursor.rowcount} linhas afetadas.", 
                                           text_color=COLORS['success'])
                self.limpar_tabela()
            
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro SQL", str(e))
            self.status_label.configure(text=f"❌ Erro: {str(e)[:100]}", text_color=COLORS['danger'])

    def mostrar_resultados(self, colunas, dados):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.tree["columns"] = colunas
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, minwidth=80)
        
        for row in dados:
            valores = [str(val) if val is not None else "" for val in row]
            self.tree.insert("", "end", values=valores)

    def limpar_tabela(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.tree["columns"] = []

    def limpar_query(self):
        self.query_text.delete("1.0", "end")
        self.limpar_tabela()
        self.status_label.configure(text="Aguardando query...", text_color=COLORS['text_secondary'])

    # ================= MÉTODOS DE INSERÇÃO =================
    
    def inserir_os(self):
        numero = self.numero_entry.get().strip()
        wan = self.wan_entry.get().strip()
        tecnico_nome = self.tecnico_entry.get().strip()
        tecnico_matricula = self.matricula_entry.get().strip()
        data = self.data_entry.get().strip()
        inicio = self.inicio_entry.get().strip()
        fim = self.fim_entry.get().strip()
        tipo_texto = self.tipo_combo.get()
        status_texto = self.status_combo.get()
        carimbo = self.carimbo_text.get("1.0", "end").strip()
        
        if not numero or not tecnico_nome or not data:
            self.inserir_status.configure(text="❌ Nº OS, Técnico e Data são obrigatórios!", text_color=COLORS['danger'])
            return
        
        tipo_map = {"Apoio": 1, "Reparo": 2, "Ativação": 3}
        tipo = tipo_map.get(tipo_texto, 2)
        status = 1 if status_texto == "Concluído" else 0
        
        data_criacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            conn = self.con.conectar()
            cursor = conn.cursor()
            
            cursor.execute("SELECT id FROM tecnicos WHERE nome = ?", (tecnico_nome,))
            tecnico = cursor.fetchone()
            
            if tecnico:
                id_tecnico = tecnico[0]
            else:
                cursor.execute("INSERT INTO tecnicos (nome, matricula) VALUES (?, ?)", 
                              (tecnico_nome, tecnico_matricula))
                id_tecnico = cursor.lastrowid
            
            cursor.execute("SELECT id_os FROM ordem_servico WHERE numero = ?", (numero,))
            if cursor.fetchone():
                self.inserir_status.configure(text=f"❌ OS {numero} já existe!", text_color=COLORS['danger'])
                conn.close()
                return
            
            cursor.execute("""
                INSERT INTO ordem_servico 
                (numero, id_tecnico, wan_piloto, carimbo, tipo, status, data_criacao, data, inicio_execucao, fim_execucao)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (numero, id_tecnico, wan, carimbo, tipo, status, data_criacao, data, inicio, fim))
            
            conn.commit()
            conn.close()
            
            self.inserir_status.configure(text=f"✅ OS {numero} inserida com sucesso!", text_color=COLORS['success'])
            self.limpar_formulario()
            
        except Exception as e:
            self.inserir_status.configure(text=f"❌ Erro: {str(e)}", text_color=COLORS['danger'])

    def inserir_csv(self):
        csv_content = self.csv_text.get("1.0", "end").strip()
        if not csv_content:
            self.csv_status.configure(text="❌ Digite ou cole o conteúdo CSV!", text_color=COLORS['danger'])
            return
        
        linhas = csv_content.strip().split('\n')
        inseridos = 0
        erros = []
        
        try:
            conn = self.con.conectar()
            cursor = conn.cursor()
            data_criacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            for i, linha in enumerate(linhas, 1):
                if not linha.strip():
                    continue
                
                partes = linha.split(';')
                if len(partes) < 10:
                    erros.append(f"Linha {i}: Formato inválido (esperado 10 campos)")
                    continue
                
                numero = partes[0].strip()
                tecnico_nome = partes[1].strip()
                tecnico_matricula = partes[2].strip()
                wan = partes[3].strip()
                carimbo = partes[4].strip()
                tipo = int(partes[5].strip()) if partes[5].strip().isdigit() else 2
                status = int(partes[6].strip()) if partes[6].strip().isdigit() else 1
                data = partes[7].strip()
                inicio = partes[8].strip()
                fim = partes[9].strip()
                
                # Buscar ou criar técnico
                cursor.execute("SELECT id FROM tecnicos WHERE nome = ?", (tecnico_nome,))
                tecnico = cursor.fetchone()
                
                if tecnico:
                    id_tecnico = tecnico[0]
                else:
                    cursor.execute("INSERT INTO tecnicos (nome, matricula) VALUES (?, ?)", 
                                  (tecnico_nome, tecnico_matricula))
                    id_tecnico = cursor.lastrowid
                
                # Inserir OS
                cursor.execute("""
                    INSERT OR IGNORE INTO ordem_servico 
                    (numero, id_tecnico, wan_piloto, carimbo, tipo, status, data_criacao, data, inicio_execucao, fim_execucao)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (numero, id_tecnico, wan, carimbo, tipo, status, data_criacao, data, inicio, fim))
                
                if cursor.rowcount > 0:
                    inseridos += 1
                else:
                    erros.append(f"Linha {i}: OS {numero} já existe")
            
            conn.commit()
            conn.close()
            
            msg = f"✅ {inseridos} OS inseridas com sucesso!"
            if erros:
                msg += f"\n⚠️ {len(erros)} erros: " + "\n".join(erros[:3])
            self.csv_status.configure(text=msg, text_color=COLORS['success'] if inseridos > 0 else COLORS['warning'])
            
        except Exception as e:
            self.csv_status.configure(text=f"❌ Erro: {str(e)}", text_color=COLORS['danger'])

    def limpar_formulario(self):
        self.numero_entry.delete(0, "end")
        self.wan_entry.delete(0, "end")
        self.tecnico_entry.delete(0, "end")
        self.matricula_entry.delete(0, "end")
        self.data_entry.delete(0, "end")
        self.data_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.inicio_entry.delete(0, "end")
        self.inicio_entry.insert(0, "08:00")
        self.fim_entry.delete(0, "end")
        self.fim_entry.insert(0, "17:00")
        self.carimbo_text.delete("1.0", "end")
        self.tipo_combo.set("Reparo")
        self.status_combo.set("Concluído")

    def limpar_csv(self):
        self.csv_text.delete("1.0", "end")
        self.csv_status.configure(text="")