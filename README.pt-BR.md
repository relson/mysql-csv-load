# mysql-csv-load

Este é um script Python simples para carregar dados de um arquivo CSV para uma tabela em um banco de dados MySQL.

## Funcionalidades

- Lê um arquivo CSV especificado como argumento na linha de comando.
- Cria uma tabela no banco de dados MySQL com o mesmo nome do arquivo CSV (sem a extensão).
- As colunas da tabela são criadas dinamicamente com base no cabeçalho do arquivo CSV.
- Insere os dados do arquivo CSV na tabela recém-criada.

## Como utilizar

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/mysql-csv-load.git
   cd mysql-csv-load
   ```

2. **(Opcional) Crie e ative um ambiente virtual:**

   É recomendado usar um ambiente virtual para gerenciar as dependências:

   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as credenciais do banco de dados:**

   Crie um arquivo `.env` na raiz do projeto com suas credenciais MySQL. Você pode usar o arquivo `.env.example` como modelo.

   ```
   MYSQL_CSV_LOAD_HOST=localhost
   MYSQL_CSV_LOAD_USER=root
   MYSQL_CSV_LOAD_PASSWORD=root
   MYSQL_CSV_LOAD_DATABASE=m
   ```

4. **Execute o script:**

   Execute o script a partir da linha de comando, passando o caminho para o seu arquivo CSV como argumento:

   ```bash
   python main.py caminho/para/seu/arquivo.csv
   ```

   Por exemplo:

   ```bash
   python main.py exemplos/dados_de_clientes.csv
   ```

   O script irá criar uma tabela chamada `dados_de_clientes` (se ainda não existir) e inserir os dados do arquivo CSV nela.

## Exemplo

Suponha que você tenha um arquivo `produtos.csv` com o seguinte conteúdo:

```csv
ID,Nome,Preco
1,Produto A,19.99
2,Produto B,29.99
3,Produto C,39.99
```

Ao executar o comando:

```bash
python main.py produtos.csv
```

O script irá:

1. Conectar-se ao seu banco de dados MySQL.
2. Criar uma tabela chamada `produtos` com as colunas `ID`, `Nome` e `Preco`.
3. Inserir as 3 linhas de dados do arquivo CSV na tabela `produtos`.

## Requisitos

- Python 3.x
- pandas
- mysql-connector-python

Você pode instalar as dependências necessárias executando:

```bash
pip install -r requirements.txt
```

## TODO

- Usar um arquivo .env para carregar as credenciais
- Criar um pacote pip