class Cep:
    def __init__(self, cep, rua, bairro, cidade, uf):
        self.cep = cep
        self.rua = rua
        self.bairro = bairro
        self.cidade = cidade
        self.uf = uf

    def exibir_endereco(self):
        return f"CEP: {self.cep}, Rua: {self.rua}, Bairro: {self.bairro}, Cidade: {self.cidade}, UF: {self.uf}"

    def to_dict(self):
        return {
            "cep": self.cep,
            "rua": self.rua,
            "bairro": self.bairro,
            "cidade": self.cidade,
            "uf": self.uf,
        }

    @staticmethod
    def from_dict(dados):
        return Cep(
            dados["cep"],
            dados["rua"],
            dados["bairro"],
            dados["cidade"],
            dados["uf"],
        )


class Mensagem:
    def __init__(self, id, nome, email, texto, data_envio, cep):
        self.id = id
        self.nome = nome
        self.email = email
        self.texto = texto
        self.data_envio = data_envio
        self.cep = cep

    def exibir_mensagem(self):
        return f"""
            Nome: {self.nome}
            E-mail: {self.email}
            Mensagem: {self.texto}
            Data: {self.data_envio}
            Endereço: {self.cep.exibir_endereco()}
        """

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "texto": self.texto,
            "data_envio": str(self.data_envio) if self.data_envio else None,
            "cep": self.cep.to_dict(),
        }

    @staticmethod
    def from_dict(dados):
        # id e data_envio são gerados pelo banco.
        return Mensagem(
            None,
            dados["nome"],
            dados["email"],
            dados["texto"],
            None,
            Cep.from_dict(dados["cep"]),
        )


class Projeto:
    def __init__(self, titulo, descricao, imagem=None, categoria=None, link=None, id_projeto=None):
        self.id_projeto = id_projeto
        self.titulo = titulo
        self.descricao = descricao
        self.imagem = imagem
        self.categoria = categoria
        self.link = link

    def to_dict(self):
        return {
            "id_projeto": self.id_projeto,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "imagem": self.imagem,
            "categoria": self.categoria,
            "link": self.link,
        }

    @staticmethod
    def from_dict(dados):
        return Projeto(
            dados["titulo"],
            dados["descricao"],
            dados.get("imagem"),
            dados.get("categoria"),
            dados.get("link"),
        )