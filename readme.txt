Como executar o projeto no GitHub Codespaces
1. Criar o Codespace
1. Acesse o repositório no GitHub.
2. Clique em Code.
3. Acesse a aba Codespaces.
4. Clique em Create codespace on main.
5. Aguarde o VS Code abrir no navegador.
2. Configurar o MySQL
Abra o terminal do Codespaces e execute:
sudo apt-get update
sudo apt-get install -y mysql-server
Inicie o MySQL:
sudo service mysql start
Crie um usuário para o projeto:
sudo mysql
No console do MySQL, execute:
CREATE USER IF NOT EXISTS 'portfolio_user'@'127.0.0.1'
IDENTIFIED BY 'SENHA_DO_BANCO';

GRANT ALL PRIVILEGES ON portfolio.*
TO 'portfolio_user'@'127.0.0.1';

FLUSH PRIVILEGES;
EXIT;
Substitua SENHA_DO_BANCO por uma senha criada para o projeto.
3. Importar o banco de dados
Na raiz do projeto, execute o comando abaixo:
mysql -h 127.0.0.1 -u portfolio_user -p < database/sql/banco.sql
Informe a senha criada no passo anterior.

O banco utilizado pelo projeto é portfolio.

Para conferir se as tabelas foram criadas:
mysql -h 127.0.0.1 -u portfolio_user -p -e "USE portfolio; SHOW TABLES;"
4. Instalar as dependências
Na raiz do projeto, execute:
python -m pip install -r requirements.txt
5. Configurar as variáveis de ambiente
Antes de iniciar o Flask, configure as informações necessárias para a conexão com o banco e a segurança da aplicação.

No terminal, execute:
export PORTFOLIO_DB_HOST="127.0.0.1"
export PORTFOLIO_DB_USER="portfolio_user"
export PORTFOLIO_DB_PASSWORD="SENHA_DO_BANCO"
export PORTFOLIO_DB_NAME="portfolio"
export PORTFOLIO_DB_PORT="3306"

export ADMIN_PASSWORD="SENHA_DO_ADMINISTRADOR"
export FLASK_SECRET_KEY="CHAVE_SECRETA"
export FRONTEND_ORIGIN="https://NOME-DO-CODESPACE-5500.app.github.dev"
export COOKIE_SECURE="true"
export COOKIE_SAMESITE="None"
export FLASK_DEBUG="false"
Substitua os valores:
- PORTFOLIO_DB_PASSWORD: senha do usuário MySQL criado no passo 2.
- ADMIN_PASSWORD: senha que será utilizada para acessar a área administrativa.
- FLASK_SECRET_KEY: chave secreta utilizada para proteger as sessões.
- FRONTEND_ORIGIN: endereço HTTPS do front-end, que será disponibilizado na porta 5500.
Para gerar uma chave secreta, execute:
python -c "import secrets; print(secrets.token_hex(32))"
Copie o resultado e utilize como valor de FLASK_SECRET_KEY.

Não compartilhe nem publique suas senhas e chaves secretas.
6. Executar o back-end
Entre na pasta backend:
cd backend
Inicie o servidor Flask:
python app.py
O servidor será iniciado na porta 5000.

Mantenha esse terminal aberto enquanto estiver utilizando o projeto.
7. Acessar a API
1. Abra a aba Ports no painel inferior do Codespaces.
2. Localize a porta 5000.
3. Caso não apareça, adicione a porta manualmente.
4. Mantenha a visibilidade como Private durante os testes.
5. Clique no endereço disponibilizado para acessar a API.
A rota inicial (/) deve apresentar a mensagem:
{
  "mensagem": "API do Portfólio funcionando!"
}
Copie o endereço HTTPS disponibilizado para a porta 5000. Ele será utilizado na configuração do JavaScript.
8. Configurar o endereço da API no JavaScript
O front-end precisa utilizar o endereço encaminhado pelo Codespaces para se comunicar com o Flask.
1. Abra o arquivo js/script.js.
2. Localize a constante API no início do arquivo.
3. Configure-a com o endereço HTTPS real da porta 5000:
const API = "https://NOME-DO-CODESPACE-5000.app.github.dev";
Substitua o endereço de exemplo pelo endereço real disponibilizado pelo Codespaces.

