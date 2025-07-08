import sys
import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# Verifica se o argumento foi fornecido
if len(sys.argv) < 2:
    print("Uso: python main.py caminho/do/arquivo.csv")
    sys.exit(1)

# Obtém o caminho do arquivo CSV
csv_file = sys.argv[1]

# Nome da tabela será o nome do arquivo sem extensão
table_name = os.path.splitext(os.path.basename(csv_file))[0]

# Lê o arquivo CSV
try:
    data = pd.read_csv(csv_file)
except Exception as e:
    print(f"Erro ao ler o arquivo CSV: {e}")
    sys.exit(1)

# Conecta ao banco de dados MySQL
db_host = os.getenv("MYSQL_CSV_LOAD_HOST")
db_user = os.getenv("MYSQL_CSV_LOAD_USER")
db_password = os.getenv("MYSQL_CSV_LOAD_PASSWORD")
db_name = os.getenv("MYSQL_CSV_LOAD_DATABASE")

if not db_host or not db_user or not db_name:
    print("Erro: As variáveis de ambiente MYSQL_CSV_LOAD_HOST, MYSQL_CSV_LOAD_USER e MYSQL_CSV_LOAD_DATABASE devem ser configuradas.")
    sys.exit(1)

try:
    conn = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = conn.cursor()
except mysql.connector.Error as err:
    print(f"Erro ao conectar ao MySQL: {err}")
    sys.exit(1)

# Cria a tabela dinamicamente
columns = ", ".join([f"`{col}` TEXT" for col in data.columns])
create_table_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({columns});"

try:
    cursor.execute(create_table_query)
    conn.commit()
except Exception as e:
    print(f"Erro ao criar a tabela: {e}")
    conn.close()
    sys.exit(1)

# Insere os dados
for _, row in data.iterrows():
    placeholders = ", ".join(["%s"] * len(row))
    insert_query = f"INSERT INTO `{table_name}` VALUES ({placeholders})"
    cursor.execute(insert_query, tuple(row))

conn.commit()
conn.close()

print(f"Dados importados com sucesso para a tabela '{table_name}'")