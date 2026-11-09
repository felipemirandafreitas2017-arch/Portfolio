
# Driver que permite ao Python abrir conexões com o MySQL.
# Se faltar no interpretador selecionado, instale com:
# python -m pip install mysql-connector-python
import mysql.connector

# Classes usadas para transformar os dados do banco em objetos.
from models import Cep, Mensagem


class CepDAO:
    def __init__(self, config):
        # Guarda os dados de conexão, como host, usuário, senha e banco.
        self.config = config

    def conectar(self):
        # Abre uma conexão com o MySQL usando a configuração recebida.
        return mysql.connector.connect(**self.config)

    def buscar(self, numero_cep):
        # Busca um endereço pelo CEP e devolve um objeto Cep, se encontrado.
        conexao = self.conectar()
        cursor = conexao.cursor()

        try:
            # O %s é preenchido pelo driver com o valor de numero_cep.
            cursor.execute(
                "SELECT cep, rua, bairro, cidade, uf FROM cep WHERE cep = %s",
                (numero_cep,)
            )

            linha = cursor.fetchone()

            if linha:
                return Cep(*linha)

            return None

        finally:
            # Fecha o cursor e a conexão mesmo se ocorrer algum erro.
            cursor.close()
            conexao.close()

    def cadastrar(self, cep):
        # Insere no banco os dados do endereço recebido.
        conexao = self.conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO cep (cep, rua, bairro, cidade, uf)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    cep.cep,
                    cep.rua,
                    cep.bairro,
                    cep.cidade,
                    cep.uf
                )
            )

            conexao.commit()

        finally:
            # Libera os recursos usados pelo banco.
            cursor.close()
            conexao.close()


class MensagemDAO:
    def __init__(self):
        # Configuração usada para conectar ao banco portfolio.
        self.config = {
            "host": "localhost",
            "user": "root",
            "password": "SUA_SENHA",
            "database": "portfolio"
        }

        # Reutiliza a mesma configuração para buscar e cadastrar CEPs.
        self.cep_dao = CepDAO(self.config)

    def conectar(self):
        # Abre uma conexão para executar operações na tabela mensagem.
        return mysql.connector.connect(**self.config)

    def cadastrar(self, mensagem):
        # Garante que o CEP exista antes de cadastrar a mensagem relacionada.
        cep_existente = self.cep_dao.buscar(mensagem.cep.cep)

        if cep_existente is None:
            self.cep_dao.cadastrar(mensagem.cep)

        # Insere a mensagem e retorna o identificador gerado pelo MySQL.
        conexao = self.conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO mensagem (nome, email, texto, cep)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    mensagem.nome,
                    mensagem.email,
                    mensagem.texto,
                    mensagem.cep.cep
                )
            )

            conexao.commit()

            return cursor.lastrowid

        finally:
            # Fecha os recursos mesmo se o cadastro falhar.
            cursor.close()
            conexao.close()

    def listar(self):
        # Busca mensagens junto com os dados do CEP de cada uma.
        conexao = self.conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    m.id,
                    m.nome,
                    m.email,
                    m.texto,
                    m.data_envio,
                    c.cep,
                    c.rua,
                    c.bairro,
                    c.cidade,
                    c.uf
                FROM mensagem m
                INNER JOIN cep c ON m.cep = c.cep
                ORDER BY m.data_envio DESC
                """
            )

            linhas = cursor.fetchall()
            mensagens = []

            # Converte cada linha retornada em objetos Cep e Mensagem.
            for linha in linhas:
                endereco = Cep(*linha[5:10])

                mensagem = Mensagem(
                    *linha[0:5],
                    endereco
                )

                mensagens.append(mensagem)

            return mensagens

        finally:
            # Fecha os recursos usados para consultar o banco.
            cursor.close()
            conexao.close()
