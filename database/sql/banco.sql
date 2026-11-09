-- Cria o banco de dados do portfólio, se ainda não existir.
CREATE DATABASE IF NOT EXISTS portfolio;

-- Seleciona o banco que será usado.
USE portfolio;

-- Cria a tabela de CEPs e seus endereços.
CREATE TABLE IF NOT EXISTS cep (
  cep     CHAR(8) PRIMARY KEY, -- CEP único do endereço.
  rua     VARCHAR(100), -- Nome da rua.
  bairro  VARCHAR(100), -- Nome do bairro.
  cidade  VARCHAR(100) NOT NULL, -- Cidade do endereço.
  uf      CHAR(2) NOT NULL -- Sigla do estado.
);

-- Cria a tabela que armazena as mensagens recebidas.
CREATE TABLE IF NOT EXISTS mensagem (
  id          INT PRIMARY KEY AUTO_INCREMENT, -- Identificador único da mensagem.
  nome        VARCHAR(100) NOT NULL, -- Nome de quem enviou a mensagem.
  email       VARCHAR(150) NOT NULL, -- E-mail para contato.
  texto       TEXT NOT NULL, -- Conteúdo da mensagem.
  data_envio  DATETIME DEFAULT CURRENT_TIMESTAMP, -- Data e hora do envio.
  cep         CHAR(8) NOT NULL, -- CEP relacionado à mensagem.
  FOREIGN KEY (cep) REFERENCES cep(cep) -- Liga a mensagem ao endereço cadastrado.
);

-- Cria a tabela que armazena os projetos exibidos na aba Serviços.
CREATE TABLE IF NOT EXISTS projeto (
  id_projeto  INT PRIMARY KEY AUTO_INCREMENT, -- Identificador único do projeto.
  titulo      VARCHAR(100) NOT NULL, -- Nome do projeto.
  descricao   TEXT NOT NULL, -- Descrição do projeto.
  imagem      VARCHAR(255), -- Caminho da imagem do projeto.
  categoria   VARCHAR(60), -- Categoria ou tipo do projeto.
  link        VARCHAR(255) -- Link para acessar o projeto.
);