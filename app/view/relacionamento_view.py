from app.controller.cliente_controller import ClienteController
from app.controller.endereco_controller import EnderecoController
from app.bd.cliente_endereco_repository import ClienteEnderecoRepository

def menu_relacionamento():
    cliente_controller = ClienteController()
    endereco_controller = EnderecoController()
    cliente_endereco_repo = ClienteEnderecoRepository()
    
    while True:
        print("\n--- RELACIONAR CLIENTE x ENDEREÇO ---")
        print("1 - Criar Relacionamento")
        print("2 - Listar Relacionamentos")
        print("0 - Voltar")
        
        op = input("Escolha: ")
        
        if op == "1":
            # Listar clientes
            clientes = cliente_controller.listar_clientes()
            if not clientes:
                print("❌ Nenhum cliente cadastrado. Cadastre um cliente primeiro.")
                continue
                
            print("\n📋 CLIENTES DISPONÍVEIS:")
            for c in clientes:
                print(f"ID: {c.id_cliente} | Nome: {c.nome}")
            id_cliente = int(input("\nID do Cliente: "))
            
            # Listar endereços
            enderecos = endereco_controller.listar_enderecos()
            if not enderecos:
                print("❌ Nenhum endereço cadastrado. Cadastre um endereço primeiro.")
                continue
                
            print("\n📋 ENDEREÇOS DISPONÍVEIS:")
            for e in enderecos:
                print(f"ID: {e.id_endereco} | {e.logradouro}, {e.cidade}/{e.estado}")
            id_endereco = int(input("ID do Endereço: "))
            
            # Criar relacionamento
            cliente_endereco_repo.criar_tabela()
            resultado = cliente_endereco_repo.buscar_ou_criar(id_cliente, id_endereco)
            print(f"✅ Relacionamento criado com sucesso!")
            
        elif op == "2":
            # Buscar e mostrar relacionamentos
            # (Você precisará implementar um método listar_relacionamentos no repository)
            print("📋 LISTA DE RELACIONAMENTOS:")
            # relacionamentos = cliente_endereco_repo.listar_todos()
            # for r in relacionamentos:
            #     print(f"ID: {r.id} | Cliente: {r.id_cliente} | Endereço: {r.id_endereco}")
            print("(Implementar método listar_relacionamentos)")
            
        elif op == "0":
            break
        else:
            print("Opção inválida!")