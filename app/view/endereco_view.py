from app.controller.endereco_controller import EnderecoController

def menu_endereco():
    endereco_controller = EnderecoController()
    
    while True:
        print("\n--- GERENCIAR ENDEREÇOS ---")
        print("1 - Inserir Endereço")
        print("2 - Listar Endereços")
        print("0 - Voltar")
        
        op = input("Escolha: ")
        
        if op == "1":
            logradouro = input("Logradouro: ")
            cidade = input("Cidade: ")
            estado = input("Estado: ")
            resultado = endereco_controller.inserir_endereco(logradouro, cidade, estado)
            print(f"✅ {resultado}")
            
        elif op == "2":
            enderecos = endereco_controller.listar_enderecos()
            if enderecos:
                print("\n📋 LISTA DE ENDEREÇOS:")
                print("-" * 50)
                for e in enderecos:
                    print(f"ID: {e.id_endereco} | {e.logradouro}, {e.cidade}/{e.estado}")
            else:
                print("Nenhum endereço cadastrado.")
                
        elif op == "0":
            break
        else:
            print("Opção inválida!")