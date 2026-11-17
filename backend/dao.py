import os
import mysql.connector

from models import Cep, Mensagem, Projeto


# Configura os dados de conexão usando variáveis de ambiente.
DB_CONFIG = {
    "host": os.getenv("PORTFOLIO_DB_HOST", "127.0.0.1"),
    "user": os.getenv("PORTFOLIO_DB_USER", "root"),
    "password": os.getenv("PORTFOLIO_DB_PASSWORD", "root"),
    "database": os.getenv("PORTFOLIO_DB_NAME", "portfolio"),
    "port": int(os.getenv("PORTFOLIO_DB_PORT", "3306"))
}


class CepDAO:
    # Abre uma conexão com o banco de dados.
    def conectar(self):
        return mysql.connector.connect(**DB_CONFIG)

    # Busca um endereço pelo CEP informado.
    def buscar(self, numero_cep):
        conexao = self.conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                "SELECT cep, rua, bairro, cidade, uf FROM cep WHERE cep = %s",
                (numero_cep,)
            )

            linha = cursor.fetchone()

            if linha:
                return Cep(*linha)

            return None
        finally:
            cursor.close()
            conexao.close()

    def cadastrar(self, cep):
        conexao = self.conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO cep (cep, rua, bairro, cidade, uf)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (cep.cep, cep.rua, cep.bairro, cep.cidade, cep.uf)
            )

            conexao.commit()
        finally:
            cursor.close()
            conexao.close()


class MensagemDAO:
    def conectar(self):
        return mysql.connector.connect(**DB_CONFIG)

    # Salva o endereço e a mensagem na mesma transação.
    def cadastrar(self, mensagem):
        conexao = self.conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                "SELECT cep FROM cep WHERE cep = %s",
                (mensagem.cep.cep,)
            )

            cep_existente = cursor.fetchone()

            if cep_existente is None:
                cursor.execute(
                    """
                    INSERT INTO cep (cep, rua, bairro, cidade, uf)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        mensagem.cep.cep,
                        mensagem.cep.rua,
                        mensagem.cep.bairro,
                        mensagem.cep.cidade,
                        mensagem.cep.uf
                    )
                )

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

        except Exception:
            conexao.rollback()
            raise

        finally:
            cursor.close()
            conexao.close()

    def listar(self):
        conexao = self.conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                """
                SELECT m.id, m.nome, m.email, m.texto, m.data_envio,
                       c.cep, c.rua, c.bairro, c.cidade, c.uf
                FROM mensagem m
                INNER JOIN cep c ON m.cep = c.cep
                ORDER BY m.data_envio DESC
                """
            )

            linhas = cursor.fetchall()
            mensagens = []

            for linha in linhas:
                endereco = Cep(*linha[5:10])
                mensagem = Mensagem(*linha[0:5], endereco)
                mensagens.append(mensagem)

            return mensagens

        finally:
            cursor.close()
            conexao.close()


# Operações de consulta e manutenção dos projetos.
class ProjetoDAO:
    def conectar(self):
        return mysql.connector.connect(**DB_CONFIG)

    def listar(self):
        conexao = self.conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                """
                SELECT id_projeto, titulo, descricao, imagem, categoria, link
                FROM projeto
                ORDER BY id_projeto DESC
                """
            )

            linhas = cursor.fetchall()
            projetos = []

            for linha in linhas:
                projeto = Projeto(
                    linha[1],
                    linha[2],
                    linha[3],
                    linha[4],
                    linha[5],
                    linha[0]
                )

                projetos.append(projeto)

            return projetos

        finally:
            cursor.close()
            conexao.close()

    def cadastrar(self, projeto):
        conexao = self.conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO projeto (titulo, descricao, imagem, categoria, link)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    projeto.titulo,
                    projeto.descricao,
                    projeto.imagem,
                    projeto.categoria,
                    projeto.link
                )
            )

            conexao.commit()
            return cursor.lastrowid

        finally:
            cursor.close()
            conexao.close()

    def atualizar(self, id_projeto, projeto):
        conexao = self.conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                """
                UPDATE projeto
                SET titulo = %s, descricao = %s, imagem = %s,
                    categoria = %s, link = %s
                WHERE id_projeto = %s
                """,
                (
                    projeto.titulo,
                    projeto.descricao,
                    projeto.imagem,
                    projeto.categoria,
                    projeto.link,
                    id_projeto
                )
            )

            conexao.commit()
            return cursor.rowcount > 0

        finally:
            cursor.close()
            conexao.close()

    def excluir(self, id_projeto):
        conexao = self.conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                "DELETE FROM projeto WHERE id_projeto = %s",
                (id_projeto,)
            )

            conexao.commit()
            return cursor.rowcount > 0

        finally:
            cursor.close()
            conexao.close()