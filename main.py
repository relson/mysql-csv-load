import sys
import pandas as pd
import mysql.connector
import os

# Verifica se o argumento foi fornecido
if len(sys.argv) < 2:
    print("Uso: python script.py caminho/do/arquivo.csv")
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
conn = mysql.connector.connect(
    host="localhost",  # Altere conforme necessário
    user="root",  # Altere conforme necessário
    password="root",  # Altere conforme necessário
    database="m"   # Altere conforme necessário
)
cursor = conn.cursor()

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
