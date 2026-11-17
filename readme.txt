# Como executar o projeto no GitHub Codespaces

Este documento apresenta os passos para preparar o ambiente, importar o banco de dados e executar o Portfólio Felipe Miranda no GitHub Codespaces.

## 1. Criar o Codespace

1. Acesse o repositório do projeto no GitHub.
2. Clique no botão **Code**.
3. Abra a aba **Codespaces**.
4. Clique em **Create codespace on main**.
5. Aguarde o carregamento do ambiente.

## 2. Configurar o MySQL

Abra o terminal do Codespace e execute:

```bash
sudo apt-get update
sudo apt-get install -y mysql-server
sudo service mysql start
sudo service mysql status
```

O último comando deve indicar que o serviço está ativo.

### Criar o usuário e o banco de dados

O MySQL precisa de um usuário com permissão para acessar o banco do projeto. Primeiro, tente abrir o console administrativo:

```bash
sudo mysql
```

**Importante:** os comandos SQL abaixo devem ser executados dentro do console do MySQL, quando o prompt aparecer como `mysql>`. Não os execute diretamente no terminal Bash.

Dentro do MySQL, execute:

```sql
CREATE USER IF NOT EXISTS 'portfolio_user'@'localhost' IDENTIFIED BY 'portfolio_senha';
CREATE USER IF NOT EXISTS 'portfolio_user'@'127.0.0.1' IDENTIFIED BY 'portfolio_senha';

GRANT ALL PRIVILEGES ON portfolio.* TO 'portfolio_user'@'localhost';
GRANT ALL PRIVILEGES ON portfolio.* TO 'portfolio_user'@'127.0.0.1';

FLUSH PRIVILEGES;
EXIT;
```

Neste exemplo, o usuário é `portfolio_user` e a senha é `portfolio_senha`. Se as credenciais forem alteradas, use os mesmos valores na importação do banco e nas configurações utilizadas pelo back-end.

**Se `sudo mysql` retornar `Access denied`:** não continue para a criação do usuário, pois ela ainda não foi executada. Não tente redefinir a senha do usuário `root` sem orientação. Verifique a configuração de autenticação do MySQL nesse ambiente antes de prosseguir.

## 3. Importar o banco de dados

Na raiz do projeto — a pasta que contém `database` — execute:

```bash
mysql -h 127.0.0.1 -u portfolio_user -p < database/sql/banco.sql
```

Quando aparecer `Enter password:`, digite a senha definida na etapa anterior (`portfolio_senha`) e pressione Enter. Os caracteres da senha não aparecem enquanto são digitados; isso é normal.

Se a importação terminar sem apresentar erros, o banco de dados foi carregado.

## 4. Instalar as dependências do Python

Na raiz do projeto, execute:

```bash
pip install -r requirements.txt
```

## 5. Configurar e executar o back-end

Antes de iniciar o Flask, confira se as variáveis de ambiente exigidas pelo projeto estão configuradas de acordo com os nomes utilizados em `backend/app.py` e `backend/dao.py`.

As credenciais do banco devem corresponder ao usuário, senha e banco definidos na etapa 2. Também configure as variáveis de ambiente de segurança e CORS utilizadas pelo projeto. Não publique senhas ou chaves secretas no repositório.

Entre na pasta do back-end:

```bash
cd backend
```

Inicie a aplicação:

```bash
python app.py
```

Mantenha esse terminal aberto enquanto estiver testando o sistema.

## 6. Acessar a API

1. No Codespaces, abra a aba **Ports**.
2. Localize a porta **5000**.
3. Se necessário, altere a visibilidade da porta para permitir o acesso pelo navegador.
4. Abra o endereço encaminhado pelo Codespaces.

A rota inicial da API (`/`) deve retornar uma resposta JSON indicando:

```json
{
  "mensagem": "API do Portfólio funcionando!"
}
```

Copie o endereço encaminhado para a porta 5000. Ele será utilizado pelo front-end para realizar as requisições à API.

## 7. Executar o front-end

O front-end é composto pelos arquivos HTML, CSS e JavaScript. Para visualizá-lo no Codespaces, abra **um segundo terminal**, mantendo o terminal do Flask em execução.

1. Volte para a pasta raiz do projeto, onde está o arquivo `index.html`:

```bash
cd ..
```

Se o terminal já estiver na raiz do projeto, não é necessário executar esse comando.

2. Inicie um servidor local para os arquivos do front-end:

```bash
python -m http.server 5500
```

3. No Codespaces, abra a aba **Ports**.
4. Localize a porta **5500** e abra o endereço encaminhado pelo Codespaces.
5. O navegador deverá exibir o `index.html` do portfólio.

### Conectar o front-end ao back-end

O JavaScript do projeto precisa utilizar o endereço atual da API, encaminhado pela porta **5000**.

1. Abra o arquivo `js/script.js`.
2. Localize a configuração da URL da API que ainda contém o texto de exemplo `https://SEU-CODESPACE-5000.app.github.dev`.
3. Substitua esse endereço pelo endereço real encaminhado pelo Codespaces para a porta **5000**, mantendo o restante do código.
4. Salve o arquivo e atualize a página do portfólio.

O endereço da porta **5500** é o front-end; o endereço da porta **5000** é o back-end. São endereços diferentes.

**Atenção ao CORS:** o back-end precisa permitir a origem usada pelo front-end. Se o projeto estiver configurado para utilizar a variável `FRONTEND_ORIGIN`, configure-a com o endereço completo encaminhado para a porta **5500**, antes de iniciar o Flask. Se alterar essa configuração, reinicie o back-end.

## Observações

- Execute os comandos a partir da pasta indicada em cada etapa.
- Comandos iniciados por `sudo`, `pip`, `mysql` ou `python` são comandos do terminal Bash.
- Comandos como `CREATE USER`, `GRANT` e `FLUSH PRIVILEGES` são comandos SQL e devem ser executados dentro do console do MySQL.
- Se o terminal solicitar uma senha, digite-a e pressione Enter. É normal que nada apareça na tela durante a digitação.
- Não compartilhe nem envie ao GitHub senhas do banco de dados, chaves secretas ou outras credenciais.
- O Codespaces precisa permanecer ativo para que o front-end e a API continuem disponíveis.
- Mantenha os dois terminais abertos: um executando o Flask (porta 5000) e outro servindo o front-end (porta 5500).
- Os endereços encaminhados pelo Codespaces podem mudar. Quando isso acontecer, confira a URL da API no `js/script.js` e a origem permitida pelo CORS.

## Rotas da API

As rotas abaixo representam as operações disponibilizadas pelo back-end do projeto:

| Método | Rota | Função |
|---|---|---|
| GET | `/` | Verificar se a API está funcionando |
| GET | `/projetos` | Listar projetos |
| POST | `/projetos` | Cadastrar projeto |
| PUT | `/projetos/<id>` | Editar projeto |
| DELETE | `/projetos/<id>` | Excluir projeto |
| GET | `/mensagens` | Consultar mensagens |
| POST | `/mensagens` | Enviar mensagem |

## Como testar

- **Navegador:** utilize para verificar a rota inicial (`/`) e a listagem de projetos (`/projetos`).
- **Thunder Client ou Postman:** utilize para testar as requisições `POST`, `PUT` e `DELETE`, enviando os dados no formato JSON quando necessário.
- **Pelo site:** com o back-end em execução e a URL da API configurada corretamente no JavaScript, teste o envio do formulário de contato e a visualização dos projetos.

Para operações de cadastro, edição, exclusão e consulta administrativa, utilize as regras de acesso implementadas no próprio back-end.
