# app/view/menu_view.py

from app.controller.tecnico_controller import TecnicoController
from app.controller.cliente_controller import ClienteController
from app.controller.endereco_controller import EnderecoController
from app.controller.produto_controller import ProdutoController
from app.bd.cliente_endereco_repository import ClienteEnderecoRepository

def menu():
    tecnico_controller = TecnicoController()
    cliente_controller = ClienteController()
    endereco_controller = EnderecoController()
    produto_controller = ProdutoController()
    cliente_endereco_repo = ClienteEnderecoRepository()

    while True:
        print("\n===== MENU =====")
        print("1 - Criar Técnico")
        print("2 - Listar Técnicos")
        print("3 - Criar Cliente")
        print("4 - Listar Clientes")
        print("5 - Criar Endereço")
        print("6 - Listar Endereços")
        print("7 - Relacionar Cliente x Endereço")
        print("8 - Criar Produto")
        print("9 - Listar Produtos")
        print("0 - Sair")

        op = input("Escolha: ")

        # TECNICO
        if op == "1":
            nome = input("Nome: ")
            matricula = input("Matrícula: ")
            tecnico_controller.inserir_tecnico(nome, matricula)

        elif op == "2":
            tecnicos = tecnico_controller.listar_tecnicos()
            for t in tecnicos:
                print(f"{t.id} - {t.nome} ({t.matricula})")

        # CLIENTE
        elif op == "3":
            nome = input("Nome do cliente: ")
            cliente_controller.inserir_cliente(nome)

        elif op == "4":
            clientes = cliente_controller.listar_clientes()
            for c in clientes:
                print(f"{c.id_cliente} - {c.nome}")

        # ENDERECO
        elif op == "5":
            logradouro = input("Logradouro: ")
            cidade = input("Cidade: ")
            estado = input("Estado: ")
            endereco_controller.inserir_endereco(logradouro, cidade, estado)

        elif op == "6":
            enderecos = endereco_controller.listar_enderecos()
            for e in enderecos:
                print(f"{e.id_endereco} - {e.logradouro}, {e.cidade}/{e.estado}")

        # RELACIONAMENTO
        elif op == "7":
            clientes = cliente_controller.listar_clientes()
            print("Clientes:")
            for c in clientes:
                print(f"{c.id} - {c.nome}")
            id_cliente = int(input("ID Cliente: "))

            enderecos = endereco_controller.listar_enderecos()
            print("Endereços:")
            for e in enderecos:
                print(f"{e.id} - {e.logradouro}")
            id_endereco = int(input("ID Endereço: "))

            cliente_endereco_repo.criar_tabela()
            cliente_endereco_repo.buscar_ou_criar(id_cliente, id_endereco)

        # PRODUTO
        elif op == "8":
            descricao = input("Descrição: ")
            designador = input("Designador: ")
            wan_piloto = input("WAN/Piloto: ")

            print("Relacionamento Cliente-Endereço:")
            # listar relacionamentos
            # simplificado: usuário informa direto
            id_cliente_endereco = int(input("ID Cliente_Endereço: "))

            produto_controller.inserir_produto(
                descricao,
                designador,
                wan_piloto,
                id_cliente_endereco
            )

        elif op == "9":
            produtos = produto_controller.listar_produtos()
            for p in produtos:
                print(f"{p.id_produto} - {p.descricao} | {p.designador} | {p.wan_piloto}")

        elif op == "0":
            break

        else:
            print("Opção inválida")