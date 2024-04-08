import pandas as pd
from sqlalchemy import create_engine

# Caminho para o seu arquivo Excel
excel_file = "BTG1.xlsx"
# Nome da tabela para a qual você deseja importar os dados
table_name = "tb_Demanda_BTG1"

# String de conexão com o banco de dados corrigida para SQLite
database_connection_string = "sqlite:///C:/CONSULTAS_FIPE/fipe.db"
# Alternativamente, usando barras invertidas duplas
# database_connection_string = "sqlite:///C:\\\\CONSULTAS_FIPE\\\\fipe.db"

# Cria um motor de conexão com o banco de dados
engine = create_engine(database_connection_string)

# Lê a planilha Excel
df = pd.read_excel(excel_file)

# Insere os dados no banco de dados
df.to_sql(table_name, engine, if_exists="replace", index=False)

print(f"Dados importados com sucesso para a tabela {table_name}.")
