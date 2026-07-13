# mysql-csv-load

Uma ferramenta de linha de comando (CLI) em Python para carregar dados de um arquivo CSV para uma tabela do MySQL utilizando **convenção sobre configuração**.

## Funcionalidades

- Processamento eficiente de arquivos CSV utilizando Pandas.
- **Convenção sobre Configuração**: O nome da tabela no banco de dados é inferido automaticamente a partir do nome do arquivo CSV (ex: `usuarios.csv` será carregado na tabela `usuarios`).
- Suporte a variáveis de ambiente para proteger credenciais de acesso.
- Execução via comando global no terminal após a instalação.

---

## Instalação

### A partir do código-fonte local
Clone o repositório e instale utilizando o `pip`:

```bash
git clone https://github.com/relson/mysql-csv-load.git
cd mysql-csv-load
pip install .

```

---

## Configuração

A aplicação utiliza o `python-dotenv` para gerenciar as credenciais do banco de dados. Crie um arquivo `.env` no seu diretório de trabalho com as seguintes variáveis:

```env
MYSQL_CSV_LOAD_HOST=localhost
MYSQL_CSV_LOAD_USER=seu_usuario
MYSQL_CSV_LOAD_PASSWORD=sua_senha
MYSQL_CSV_LOAD_DATABASE=nome_do_seu_banco
MYSQL_CSV_LOAD_PORT=porta_do_seu_banco      # se em branco ou não configurado usa 3306
```

---

## Como Usar

Após a instalação, o pacote registra um comando global `mysql-csv-load`. Basta passar o caminho do arquivo CSV como argumento:

```bash
mysql-csv-load caminho/do/seu/clientes.csv

```

> **Como funciona:** O comando acima vai processar o arquivo `clientes.csv` e tentar inserir os dados diretamente na tabela `clientes` no seu MySQL.

---