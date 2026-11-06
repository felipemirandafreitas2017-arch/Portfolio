-- Cria o banco de dados do portfólio, se ainda não existir.
CREATE DATABASE IF NOT EXISTS portfolio;

-- Seleciona o banco que será usado.
USE portfolio;

-- Cria a tabela de CEPs e seus endereços.
CREATE TABLE IF NOT EXISTS cep (
  cep     CHAR(9) PRIMARY KEY, -- CEP único do endereço.
  rua     VARCHAR(100), -- Nome da rua.
  bairro  VARCHAR(100), -- Nome do bairro.
  cidade  VARCHAR(100) NOT NULL, -- Cidade do endereço.
  uf      CHAR(2) NOT NULL -- Sigla do estado.
);

-- Cria a tabela que armazena as mensagens recebidas.
CREATE TABLE IF NOT EXISTS mensagem (
  id          INT PRIMARY KEY AUTO_INCREMENT, -- Identificador único da mensagem.
  nome        VARCHAR(100) NOT NULL, -- Nome de quem enviou a mensagem.
  email       VARCHAR(100) NOT NULL, -- E-mail para contato.
  texto       TEXT NOT NULL, -- Conteúdo da mensagem.
  data_envio  DATETIME DEFAULT NOW(), -- Data e hora do envio.
  cep         CHAR(9) NOT NULL, -- CEP relacionado à mensagem.
  FOREIGN KEY (cep) REFERENCES cep(cep) -- Liga a mensagem ao endereço cadastrado.
);