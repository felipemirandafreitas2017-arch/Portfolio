import hmac
import os
import secrets

from flask import Flask, request, jsonify, session
from flask_cors import CORS
from mysql.connector import Error

from dao import ProjetoDAO, MensagemDAO
from models import Projeto, Mensagem

app = Flask(__name__)
# Define a chave usada para proteger os dados da sessão.
# Se não houver uma chave configurada, a chave temporária mantém o app executável,
# mas as sessões existentes deixam de ser válidas quando o processo reinicia.
app.secret_key = os.getenv("FLASK_SECRET_KEY") or secrets.token_hex(32)

app.config["SESSION_COOKIE_HTTPONLY"] = True
# Cookies Secure só são enviados por HTTPS; SameSite é ajustado junto dessa opção
# para permitir ou restringir o envio do cookie em requisições entre origens.
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"
app.config["SESSION_COOKIE_SECURE"] = COOKIE_SECURE
app.config["SESSION_COOKIE_SAMESITE"] = os.getenv(
    "COOKIE_SAMESITE", "None" if COOKIE_SECURE else "Lax"
)

ORIGEM_FRONTEND = os.getenv(
    "FRONTEND_ORIGIN",
    "http://127.0.0.1:5500"
)

# Permite requisições do frontend configurado.
CORS(app, supports_credentials=True, origins=[ORIGEM_FRONTEND])

SENHA_ADMIN = os.getenv("ADMIN_PASSWORD")


def administrador_logado():
    return session.get("administrador") is True


# Protege operações administrativas com sessão e token CSRF.
# A sessão identifica o administrador; o token adicional exige que a interface
# autenticada envie o valor associado à sessão nas operações de alteração.
def proteger_requisicao():
    if not administrador_logado():
        return jsonify({
            "mensagem": "Acesso não autorizado. Faça login."
        }), 401

    token_enviado = request.headers.get("X-CSRF-Token", "")
    token_salvo = session.get("csrf_token", "")

    # A comparação em tempo constante evita revelar informações do token
    # pela duração da comparação.
    if not token_salvo or not hmac.compare_digest(
        token_enviado, token_salvo
    ):
        return jsonify({
            "mensagem": "Requisição não autorizada."
        }), 403

    return None


projeto_dao = ProjetoDAO()
mensagem_dao = MensagemDAO()


@app.route("/", methods=["GET"])
def inicio():
    return jsonify({
        "mensagem": "API do Portfólio funcionando!"
    })


# Consulta pública dos projetos disponíveis.
@app.route("/projetos", methods=["GET"])
def listar_projetos():
    projetos = projeto_dao.listar()

    return jsonify([
        projeto.to_dict() for projeto in projetos
    ])


@app.route("/projetos", methods=["POST"])
def cadastrar_projeto():
    bloqueio = proteger_requisicao()

    if bloqueio:
        return bloqueio

    dados = request.get_json(silent=True)

    if (
        not isinstance(dados, dict)
        or not dados.get("titulo")
        or not dados.get("descricao")
    ):
        return jsonify({
            "mensagem": "Informe título e descrição do projeto."
        }), 400

    projeto = Projeto.from_dict(dados)

    if (
        len(projeto.titulo) > 100
        or len(projeto.descricao) == 0
        or len(projeto.imagem or "") > 255
        or len(projeto.categoria or "") > 60
        or len(projeto.link or "") > 255
    ):
        return jsonify({
            "mensagem": "Verifique os campos e os limites de caracteres do projeto."
        }), 400

    # O DAO devolve o identificador gerado pelo banco para a resposta da API.
    id_projeto = projeto_dao.cadastrar(projeto)

    return jsonify({
        "mensagem": "Projeto cadastrado com sucesso!",
        "id_projeto": id_projeto
    }), 201


@app.route("/projetos/<int:id_projeto>", methods=["PUT"])
def atualizar_projeto(id_projeto):
    bloqueio = proteger_requisicao()

    if bloqueio:
        return bloqueio

    dados = request.get_json(silent=True)

    if (
        not isinstance(dados, dict)
        or not dados.get("titulo")
        or not dados.get("descricao")
    ):
        return jsonify({
            "mensagem": "Informe título e descrição do projeto."
        }), 400

    projeto = Projeto.from_dict(dados)

    if (
        len(projeto.titulo) > 100
        or len(projeto.descricao) == 0
        or len(projeto.imagem or "") > 255
        or len(projeto.categoria or "") > 60
        or len(projeto.link or "") > 255
    ):
        return jsonify({
            "mensagem": "Verifique os campos e os limites de caracteres do projeto."
        }), 400

    atualizado = projeto_dao.atualizar(
        id_projeto, projeto
    )

    if atualizado:
        return jsonify({
            "mensagem": "Projeto atualizado com sucesso!"
        })

    return jsonify({
        "mensagem": "Projeto não encontrado!"
    }), 404


