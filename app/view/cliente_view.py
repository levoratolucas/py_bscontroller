from app.controller.cliente_controller import ClienteController
from app.controller.endereco_controller import EnderecoController
from app.bd.cliente_endereco_repository import ClienteEnderecoRepository
from app.model.cliente_endereco import ClienteEndereco

def menu_cliente():
    cliente_controller = ClienteController()
    endereco_controller = EnderecoController()
    cliente_endereco_repo = ClienteEnderecoRepository()
    
    while True:
        print("\n--- GERENCIAR CLIENTES ---")
        print("1 - Inserir Cliente (com Endereço)")
        print("2 - Adicionar Endereço a Cliente Existente")
        print("3 - Listar Clientes com Endereços")
        print("4 - Listar Apenas Clientes")
        print("0 - Voltar")
        
        op = input("Escolha: ")
        
        if op == "1":
            nome = input("Nome do cliente: ")
            
            # Verificar se cliente já existe
            cliente_existente = cliente_controller.buscar_cliente_por_nome(nome)
            
            if cliente_existente:
                print(f"\n⚠️ Cliente '{nome}' JÁ EXISTE com ID {cliente_existente.id_cliente}")
                resposta = input("Deseja adicionar um novo endereço a este cliente? (s/n): ")
                
                if resposta.lower() == 's':
                    # Adicionar endereço ao cliente existente
                    print("\n--- CADASTRO DE NOVO ENDEREÇO ---")
                    logradouro = input("Logradouro: ")
                    cidade = input("Cidade: ")
                    estado = input("Estado: ")
                    
                    endereco = endereco_controller.inserir_endereco(logradouro, cidade, estado)
                    
                    if endereco and endereco.id_endereco is not None:
                        relacionamento = ClienteEndereco(cliente_existente.id_cliente, endereco.id_endereco)
                        cliente_endereco_repo.inserir(relacionamento)
                        print(f"\n✅ Novo endereço adicionado ao cliente '{nome}'!")
                    else:
                        print("❌ Erro ao cadastrar endereço")
                else:
                    print("Operação cancelada.")
                continue  # Volta ao início do loop
            
            # Se cliente não existe, prosseguir com cadastro completo
            print("\n--- CADASTRO DE ENDEREÇO ---")
            logradouro = input("Logradouro: ")
            cidade = input("Cidade: ")
            estado = input("Estado: ")
            
            # Inserir cliente
            cliente = cliente_controller.inserir_cliente(nome)
            
            # Verificar se cliente foi inserido
            if cliente and cliente.id_cliente is not None:
                # Inserir endereço
                endereco = endereco_controller.inserir_endereco(logradouro, cidade, estado)
                
                if endereco and endereco.id_endereco is not None:
                    # Criar relacionamento
                    relacionamento = ClienteEndereco(cliente.id_cliente, endereco.id_endereco)
                    cliente_endereco_repo.inserir(relacionamento)
                    print(f"\n✅ Cliente '{nome}' cadastrado com sucesso!")
                    print(f"✅ Endereço '{logradouro}' vinculado ao cliente!")
                else:
                    print("❌ Erro ao cadastrar endereço")
            else:
                print("❌ Erro ao cadastrar cliente")
                
        elif op == "2":
            # Adicionar novo endereço a cliente existente
            clientes = cliente_controller.listar_clientes()
            if not clientes:
                print("❌ Nenhum cliente cadastrado.")
                continue
                
            print("\n📋 CLIENTES DISPONÍVEIS:")
            for c in clientes:
                print(f"ID: {c.id_cliente} | Nome: {c.nome}")
            
            try:
                id_cliente = int(input("\nID do cliente: "))
            except ValueError:
                print("❌ ID inválido!")
                continue
            
            # Verificar se cliente existe
            cliente_existe = None
            for c in clientes:
                if c.id_cliente == id_cliente:
                    cliente_existe = c
                    break
                    
            if not cliente_existe:
                print("❌ Cliente não encontrado!")
                continue
            
            print(f"\n--- ADICIONAR ENDEREÇO PARA: {cliente_existe.nome} ---")
            logradouro = input("Logradouro: ")
            cidade = input("Cidade: ")
            estado = input("Estado: ")
            
            # Inserir endereço
            endereco = endereco_controller.inserir_endereco(logradouro, cidade, estado)
            
            if endereco and endereco.id_endereco is not None:
                # Criar relacionamento
                relacionamento = ClienteEndereco(id_cliente, endereco.id_endereco)
                cliente_endereco_repo.inserir(relacionamento)
                print(f"\n✅ Endereço '{logradouro}' adicionado ao cliente {cliente_existe.nome}!")
            else:
                print("❌ Erro ao cadastrar endereço")
                
        elif op == "3":
            # Listar clientes com todos os seus endereços
            relacionamentos = cliente_endereco_repo.listar()
            
            if not relacionamentos:
                print("Nenhum relacionamento cliente-endereço encontrado.")
                continue
                
            print("\n📋 CLIENTES E SEUS ENDEREÇOS:")
            print("=" * 60)
            
            # Agrupar endereços por cliente
            clientes_dict = {}
            for rel in relacionamentos:
                if rel.id_cliente not in clientes_dict:
                    clientes_dict[rel.id_cliente] = []
                clientes_dict[rel.id_cliente].append(rel.id_endereco)
            
            # Buscar informações completas
            clientes = cliente_controller.listar_clientes()
            enderecos = endereco_controller.listar_enderecos()
            
            # Criar dicionários para busca rápida
            clientes_info = {c.id_cliente: c.nome for c in clientes}
            enderecos_info = {e.id_endereco: f"{e.logradouro}, {e.cidade}/{e.estado}" for e in enderecos}
            
            # Exibir
            for id_cliente, enderecos_ids in clientes_dict.items():
                nome_cliente = clientes_info.get(id_cliente, "Desconhecido")
                print(f"\n👤 Cliente: {nome_cliente} (ID: {id_cliente})")
                print("   Endereços:")
                for id_endereco in enderecos_ids:
                    endereco_str = enderecos_info.get(id_endereco, "Endereço não encontrado")
                    print(f"     📍 {endereco_str}")
                    
        elif op == "4":
            # Listar apenas clientes (sem endereços)
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