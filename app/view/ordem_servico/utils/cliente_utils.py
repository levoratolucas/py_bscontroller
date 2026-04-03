from app.model.cliente_endereco import ClienteEndereco
from app.view.ordem_servico.utils.endereco_utils import cadastrar_novo_endereco

from app.model.cliente_endereco import ClienteEndereco
from app.view.ordem_servico.utils.endereco_utils import cadastrar_novo_endereco

def selecionar_cliente_existente(cliente_controller, endereco_controller, cliente_endereco_repo, produto_controller=None):
    """Selecionar cliente existente, seu endereço e produto"""
    while True:
        clientes = cliente_controller.listar_clientes()
        if not clientes:
            print("❌ Nenhum cliente cadastrado.")
            return None, None, None, False  # Agora retorna produto também
        
        print("\n📋 CLIENTES DISPONÍVEIS:")
        for c in clientes:
            print(f"ID: {c.id_cliente} | Nome: {c.nome}")
        
        try:
            id_cliente = int(input("\nID do Cliente: "))
            
            cliente_existe = None
            for c in clientes:
                if c.id_cliente == id_cliente:
                    cliente_existe = c
                    break
            
            if not cliente_existe:
                print("❌ Cliente não encontrado!")
                continue
            
            # Buscar endereços deste cliente
            relacionamentos = cliente_endereco_repo.buscar_por_cliente(id_cliente)
            
            if not relacionamentos:
                print(f"\n⚠️ Cliente '{cliente_existe.nome}' não possui endereços cadastrados!")
                resposta = input("Deseja cadastrar um endereço agora? (s/n): ")
                if resposta.lower() == 's':
                    id_endereco = cadastrar_novo_endereco(endereco_controller)
                    if id_endereco:
                        relacionamento = ClienteEndereco(id_cliente, id_endereco)
                        cliente_endereco_repo.inserir(relacionamento)
                        print(f"✅ Endereço vinculado ao cliente {cliente_existe.nome}!")
                        # Após cadastrar endereço, vai para cadastro de produto
                        print("\n🆕 NOVO ENDEREÇO DETECTADO!")
                        print("Vamos cadastrar o produto agora.")
                        return id_cliente, id_endereco, None, True  # True = novo endereço, produto virá depois
                continue
            
            # Mostrar endereços E produtos juntos
            print(f"\n📋 ENDEREÇOS E PRODUTOS DO CLIENTE: {cliente_existe.nome}")
            print("-" * 60)
            
            enderecos = endereco_controller.listar_enderecos()
            enderecos_dict = {e.id_endereco: e for e in enderecos}
            
            # Buscar todos os produtos do cliente
            todos_produtos = []
            if produto_controller:
                todos_produtos = produto_controller.listar_produtos()
            
            # Dicionário para mapear relacionamento -> produto
            rel_produto = {}
            for p in todos_produtos:
                rel_produto[p.id_cliente_endereco] = p
            
            opcoes = []
            for i, rel in enumerate(relacionamentos, 1):
                endereco = enderecos_dict.get(rel.id_endereco)
                if endereco:
                    endereco_str = f"{endereco.logradouro}, {endereco.cidade}/{endereco.estado}"
                    
                    # Verificar se tem produto para este endereço
                    produto = rel_produto.get(rel.id)
                    if produto:
                        produto_str = f" [Produto: {produto.descricao} - WAN: {produto.wan_piloto}]"
                        opcoes.append((rel.id, endereco_str, produto.id_produto, rel.id_endereco))
                        print(f"{i} - {endereco_str}{produto_str}")
                    else:
                        opcoes.append((rel.id, endereco_str, None, rel.id_endereco))
                        print(f"{i} - {endereco_str} [⚠️ Sem produto cadastrado]")
            
            print(f"{len(relacionamentos)+1} - Cadastrar novo endereço")
            print(f"{len(relacionamentos)+2} - Cadastrar novo produto para endereço existente")
            
            escolha = int(input("\nEscolha uma opção: "))
            
            if 1 <= escolha <= len(relacionamentos):
                # Escolheu endereço existente
                id_rel, endereco_str, id_produto, id_endereco = opcoes[escolha-1]
                
                if id_produto:
                    # Tem produto, retorna tudo
                    print(f"\n✅ Produto selecionado!")
                    return id_cliente, id_endereco, id_produto, False
                else:
                    # Não tem produto, pergunta se quer cadastrar
                    print(f"\n⚠️ Este endereço não possui produto cadastrado!")
                    resposta = input("Deseja cadastrar um produto agora? (s/n): ")
                    if resposta.lower() == 's':
                        return id_cliente, id_endereco, None, True  # True = precisa cadastrar produto
                    else:
                        print("❌ Operação cancelada!")
                        return None, None, None, False
                        
            elif escolha == len(relacionamentos)+1:
                # Cadastrar novo endereço
                id_endereco = cadastrar_novo_endereco(endereco_controller)
                if id_endereco:
                    relacionamento = ClienteEndereco(id_cliente, id_endereco)
                    cliente_endereco_repo.inserir(relacionamento)
                    print(f"✅ Novo endereço vinculado ao cliente {cliente_existe.nome}!")
                    return id_cliente, id_endereco, None, True  # True = novo endereço, precisa cadastrar produto
                    
            elif escolha == len(relacionamentos)+2:
                # Cadastrar novo produto para endereço existente
                print("\n📋 ENDEREÇOS DISPONÍVEIS PARA CADASTRAR PRODUTO:")
                for i, (id_rel, endereco_str, _, id_endereco) in enumerate(opcoes, 1):
                    print(f"{i} - {endereco_str}")
                
                sub_escolha = int(input("\nEscolha o endereço: "))
                if 1 <= sub_escolha <= len(opcoes):
                    id_rel, _, _, id_endereco = opcoes[sub_escolha-1]
                    print(f"\n🆕 Vamos cadastrar um produto para este endereço!")
                    return id_cliente, id_endereco, None, True  # True = precisa cadastrar produto
                else:
                    print("❌ Opção inválida!")
                    continue
            else:
                print("❌ Opção inválida!")
                
        except ValueError:
            print("❌ Opção inválida!")
    
    return None, None, None, False


def cadastrar_novo_cliente(cliente_controller, endereco_controller, cliente_endereco_repo):
    """Cadastrar novo cliente com endereço"""
    print("\n--- CADASTRO DE NOVO CLIENTE ---")
    nome = input("Nome do cliente: ")
    
    print("\n--- CADASTRO DE ENDEREÇO ---")
    logradouro = input("Logradouro: ")
    cidade = input("Cidade: ")
    estado = input("Estado: ")
    
    cliente = cliente_controller.inserir_cliente(nome)
    
    if cliente and cliente.id_cliente is not None:
        endereco = endereco_controller.inserir_endereco(logradouro, cidade, estado)
        
        if endereco and endereco.id_endereco is not None:
            relacionamento = ClienteEndereco(cliente.id_cliente, endereco.id_endereco)
            cliente_endereco_repo.inserir(relacionamento)
            print(f"\n✅ Cliente '{nome}' cadastrado com sucesso!")
            print(f"✅ Endereço vinculado ao cliente!")
            return cliente.id_cliente, endereco.id_endereco, True
        else:
            print("❌ Erro ao cadastrar endereço")
    else:
        print("❌ Erro ao cadastrar cliente")
    
    return None, None, False