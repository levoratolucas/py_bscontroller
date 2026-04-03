def selecionar_ou_criar_tecnico(tecnico_controller):
    """Função para selecionar técnico existente ou criar novo"""
    while True:
        print("\n--- TÉCNICO RESPONSÁVEL ---")
        print("1 - Selecionar técnico existente")
        print("2 - Cadastrar novo técnico")
        
        opcao = input("Escolha: ")
        
        if opcao == "1":
            tecnicos = tecnico_controller.listar_tecnicos()
            if not tecnicos:
                print("❌ Nenhum técnico cadastrado. Cadastre um primeiro.")
                continue
            
            print("\n📋 TÉCNICOS DISPONÍVEIS:")
            for t in tecnicos:
                print(f"ID: {t.id} | Nome: {t.nome} | Matrícula: {t.matricula}")
            
            try:
                id_tecnico = int(input("\nID do Técnico: "))
                for t in tecnicos:
                    if t.id == id_tecnico:
                        return id_tecnico
                print("❌ ID inválido!")
            except ValueError:
                print("❌ ID inválido!")
                
        elif opcao == "2":
            print("\n--- CADASTRO DE NOVO TÉCNICO ---")
            nome = input("Nome: ")
            matricula = input("Matrícula: ")
            
            resultado = tecnico_controller.inserir_tecnico(nome, matricula)
            print(f"✅ {resultado}")
            
            tecnicos = tecnico_controller.listar_tecnicos()
            for t in tecnicos:
                if t.nome == nome and t.matricula == matricula:
                    return t.id
        else:
            print("Opção inválida!")