@app.route("/projetos/<int:id_projeto>", methods=["DELETE"])
def excluir_projeto(id_projeto):
    bloqueio = proteger_requisicao()

    if bloqueio:
        return bloqueio

    excluido = projeto_dao.excluir(id_projeto)

    if excluido:
        return jsonify({
            "mensagem": "Projeto excluído com sucesso!"
        })

    return jsonify({
        "mensagem": "Projeto não encontrado!"
    }), 404


# Autenticação e sessão do administrador.
@app.route("/admin/login", methods=["POST"])
def login_admin():
    dados = request.get_json(silent=True) or {}
    senha_digitada = str(dados.get("senha", ""))

    if not SENHA_ADMIN:
        return jsonify({
            "mensagem": "Configure o segredo ADMIN_PASSWORD no Codespaces."
        }), 503

    if not hmac.compare_digest(senha_digitada, SENHA_ADMIN):
        return jsonify({
            "mensagem": "Senha incorreta."
        }), 401

    session.clear()
    session["administrador"] = True
    # O token fica associado à sessão e será enviado pela interface nas operações
    # que alteram dados (POST, PUT e DELETE).
    session["csrf_token"] = secrets.token_hex(32)

    return jsonify({
        "mensagem": "Login realizado com sucesso!",
        "csrf_token": session["csrf_token"]
    })


@app.route("/admin/status", methods=["GET"])
def status_admin():
    if not administrador_logado():
        return jsonify({
            "autenticado": False
        }), 401

    return jsonify({
        "autenticado": True,
        "csrf_token": session.get("csrf_token")
    })


@app.route("/admin/logout", methods=["POST"])
def logout_admin():
    bloqueio = proteger_requisicao()

    if bloqueio:
        return bloqueio

    session.clear()

    return jsonify({
        "mensagem": "Sessão encerrada."
    })


# Rotas de envio e consulta das mensagens de contato.
@app.route("/mensagens", methods=["GET"])
def listar_mensagens():
    bloqueio = proteger_requisicao()

    if bloqueio:
        return bloqueio

    mensagens = mensagem_dao.listar()

    return jsonify([
        mensagem.to_dict() for mensagem in mensagens
    ])


@app.route("/mensagens", methods=["POST"])
def cadastrar_mensagem():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({
            "mensagem": "Envie os dados da mensagem em JSON."
        }), 400

    mensagem = Mensagem.from_dict(dados)

    if not mensagem.nome or not mensagem.email or not mensagem.texto:
        return jsonify({
            "mensagem": "Preencha nome, e-mail e mensagem."
        }), 400

    if (
        not mensagem.cep.cep
        or len(mensagem.cep.cep) != 8
        or not mensagem.cep.cep.isdigit()
    ):
        return jsonify({
            "mensagem": "Informe um CEP válido com 8 números."
        }), 400

    if not mensagem.cep.cidade or len(mensagem.cep.uf) != 2:
        return jsonify({
            "mensagem": "Busque o CEP para preencher cidade e UF."
        }), 400

    if len(mensagem.nome) > 100 or len(mensagem.email) > 150:
        return jsonify({
            "mensagem": "Nome ou e-mail excede o tamanho permitido."
        }), 400

    if "@" not in mensagem.email or "." not in mensagem.email.rsplit("@", 1)[-1]:
        return jsonify({
            "mensagem": "Informe um e-mail válido."
        }), 400

    id_mensagem = mensagem_dao.cadastrar(mensagem)

    return jsonify({
        "mensagem": "Mensagem enviada com sucesso!",
        "id": id_mensagem
    }), 201


@app.errorhandler(Error)
def erro_banco(error):
    # Evita expor detalhes da conexão ou da consulta na resposta pública da API.
    return jsonify({
        "mensagem": "Não foi possível acessar o banco de dados."
    }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true"
    )