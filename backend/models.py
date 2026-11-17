# Classe que representa um endereço de CEP.
# Guarda os dados do local relacionado à mensagem de contato.
class Cep:
    def __init__(self, cep, rua, bairro, cidade, uf):
        self.cep = cep
        self.rua = rua
        self.bairro = bairro
        self.cidade = cidade
        self.uf = uf

    def exibir_endereco(self):
        # Devolve o endereço em uma linha de texto legível.
        return (
            f"{self.rua}, {self.bairro} - "
            f"{self.cidade}/{self.uf} (CEP {self.cep})"
        )

    def to_dict(self):
        # Converte o objeto em um dicionário para devolver em JSON.
        return {
            "cep": self.cep,
            "rua": self.rua,
            "bairro": self.bairro,
            "cidade": self.cidade,
            "uf": self.uf
        }

    @staticmethod
    def from_dict(dados):
        # Aceita tanto os nomes usados no banco quanto os nomes do ViaCEP.
        if not isinstance(dados, dict):
            dados = {}

        # A API externa pode formatar o CEP com hífen e usar "logradouro" e
        # "localidade"; aqui os formatos diferentes são normalizados no modelo.
        cep = str(dados.get("cep", "")).replace("-", "").strip()
        rua = str(dados.get("rua", dados.get("logradouro", "")) or "").strip()
        cidade = str(dados.get("cidade", dados.get("localidade", "")) or "").strip()

        return Cep(
            cep,
            rua,
            str(dados.get("bairro", "") or "").strip(),
            cidade,
            str(dados.get("uf", "") or "").strip().upper()
        )


# Classe que representa uma mensagem enviada pelo formulário de contato.
class Mensagem:
    def __init__(self, id, nome, email, texto, data_envio, cep):
        self.id = id
        self.nome = nome
        self.email = email
        self.texto = texto
        self.data_envio = data_envio
        self.cep = cep

    def exibir_mensagem(self):
        # Devolve a mensagem em uma linha de texto legível.
        return f"{self.nome} ({self.email}): {self.texto}"

    def to_dict(self):
        # Converte a mensagem em JSON para devolver pela API.
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "texto": self.texto,
            "data_envio": str(self.data_envio) if self.data_envio else None,
            "cep": self.cep.to_dict()
        }

    @staticmethod
    def from_dict(dados):
        if not isinstance(dados, dict):
            dados = {}

        dados_cep = dados.get("cep")

        # Se o CEP vier junto com as demais informações, usa esse bloco.
        # Caso contrário, considera que os dados do endereço estão no mesmo objeto.
        # Isso permite receber tanto o formato aninhado do formulário quanto um
        # objeto plano sem espalhar essa decisão pela rota da API.
        if not isinstance(dados_cep, dict):
            dados_cep = dados

        return Mensagem(
            None,
            str(dados.get("nome", "") or "").strip(),
            str(dados.get("email", "") or "").strip(),
            str(dados.get("texto", "") or "").strip(),
            None,
            Cep.from_dict(dados_cep)
        )


# Classe que representa um projeto do portfólio.
class Projeto:
    def __init__(self, titulo, descricao, imagem=None, categoria=None, link=None, id_projeto=None):
        self.id_projeto = id_projeto
        self.titulo = titulo
        self.descricao = descricao
        self.imagem = imagem
        self.categoria = categoria
        self.link = link

    def to_dict(self):
        # Transformando o projeto em dicionário para renderizar no frontend.
        return {
            "id_projeto": self.id_projeto,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "imagem": self.imagem,
            "categoria": self.categoria,
            "link": self.link
        }

    @staticmethod
    def from_dict(dados):
        # Cria um objeto Projeto a partir do JSON enviado pela aplicação.
        if not isinstance(dados, dict):
            dados = {}

        return Projeto(
            str(dados.get("titulo", "") or "").strip(),
            str(dados.get("descricao", "") or "").strip(),
            str(dados.get("imagem", "") or "").strip() or None,
            str(dados.get("categoria", "") or "").strip() or None,
            str(dados.get("link", "") or "").strip() or None
        )
