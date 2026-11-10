from flask import Flask, request, jsonify
from flask_cors import CORS
from mysql.connector import Error

# Importa as classes que acessam os dados do banco e os modelos de negócio.
from dao import ProjetoDAO, MensagemDAO
from models import Projeto, Mensagem

# Cria a aplicação Flask e habilita o acesso vindo do frontend.
app = Flask(__name__)
CORS(app)

# Cria os objetos DAO para separar a lógica de banco da lógica da API.
projeto_dao = ProjetoDAO()
mensagem_dao = MensagemDAO()


@app.route("/", methods=["GET"])
def inicio():
    # Endpoint simples para confirmar que a API está funcionando.
    return jsonify({"mensagem": "API do Portfólio funcionando!"})


# Rotas para listar, cadastrar, atualizar e excluir projetos.
@app.route("/projetos", methods=["GET"])
def listar_projetos():
    # Busca todos os projetos no banco e transforma em JSON.
    projetos = projeto_dao.listar()
    return jsonify([projeto.to_dict() for projeto in projetos])


@app.route("/projetos", methods=["POST"])
def cadastrar_projeto():
    # Lê os dados enviados no corpo da requisição em JSON.
    dados = request.get_json(silent=True)

    # Valida se os campos essenciais foram preenchidos.
    if not isinstance(dados, dict) or not dados.get("titulo") or not dados.get("descricao"):
        return jsonify({"mensagem": "Informe título e descrição do projeto."}), 400

    # Cria o objeto Projeto com os dados recebidos.
    projeto = Projeto.from_dict(dados)
    id_projeto = projeto_dao.cadastrar(projeto)

    # Retorna uma resposta de sucesso com o ID do novo projeto.
    return jsonify({
        "mensagem": "Projeto cadastrado com sucesso!",
        "id_projeto": id_projeto
    }), 201


@app.route("/projetos/<int:id_projeto>", methods=["PUT"])
def atualizar_projeto(id_projeto):
    # Recebe os dados para alterar um projeto existente.
    dados = request.get_json(silent=True)

    # Garante que o título e a descrição sejam enviados.
    if not isinstance(dados, dict) or not dados.get("titulo") or not dados.get("descricao"):
        return jsonify({"mensagem": "Informe título e descrição do projeto."}), 400

    # Cria o objeto atualizado e tenta salvar no banco.
    projeto = Projeto.from_dict(dados)
    atualizado = projeto_dao.atualizar(id_projeto, projeto)

    if atualizado:
        return jsonify({"mensagem": "Projeto atualizado com sucesso!"})

    return jsonify({"mensagem": "Projeto não encontrado!"}), 404


@app.route("/projetos/<int:id_projeto>", methods=["DELETE"])
def excluir_projeto(id_projeto):
    # Remove o projeto pelo ID informado.
    excluido = projeto_dao.excluir(id_projeto)

    if excluido:
        return jsonify({"mensagem": "Projeto excluído com sucesso!"})

    return jsonify({"mensagem": "Projeto não encontrado!"}), 404


# Rotas para listar e cadastrar mensagens de contato.
@app.route("/mensagens", methods=["GET"])
def listar_mensagens():
    # Busca todas as mensagens e as devolve em formato JSON.
    mensagens = mensagem_dao.listar()
    return jsonify([mensagem.to_dict() for mensagem in mensagens])


@app.route("/mensagens", methods=["POST"])
def cadastrar_mensagem():
    # Lê a mensagem enviada pelo formulário ou cliente.
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"mensagem": "Envie os dados da mensagem em JSON."}), 400

    # Cria o objeto Mensagem com os dados recebidos.
    mensagem = Mensagem.from_dict(dados)

    # Verifica se os campos principais foram preenchidos.
    if not mensagem.nome or not mensagem.email or not mensagem.texto:
        return jsonify({"mensagem": "Preencha nome, e-mail e mensagem."}), 400

    # Valida o CEP informado antes de salvar.
    if not mensagem.cep.cep or len(mensagem.cep.cep) != 8:
        return jsonify({"mensagem": "Informe um CEP válido com 8 números."}), 400

    id_mensagem = mensagem_dao.cadastrar(mensagem)

    # Responde com sucesso após salvar a mensagem.
    return jsonify({
        "mensagem": "Mensagem enviada com sucesso!",
        "id": id_mensagem
    }), 201


@app.errorhandler(Error)
def erro_banco(error):
    # Captura erros de conexão com o banco e responde ao cliente.
    return jsonify({"mensagem": "Não foi possível acessar o banco de dados."}), 500


if __name__ == "__main__":
    # Inicia o servidor Flask em modo de desenvolvimento.
    app.run(debug=True)
