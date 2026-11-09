class Cep:
    def __init__(self, cep, rua, bairro, cidade, uf):
        self.cep = cep
        self.rua = rua
        self.bairro = bairro
        self.cidade = cidade
        self.uf = uf

    def exibir_endereco(self):
        return f"CEP: {self.cep}, Rua: {self.rua}, Bairro: {self.bairro}, Cidade: {self.cidade}, UF: {self.uf}"

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
            Endereço: {self.cep.exibir_endereco()}"""