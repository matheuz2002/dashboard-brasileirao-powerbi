import sqlite3 
import pandas as pd

conn = sqlite3.connect("futebol.db")

df = pd.read_sql_query("SELECT posicao, time, pontos, jogos, vitorias, saldo_gols FROM tabela_brasileirao", conn)

conn.close()

print("--- CLASSIFICAÇÃO DO BRASILEIRÃO (VIA SQL) ---")
print(df.to_string(index=False))