import sqlite3
import pandas as pd

# Conecta ao banco SQLite
conn = sqlite3.connect("futebol.db")

# Lê as tabelas do banco para DataFrames do Pandas
df_tabela = pd.read_sql("SELECT * FROM tabela_brasileirao", conn)
df_partidas = pd.read_sql("SELECT * FROM partidas_brasileirao", conn)

# Exporta para arquivos CSV dentro da pasta do projeto
df_tabela.to_csv("tabela_brasileirao.csv", index=False, encoding="utf-8-sig")
df_partidas.to_csv("partidas_brasileirao.csv", index=False, encoding="utf-8-sig")

conn.close()
print("Exportação para CSV concluída com sucesso! Os arquivos estão na pasta do projeto.")