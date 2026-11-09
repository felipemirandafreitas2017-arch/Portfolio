from flask import Flask, request, jsonify
from dao import ProjetoDAO, MensagemDAO
from models import Projeto, Mensagem

app = Flask(__name__)

# Instâncias dos repositórios usados pela API.
projeto_dao = ProjetoDAO()
mensagem_dao = MensagemDAO()


# Rotas para gerenciar projetos.
@app.route("/projetos", methods=["GET"])
def listar_projetos():
    projetos = projeto_dao.listar()
    return jsonify([projeto.to_dict() for projeto in projetos])


@app.route("/projetos", methods=["POST"])
def cadastrar_projeto():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"mensagem": "Dados incompletos!"}), 400

    try:
        projeto = Projeto.from_dict(dados)
    except (KeyError, TypeError):
        return jsonify({"mensagem": "Dados incompletos!"}), 400

    id_projeto = projeto_dao.cadastrar(projeto)

    return jsonify({
        "mensagem": "Projeto cadastrado com sucesso!",
        "id_projeto": id_projeto,
    }), 201


@app.route("/projetos/<int:id_projeto>", methods=["PUT"])
def atualizar_projeto(id_projeto):
    dados = request.get_json()
    atualizado = projeto_dao.atualizar(id_projeto, dados)

    if atualizado:
        return jsonify({"mensagem": "Projeto atualizado com sucesso!"})

    return jsonify({"mensagem": "Projeto não encontrado!"}), 404


@app.route("/projetos/<int:id_projeto>", methods=["DELETE"])
def excluir_projeto(id_projeto):
    excluido = projeto_dao.excluir(id_projeto)

    if excluido:
        return jsonify({"mensagem": "Projeto excluído com sucesso!"})

    return jsonify({"mensagem": "Projeto não encontrado!"}), 404


# Rotas para gerenciar mensagens de contato.
@app.route("/mensagens", methods=["GET"])
def listar_mensagens():
    mensagens = mensagem_dao.listar()
    return jsonify([mensagem.to_dict() for mensagem in mensagens])


@app.route("/mensagens", methods=["POST"])
def cadastrar_mensagem():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"mensagem": "Dados incompletos!"}), 400

    try:
        mensagem = Mensagem.from_dict(dados)
    except (KeyError, TypeError):
        return jsonify({"mensagem": "Dados incompletos!"}), 400

    id_mensagem = mensagem_dao.cadastrar(mensagem)

    return jsonify({
        "mensagem": "Mensagem enviada com sucesso!",
        "id": id_mensagem,
    }), 201


if __name__ == "__main__":
    app.run(debug=True)