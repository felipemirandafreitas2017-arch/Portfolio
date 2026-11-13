# Como executar o projeto no GitHub Codespaces

## 1. Criar o Codespace

1. Acesse o repositório no GitHub.
2. Clique em **Code**.
3. Acesse a aba **Codespaces**.
4. Clique em **Create codespace on main**.
5. Aguarde o VS Code abrir no navegador.

## 2. Configurar o MySQL

Abra o terminal do Codespaces e execute:

```bash
sudo apt-get update
sudo apt-get install -y mysql-server
```

Inicie o MySQL:

```bash
sudo service mysql start
```

Configure a senha do usuário root:

```bash
sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';"
```

## 3. Importar o banco de dados

Na raiz do projeto, execute o comando abaixo, substituindo `banco.sql` pelo nome do arquivo SQL disponível em `database/sql`:

```bash
mysql -h 127.0.0.1 -uroot -proot < database/sql/banco.sql
```

O banco utilizado pelo projeto é `portfolio`.

## 4. Instalar as dependências

Na raiz do projeto, execute:

```bash
pip install -r requirements.txt
```

## 5. Executar o back-end

Entre na pasta `backend`:

```bash
cd backend
```

Inicie o servidor Flask:

```bash
python app.py
```

O servidor será iniciado na porta **5000**.

## 6. Acessar a API

1. Abra a aba **Ports** no painel inferior do Codespaces.
2. Localize a porta `5000`.
3. Clique no endereço disponibilizado para acessar a API.

A rota inicial (`/`) deve apresentar a mensagem:

```json
{
  "mensagem": "API do Portfólio funcionando!"
}
```

---

**Observações:**
- No mesmo Codespace, não é necessário reinstalar as dependências ou importar novamente o banco a cada execução, desde que o ambiente e os dados sejam preservados.
- Sempre inicie o MySQL antes de executar o Flask.
- Para executar novamente o projeto, basta iniciar o MySQL e rodar `python app.py` dentro da pasta `backend`.