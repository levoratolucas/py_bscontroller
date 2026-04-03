from app.controller.ordem_servico_controller import OrdemServicoController
from app.controller.tecnico_controller import TecnicoController
from app.controller.produto_controller import ProdutoController
from app.controller.cliente_controller import ClienteController
from app.controller.endereco_controller import EnderecoController
from app.bd.cliente_endereco_repository import ClienteEnderecoRepository

from app.view.ordem_servico.criar_os import criar_ordem_servico
from app.view.ordem_servico.listar_os import listar_todas_os, listar_os_por_tecnico
from app.view.ordem_servico.buscar_os import buscar_os_por_id
# from app.view.ordem_servico.concluir_os import concluir_os

def menu_ordem_servico():
    os_controller = OrdemServicoController()
    tecnico_controller = TecnicoController()
    produto_controller = ProdutoController()
    cliente_controller = ClienteController()
    endereco_controller = EnderecoController()
    cliente_endereco_repo = ClienteEnderecoRepository()
    
    while True:
        print("\n" + "="*50)
        print("       ORDEM DE SERVIÇO - OS")
        print("="*50)
        print("1 - Criar Nova OS")
        print("2 - Listar Todas OS")
        print("3 - Buscar OS por ID")
        print("4 - Concluir OS")
        print("5 - Listar OS por Técnico")
        print("0 - Voltar")
        print("-"*50)
        
        op = input("Escolha: ")
        
        if op == "1":
            criar_ordem_servico(os_controller, tecnico_controller, produto_controller, 
                               cliente_controller, endereco_controller, cliente_endereco_repo)
        
        elif op == "2":
            listar_todas_os(os_controller, tecnico_controller, produto_controller, 
                           cliente_controller, endereco_controller, cliente_endereco_repo)
        
        elif op == "3":
            buscar_os_por_id(os_controller, tecnico_controller, produto_controller,
                            cliente_controller, endereco_controller, cliente_endereco_repo)
        
        elif op == "4":
            print("ok")
        
        elif op == "5":
            listar_os_por_tecnico(os_controller, tecnico_controller, produto_controller,
                                 cliente_controller, endereco_controller, cliente_endereco_repo)
        
        elif op == "0":
            break
        else:
            print("Opção inválida!")