Não coloque uma barra / no final do endereço.

Salve o arquivo.
9. Configurar o endereço do front-end
O Flask precisa reconhecer o endereço do front-end para permitir a comunicação entre as duas partes do sistema.
1. Abra a aba Ports.
2. Adicione a porta 5500.
3. Copie o endereço HTTPS disponibilizado para essa porta.
4. Configure a variável FRONTEND_ORIGIN com esse endereço, conforme o passo 5.
5. Se você alterou a variável depois de iniciar o Flask, pare o servidor utilizando Ctrl + C e inicie-o novamente.
10. Executar o front-end
Abra um segundo terminal no Codespaces.

Certifique-se de estar na raiz do projeto e execute:
python -m http.server 5500
Acesse a aba Ports e clique no endereço HTTPS da porta 5500.

O site deverá abrir normalmente.
11. Testar a integração
Depois de iniciar o front-end e o back-end, faça os seguintes testes:
1. Página inicial: confira se o site abre corretamente.
2. Projetos: verifique se os projetos são carregados pela API.
3. Contato: informe um CEP válido e confira se os dados do endereço são preenchidos automaticamente.
4. Envio de mensagem: preencha o formulário e envie uma mensagem de teste.
5. Administração: acesse a página administrativa e entre com a senha definida em ADMIN_PASSWORD.
6. Gerenciamento de projetos: teste o cadastro, a edição e a exclusão de projetos.
7. Mensagens: confira se as mensagens enviadas aparecem na área administrativa.
Para conferir os registros diretamente no banco:
mysql -h 127.0.0.1 -u portfolio_user -p -e "USE portfolio; SELECT * FROM projeto; SELECT * FROM mensagem; SELECT * FROM cep;"
Caso apareça algum erro de conexão ou CORS, confira:
- Se o MySQL está iniciado.
- Se o Flask está funcionando na porta 5000.
- Se o front-end está funcionando na porta 5500.
- Se o endereço da API no JavaScript está correto.
- Se FRONTEND_ORIGIN corresponde exatamente ao endereço do front-end.
Observações:
- No mesmo Codespace, não é necessário reinstalar as dependências ou importar novamente o banco a cada execução, desde que o ambiente e os dados sejam preservados.
- Sempre inicie o MySQL antes de executar o Flask.
- As variáveis de ambiente configuradas com export ficam disponíveis naquele terminal e em processos iniciados por ele. Se abrir um novo terminal para o back-end, configure-as novamente nele.
- Não publique senhas ou chaves secretas no GitHub.
- Para executar novamente o projeto, basta iniciar o MySQL, configurar as variáveis de ambiente, iniciar o Flask e iniciar o servidor do front-end.
Rotas da API (Flask)
O backend utiliza Flask para disponibilizar rotas que permitem a comunicação entre o sistema e o banco de dados MySQL.

A API pode ser acessada pela porta 5000 do Codespaces.
Projetos
Método	Rota	Descrição
GET	/projetos	Lista todos os projetos cadastrados.
POST	/projetos	Cadastra um novo projeto.
PUT	/projetos/<id>	Atualiza os dados de um projeto.
DELETE	/projetos/<id>	Exclui um projeto.


Mensagens
Método	Rota	Descrição
GET	/mensagens	Lista as mensagens cadastradas.
POST	/mensagens	Cadastra uma nova mensagem.


Rota inicial
Método	Rota	Descrição
GET	/	Verifica se a API está funcionando.


Como testar
As rotas GET podem ser testadas diretamente pelo navegador, utilizando a URL encaminhada pelo Codespaces.

As rotas POST, PUT e DELETE devem ser testadas por uma ferramenta de requisições HTTP, como Thunder Client ou Postman, enviando os dados necessários no formato JSON.

Observação: substitua <id> pelo identificador do projeto que deseja consultar, editar ou excluir.