import customtkinter as ctk
from tkinter import messagebox
from app.view.frontend.styles import COLORS, FONTS
from app.bd.conexao import Conexao


class AdminScreen(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        
        self.app = app
        self.con = Conexao()
        self.os_selecionada_id = None
        
        self.setup_ui()
        self.carregar_tecnicos()

    def setup_ui(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        ctk.CTkLabel(
            main_frame,
            text="⚙️ Administração",
            font=FONTS['title'],
            text_color=COLORS['primary']
        ).pack(anchor="w", pady=(0, 20))

        # ================= ABAS =================
        self.tabview = ctk.CTkTabview(main_frame)
        self.tabview.pack(fill="both", expand=True)
        
        # Aba Técnicos
        self.tab_tecnicos = self.tabview.add("👤 Técnicos")
        self.setup_tab_tecnicos()
        
        # Aba Buscar/Editar OS
        self.tab_buscar = self.tabview.add("🔍 Buscar/Editar OS")
        self.setup_tab_buscar()

    # ================= ABA TÉCNICOS =================
    def setup_tab_tecnicos(self):
        # Frame do formulário
        form_frame = ctk.CTkFrame(self.tab_tecnicos, fg_color=COLORS['bg_card'], corner_radius=12)
        form_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            form_frame,
            text="➕ Adicionar Novo Técnico",
            font=FONTS['subtitle'],
            text_color=COLORS['primary']
        ).pack(anchor="w", padx=15, pady=(10, 5))

        form_content = ctk.CTkFrame(form_frame, fg_color="transparent")
        form_content.pack(fill="x", padx=15, pady=(0, 15))

        # Nome
        row1 = ctk.CTkFrame(form_content, fg_color="transparent")
        row1.pack(fill="x", pady=5)
        
        ctk.CTkLabel(row1, text="Nome:", width=80, font=FONTS['normal']).pack(side="left", padx=5)
        self.nome_entry = ctk.CTkEntry(row1, width=300, placeholder_text="Nome do técnico")
        self.nome_entry.pack(side="left", padx=5)

        # Matrícula
        row2 = ctk.CTkFrame(form_content, fg_color="transparent")
        row2.pack(fill="x", pady=5)
        
        ctk.CTkLabel(row2, text="Matrícula:", width=80, font=FONTS['normal']).pack(side="left", padx=5)
        self.matricula_entry = ctk.CTkEntry(row2, width=200, placeholder_text="Nº da matrícula")
        self.matricula_entry.pack(side="left", padx=5)

        # Botões
        btn_frame = ctk.CTkFrame(form_content, fg_color="transparent")
        btn_frame.pack(fill="x", pady=10)
        
        ctk.CTkButton(
            btn_frame,
            text="💾 Salvar Técnico",
            fg_color=COLORS['success'],
            width=150,
            command=self.salvar_tecnico
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="🗑️ Limpar",
            fg_color=COLORS['warning'],
            width=100,
            command=self.limpar_formulario_tecnico
        ).pack(side="left", padx=5)

        # Lista de técnicos
        lista_frame = ctk.CTkFrame(self.tab_tecnicos, fg_color=COLORS['bg_card'], corner_radius=12)
        lista_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            lista_frame,
            text="📋 Lista de Técnicos",
            font=FONTS['subtitle'],
            text_color=COLORS['primary']
        ).pack(anchor="w", padx=15, pady=(10, 5))

        table_container = ctk.CTkFrame(lista_frame, fg_color="transparent")
        table_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Cabeçalho
        header_frame = ctk.CTkFrame(table_container, fg_color=COLORS['bg_hover'], corner_radius=8)
        header_frame.pack(fill="x", pady=(0, 5))
        
        ctk.CTkLabel(header_frame, text="ID", width=50, font=FONTS['small_bold']).pack(side="left", padx=5, pady=8)
        ctk.CTkLabel(header_frame, text="Nome", width=250, font=FONTS['small_bold']).pack(side="left", padx=5, pady=8)
        ctk.CTkLabel(header_frame, text="Matrícula", width=150, font=FONTS['small_bold']).pack(side="left", padx=5, pady=8)
        ctk.CTkLabel(header_frame, text="Ações", width=100, font=FONTS['small_bold']).pack(side="left", padx=5, pady=8)

        self.lista_container = ctk.CTkScrollableFrame(table_container, fg_color="transparent")
        self.lista_container.pack(fill="both", expand=True)

    # ================= ABA BUSCAR/EDITAR OS =================
    def setup_tab_buscar(self):
        # Frame de busca
        busca_frame = ctk.CTkFrame(self.tab_buscar, fg_color=COLORS['bg_card'], corner_radius=12)
        busca_frame.pack(fill="x", padx=10, pady=10)

        busca_content = ctk.CTkFrame(busca_frame, fg_color="transparent")
        busca_content.pack(fill="x", padx=15, pady=15)

        row1 = ctk.CTkFrame(busca_content, fg_color="transparent")
        row1.pack(fill="x", pady=5)
        
        ctk.CTkLabel(row1, text="Nº OS:", width=80, font=FONTS['normal']).pack(side="left", padx=5)
        self.busca_numero_entry = ctk.CTkEntry(row1, width=200, placeholder_text="Digite o número da OS")
        self.busca_numero_entry.pack(side="left", padx=5)
        
        ctk.CTkButton(
            row1,
            text="🔍 Buscar",
            fg_color=COLORS['primary'],
            width=100,
            command=self.buscar_os
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            row1,
            text="🗑️ Limpar",
            fg_color=COLORS['warning'],
            width=100,
            command=self.limpar_busca
        ).pack(side="left", padx=5)

        # Frame de edição (será preenchido ao buscar)
        editar_frame = ctk.CTkFrame(self.tab_buscar, fg_color=COLORS['bg_card'], corner_radius=12)
        editar_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            editar_frame,
            text="✏️ Dados da OS",
            font=FONTS['subtitle'],
            text_color=COLORS['primary']
        ).pack(anchor="w", padx=15, pady=(10, 5))

        form_content = ctk.CTkFrame(editar_frame, fg_color="transparent")
        form_content.pack(fill="both", expand=True, padx=15, pady=10)

        # ID da OS (oculto)
        self.edit_id_os = ctk.CTkEntry(form_content, width=0)
        self.edit_id_os.pack_forget()

        # Nº OS
        row_num = ctk.CTkFrame(form_content, fg_color="transparent")
        row_num.pack(fill="x", pady=5)
        ctk.CTkLabel(row_num, text="Nº OS:", width=100, font=FONTS['normal']).pack(side="left", padx=5)
        self.edit_numero = ctk.CTkEntry(row_num, width=200)
        self.edit_numero.pack(side="left", padx=5)

        # WAN/Piloto
        row_wan = ctk.CTkFrame(form_content, fg_color="transparent")
        row_wan.pack(fill="x", pady=5)
        ctk.CTkLabel(row_wan, text="WAN/Piloto:", width=100, font=FONTS['normal']).pack(side="left", padx=5)
        self.edit_wan = ctk.CTkEntry(row_wan, width=300)
        self.edit_wan.pack(side="left", padx=5)

        # Técnico
        row_tec = ctk.CTkFrame(form_content, fg_color="transparent")
        row_tec.pack(fill="x", pady=5)
        ctk.CTkLabel(row_tec, text="Técnico:", width=100, font=FONTS['normal']).pack(side="left", padx=5)
        self.edit_tecnico = ctk.CTkComboBox(row_tec, values=[], width=300)
        self.edit_tecnico.pack(side="left", padx=5)

        # Tipo e Status (mesma linha)
        row_tipo_status = ctk.CTkFrame(form_content, fg_color="transparent")
        row_tipo_status.pack(fill="x", pady=5)
        
        ctk.CTkLabel(row_tipo_status, text="Tipo:", width=100, font=FONTS['normal']).pack(side="left", padx=5)
        self.edit_tipo = ctk.CTkComboBox(row_tipo_status, values=["1 - Apoio", "2 - Reparo", "3 - Ativação"], width=150)
        self.edit_tipo.pack(side="left", padx=5)
        
        ctk.CTkLabel(row_tipo_status, text="Status:", width=60, font=FONTS['normal']).pack(side="left", padx=(20, 5))
        self.edit_status = ctk.CTkComboBox(row_tipo_status, values=["0 - Suspenso", "1 - Concluído"], width=150)
        self.edit_status.pack(side="left", padx=5)

        # Data, Início, Fim (mesma linha)
        row_datas = ctk.CTkFrame(form_content, fg_color="transparent")
        row_datas.pack(fill="x", pady=5)
        
        ctk.CTkLabel(row_datas, text="Data:", width=100, font=FONTS['normal']).pack(side="left", padx=5)
        self.edit_data = ctk.CTkEntry(row_datas, width=120, placeholder_text="YYYY-MM-DD")
        self.edit_data.pack(side="left", padx=5)
        
        ctk.CTkLabel(row_datas, text="Início:", width=50, font=FONTS['normal']).pack(side="left", padx=(20, 5))
        self.edit_inicio = ctk.CTkEntry(row_datas, width=80, placeholder_text="HH:MM")
        self.edit_inicio.pack(side="left", padx=5)
        
        ctk.CTkLabel(row_datas, text="Fim:", width=40, font=FONTS['normal']).pack(side="left", padx=(20, 5))
        self.edit_fim = ctk.CTkEntry(row_datas, width=80, placeholder_text="HH:MM")
        self.edit_fim.pack(side="left", padx=5)

        # Carimbo
        row_carimbo = ctk.CTkFrame(form_content, fg_color="transparent")
        row_carimbo.pack(fill="both", expand=True, pady=10)
        ctk.CTkLabel(row_carimbo, text="Carimbo:", font=FONTS['normal']).pack(anchor="w", padx=5)
        self.edit_carimbo = ctk.CTkTextbox(row_carimbo, height=200, font=('Consolas', 11))
        self.edit_carimbo.pack(fill="both", expand=True, padx=5, pady=5)

        # Botões
        btn_frame = ctk.CTkFrame(form_content, fg_color="transparent")
        btn_frame.pack(fill="x", pady=10)
        
        ctk.CTkButton(
            btn_frame,
            text="💾 Salvar Alterações",
            fg_color=COLORS['success'],
            width=150,
            command=self.salvar_edicao_os
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="🗑️ Limpar Campos",
            fg_color=COLORS['warning'],
            width=150,
            command=self.limpar_campos_edicao
        ).pack(side="left", padx=5)

        self.edit_status_label = ctk.CTkLabel(form_content, text="", font=FONTS['small'])
        self.edit_status_label.pack(anchor="w", pady=5)

        # Desabilitar campos inicialmente
        self.habilitar_edicao(False)

    def habilitar_edicao(self, enabled):
        """Habilita/desabilita campos de edição"""
        self.edit_numero.configure(state="normal" if enabled else "disabled")
        self.edit_wan.configure(state="normal" if enabled else "disabled")
        self.edit_tecnico.configure(state="normal" if enabled else "disabled")
        self.edit_tipo.configure(state="normal" if enabled else "disabled")
        self.edit_status.configure(state="normal" if enabled else "disabled")
        self.edit_data.configure(state="normal" if enabled else "disabled")
        self.edit_inicio.configure(state="normal" if enabled else "disabled")
        self.edit_fim.configure(state="normal" if enabled else "disabled")
        self.edit_carimbo.configure(state="normal" if enabled else "disabled")

    # ================= MÉTODOS TÉCNICOS =================
    def carregar_tecnicos(self):
        for widget in self.lista_container.winfo_children():
            widget.destroy()
        
        try:
            conn = self.con.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, matricula FROM tecnicos ORDER BY id")
            tecnicos = cursor.fetchall()
            conn.close()
            
            # Carregar também no combo da edição
            tecnicos_nomes = [t[1] for t in tecnicos]
            self.edit_tecnico.configure(values=tecnicos_nomes)
            
            for tecnico in tecnicos:
                self.adicionar_linha_tecnico(tecnico)
                
        except Exception as e:
            print(f"Erro ao carregar técnicos: {e}")

    def adicionar_linha_tecnico(self, tecnico):
        linha = ctk.CTkFrame(self.lista_container, fg_color="transparent")
        linha.pack(fill="x", pady=2)
        
        ctk.CTkLabel(linha, text=str(tecnico[0]), width=50).pack(side="left", padx=5, pady=5)
        ctk.CTkLabel(linha, text=tecnico[1], width=250, anchor="w").pack(side="left", padx=5, pady=5)
        ctk.CTkLabel(linha, text=tecnico[2] if tecnico[2] else "-", width=150).pack(side="left", padx=5, pady=5)
        
        btn_frame = ctk.CTkFrame(linha, fg_color="transparent", width=100)
        btn_frame.pack(side="left", padx=5, pady=5)
        btn_frame.pack_propagate(False)
        
        ctk.CTkButton(
            btn_frame,
            text="✏️",
            width=30,
            fg_color=COLORS['info'],
            command=lambda t=tecnico: self.editar_tecnico(t)
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text="🗑️",
            width=30,
            fg_color=COLORS['danger'],
            command=lambda t=tecnico: self.excluir_tecnico(t)
        ).pack(side="left", padx=2)

    def salvar_tecnico(self):
        nome = self.nome_entry.get().strip()
        matricula = self.matricula_entry.get().strip()
        
        if not nome:
            messagebox.showwarning("Aviso", "Informe o nome do técnico!")
            return
        
        conn = self.con.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM tecnicos WHERE nome = ?", (nome,))
        if cursor.fetchone():
            conn.close()
            messagebox.showwarning("Aviso", f"Técnico '{nome}' já existe!")
            return
        
        cursor.execute("INSERT INTO tecnicos (nome, matricula) VALUES (?, ?)", (nome, matricula))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Sucesso", f"Técnico '{nome}' adicionado!")
        self.limpar_formulario_tecnico()
        self.carregar_tecnicos()

    def editar_tecnico(self, tecnico):
        janela = ctk.CTkToplevel(self)
        janela.title(f"Editar Técnico - {tecnico[1]}")
        janela.geometry("400x250")
        janela.grab_set()
        
        main_frame = ctk.CTkFrame(janela, fg_color=COLORS['bg_dark'])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(main_frame, text="✏️ Editar Técnico", font=FONTS['subtitle'], text_color=COLORS['primary']).pack(anchor="w", pady=(0, 20))
        
        ctk.CTkLabel(main_frame, text="Nome:").pack(anchor="w")
        nome_entry = ctk.CTkEntry(main_frame, width=300)
        nome_entry.insert(0, tecnico[1])
        nome_entry.pack(fill="x", pady=(5, 10))
        
        ctk.CTkLabel(main_frame, text="Matrícula:").pack(anchor="w")
        matricula_entry = ctk.CTkEntry(main_frame, width=200)
        matricula_entry.insert(0, tecnico[2] if tecnico[2] else "")
        matricula_entry.pack(fill="x", pady=(5, 20))
        
        def salvar_edicao():
            novo_nome = nome_entry.get().strip()
            nova_matricula = matricula_entry.get().strip()
            if not novo_nome:
                messagebox.showwarning("Aviso", "Informe o nome!")
                return
            
            conn = self.con.conectar()
            cursor = conn.cursor()
            cursor.execute("UPDATE tecnicos SET nome = ?, matricula = ? WHERE id = ?", (novo_nome, nova_matricula, tecnico[0]))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Sucesso", "Técnico atualizado!")
            janela.destroy()
            self.carregar_tecnicos()
        
        ctk.CTkButton(main_frame, text="💾 Salvar", fg_color=COLORS['success'], command=salvar_edicao).pack()

    def excluir_tecnico(self, tecnico):
        conn = self.con.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM ordem_servico WHERE id_tecnico = ?", (tecnico[0],))
        count = cursor.fetchone()[0]
        conn.close()
        
        if count > 0:
            messagebox.showwarning("Aviso", f"Técnico '{tecnico[1]}' possui {count} OS vinculadas! Não pode excluir.")
            return
        
        if messagebox.askyesno("Confirmar", f"Excluir técnico '{tecnico[1]}'?"):
            conn = self.con.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tecnicos WHERE id = ?", (tecnico[0],))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Técnico excluído!")
            self.carregar_tecnicos()

    def limpar_formulario_tecnico(self):
        self.nome_entry.delete(0, "end")
        self.matricula_entry.delete(0, "end")
        self.nome_entry.focus()

    # ================= MÉTODOS BUSCAR/EDITAR OS =================
    def buscar_os(self):
        numero = self.busca_numero_entry.get().strip()
        if not numero:
            messagebox.showwarning("Aviso", "Digite o número da OS!")
            return
        
        try:
            conn = self.con.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.id_os, o.numero, o.id_tecnico, t.nome, o.wan_piloto, o.carimbo,
                       o.tipo, o.status, o.data, o.inicio_execucao, o.fim_execucao
                FROM ordem_servico o
                LEFT JOIN tecnicos t ON t.id = o.id_tecnico
                WHERE o.numero = ?
                ORDER BY o.data_criacao DESC
                LIMIT 1
            """, (numero,))
            resultado = cursor.fetchone()
            conn.close()
            
            if not resultado:
                self.edit_status_label.configure(text=f"❌ OS {numero} não encontrada!", text_color=COLORS['danger'])
                self.habilitar_edicao(False)
                return
            
            # Preencher campos
            self.os_selecionada_id = resultado[0]
            self.edit_id_os.delete(0, "end")
            self.edit_id_os.insert(0, str(resultado[0]))
            
            self.edit_numero.delete(0, "end")
            self.edit_numero.insert(0, resultado[1])
            
            self.edit_wan.delete(0, "end")
            self.edit_wan.insert(0, resultado[4] if resultado[4] else "")
            
            tipo_map = {1: "1 - Apoio", 2: "2 - Reparo", 3: "3 - Ativação"}
            self.edit_tipo.set(tipo_map.get(resultado[6], "2 - Reparo"))
            
            status_map = {0: "0 - Suspenso", 1: "1 - Concluído"}
            self.edit_status.set(status_map.get(resultado[7], "0 - Suspenso"))
            
            self.edit_data.delete(0, "end")
            self.edit_data.insert(0, resultado[8] if resultado[8] else "")
            
            self.edit_inicio.delete(0, "end")
            self.edit_inicio.insert(0, resultado[9] if resultado[9] else "")
            
            self.edit_fim.delete(0, "end")
            self.edit_fim.insert(0, resultado[10] if resultado[10] else "")
            
            self.edit_tecnico.set(resultado[3] if resultado[3] else "")
            
            self.edit_carimbo.delete("1.0", "end")
            self.edit_carimbo.insert("1.0", resultado[5] if resultado[5] else "")
            
            self.habilitar_edicao(True)
            self.edit_status_label.configure(text=f"✅ OS {numero} carregada. Edite os campos e clique em Salvar.", text_color=COLORS['success'])
            
        except Exception as e:
            self.edit_status_label.configure(text=f"❌ Erro: {e}", text_color=COLORS['danger'])

    def salvar_edicao_os(self):
        if not self.os_selecionada_id:
            messagebox.showwarning("Aviso", "Nenhuma OS selecionada! Busque uma OS primeiro.")
            return
        
        id_os = self.edit_id_os.get()
        numero = self.edit_numero.get().strip()
        wan = self.edit_wan.get().strip()
        tipo_texto = self.edit_tipo.get()
        status_texto = self.edit_status.get()
        data = self.edit_data.get().strip()
        inicio = self.edit_inicio.get().strip()
        fim = self.edit_fim.get().strip()
        tecnico_nome = self.edit_tecnico.get().strip()
        carimbo = self.edit_carimbo.get("1.0", "end-1c")
        
        if not numero:
            messagebox.showwarning("Aviso", "O Nº OS é obrigatório!")
            return
        
        tipo_map = {"1 - Apoio": 1, "2 - Reparo": 2, "3 - Ativação": 3}
        tipo = tipo_map.get(tipo_texto, 2)
        status = 1 if "Concluído" in status_texto else 0
        
        try:
            conn = self.con.conectar()
            cursor = conn.cursor()
            
            # Buscar ou criar técnico
            cursor.execute("SELECT id FROM tecnicos WHERE nome = ?", (tecnico_nome,))
            tecnico = cursor.fetchone()
            if tecnico:
                id_tecnico = tecnico[0]
            else:
                cursor.execute("INSERT INTO tecnicos (nome, matricula) VALUES (?, ?)", (tecnico_nome, ""))
                id_tecnico = cursor.lastrowid
                self.carregar_tecnicos()
            
            cursor.execute("""
                UPDATE ordem_servico 
                SET numero = ?, id_tecnico = ?, wan_piloto = ?, carimbo = ?,
                    tipo = ?, status = ?, data = ?, inicio_execucao = ?, fim_execucao = ?
                WHERE id_os = ?
            """, (numero, id_tecnico, wan, carimbo, tipo, status, data, inicio, fim, id_os))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Sucesso", "OS atualizada com sucesso!")
            self.edit_status_label.configure(text="✅ OS salva com sucesso!", text_color=COLORS['success'])
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")

    def limpar_busca(self):
        self.busca_numero_entry.delete(0, "end")
        self.limpar_campos_edicao()
        self.edit_status_label.configure(text="")
        self.habilitar_edicao(False)

    def limpar_campos_edicao(self):
        self.edit_numero.delete(0, "end")
        self.edit_wan.delete(0, "end")
        self.edit_tecnico.set("")
        self.edit_tipo.set("2 - Reparo")
        self.edit_status.set("0 - Suspenso")
        self.edit_data.delete(0, "end")
        self.edit_inicio.delete(0, "end")
        self.edit_fim.delete(0, "end")
        self.edit_carimbo.delete("1.0", "end")
        self.os_selecionada_id = None