from app.controller.tecnico_controller import TecnicoController

def menu_tecnico():
    tecnico_controller = TecnicoController()
    
    while True:
        print("\n--- GERENCIAR TÉCNICOS ---")
        print("1 - Inserir Técnico")
        print("2 - Listar Técnicos")
        print("0 - Voltar")
        
        op = input("Escolha: ")
        
        if op == "1":
            nome = input("Nome: ")
            matricula = input("Matrícula: ")
            resultado = tecnico_controller.inserir_tecnico(nome, matricula)
            print(f"✅ {resultado}")
            
        elif op == "2":
            tecnicos = tecnico_controller.listar_tecnicos()
            if tecnicos:
                print("\n📋 LISTA DE TÉCNICOS:")
                print("-" * 40)
                for t in tecnicos:
                    print(f"ID: {t.id} | Nome: {t.nome} | Matrícula: {t.matricula}")
            else:
                print("Nenhum técnico cadastrado.")
                
        elif op == "0":
            break
        else:
            print("Opção inválida!")