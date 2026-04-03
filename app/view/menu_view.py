from app.view.tecnico_view import menu_tecnico
from app.view.cliente_view import menu_cliente
from app.view.endereco_view import menu_endereco
from app.view.produto_view import menu_produto
from app.view.relacionamento_view import menu_relacionamento

def menu():
    while True:
        print("\n" + "="*50)
        print("       SISTEMA DE ORDEM DE SERVIÇO")
        print("="*50)
        print("1 - Gerenciar Técnicos")
        print("2 - Gerenciar Clientes")
        print("3 - Gerenciar Endereços")
        print("4 - Gerenciar Produtos")
        print("5 - Relacionar Cliente x Endereço")
        print("0 - Sair")
        print("-"*50)

        op = input("Escolha uma opção: ")

        if op == "1":
            menu_tecnico()
        elif op == "2":
            menu_cliente()
        elif op == "3":
            menu_endereco()
        elif op == "4":
            menu_produto()
        elif op == "5":
            menu_relacionamento()
        elif op == "0":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida! Tente novamente.")