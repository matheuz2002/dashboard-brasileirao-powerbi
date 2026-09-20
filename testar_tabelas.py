import sqlite3
import pandas as pd

# Conecta ao banco de dados SQLite
conn = sqlite3.connect("futebol.db")

# Lista todas as tabelas criadas no banco
tabelas = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
print("--- TABELAS NO BANCO DE DADOS ---")
print(tabelas)

# Se a tabela de partidas existir, mostra as primeiras linhas
if "partidas_brasileirao" in tabelas["name"].values:
    print("\n--- AMOSTRA DA TABELA DE PARTIDAS ---")
    df_partidas = pd.read_sql("SELECT * FROM partidas_brasileirao LIMIT 5", conn)
    print(df_partidas[["rodada", "mandante", "visitante", "gols_mandante", "gols_visitante", "status"]])

conn.close()