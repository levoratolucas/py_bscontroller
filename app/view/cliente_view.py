from app.controller.cliente_controller import ClienteController

def menu_cliente():
    cliente_controller = ClienteController()
    
    while True:
        print("\n--- GERENCIAR CLIENTES ---")
        print("1 - Inserir Cliente")
        print("2 - Listar Clientes")
        print("0 - Voltar")
        
        op = input("Escolha: ")
        
        if op == "1":
            nome = input("Nome do cliente: ")
            resultado = cliente_controller.inserir_cliente(nome)
            print(f"✅ {resultado}")
            
        elif op == "2":
            clientes = cliente_controller.listar_clientes()
            if clientes:
                print("\n📋 LISTA DE CLIENTES:")
                print("-" * 40)
                for c in clientes:
                    print(f"ID: {c.id_cliente} | Nome: {c.nome}")
            else:
                print("Nenhum cliente cadastrado.")
                
        elif op == "0":
            break
        else:
            print("Opção inválida!")
            