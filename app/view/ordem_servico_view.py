# app/view/ordem_servico_view.py

from app.controller.ordem_servico_controller import OrdemServicoController
from app.bd.tecnico_repository import TecnicoRepository
from app.bd.cliente_repository import ClienteRepository
from app.bd.endereco_repository import EnderecoRepository
from app.bd.cliente_endereco_repository import ClienteEnderecoRepository
from app.bd.produto_repository import ProdutoRepository

def mostrar_menu():
    tecnico_repo = TecnicoRepository()
    cliente_repo = ClienteRepository()
    endereco_repo = EnderecoRepository()
    cliente_endereco_repo = ClienteEnderecoRepository()
    produto_repo = ProdutoRepository()
    ordem_controller = OrdemServicoController()

    tecnico_repo.criar_tabela()
    cliente_repo.criar_tabela()
    endereco_repo.criar_tabela()
    cliente_endereco_repo.criar_tabela()
    produto_repo.criar_tabela()

    print("\nInserção de Ordem de Serviço (carimbo manual)")

    tecnico_nome = input("Nome do técnico: ")
    tecnico_matricula = input("Matrícula do técnico: ")
    tecnico = tecnico_repo.buscar_ou_criar(tecnico_nome, tecnico_matricula)

    cliente_nome = input("Nome do cliente: ")
    cliente = cliente_repo.buscar_ou_criar(cliente_nome)

    logradouro = input("Endereço: ")
    cidade = input("Cidade: ")
    estado = input("Estado: ")
    endereco = endereco_repo.buscar_ou_criar(logradouro, cidade, estado)

    id_cliente_endereco = cliente_endereco_repo.buscar_ou_criar(cliente.id, endereco.id)

    descricao = input("Descrição do produto: ")
    designador = input("Designador: ")
    wan_piloto = input("WAN/Piloto: ")

    produto = produto_repo.buscar_ou_criar(
        descricao,
        designador,
        wan_piloto,
        id_cliente_endereco
    )

    ordem_controller.inserir_ordem(
        id_tecnico=tecnico.id,
        id_produto=produto.id,
        causa_raiz=input("Causa raiz: "),
        materiais_utilizados=input("Materiais utilizados: "),
        acao=input("Ação: "),
        contato_responsavel=input("Contato do responsável: "),
        observacoes=input("Observações: "),
        data_criacao=input("Data de criação (AAAA-MM-DD): "),
        concluida=(input("Está concluída? (s/n): ").lower() == 's'),
        data_conclusao=input("Data de conclusão: ")
    )

    print("Ordem de serviço inserida com sucesso!")