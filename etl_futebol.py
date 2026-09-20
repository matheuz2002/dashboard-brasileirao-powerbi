import os
import requests
import pandas as pd
import sqlite3
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()
API_KEY = os.getenv("FOOTBALL_API_KEY")

COMPETITION_CODE = "BSA"
HEADERS = {"X-Auth-Token": API_KEY}

def extrair_dados_api(endpoint):
    url = f"https://api.football-data.org/v4/competitions/{COMPETITION_CODE}/{endpoint}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao acessar {endpoint}: {response.status_code}")
        return None

def processar_tabela(data):
    if not data:
        return None
    
    standings = data["standings"][0]["table"]
    lista = []
    for item in standings:
        lista.append({
            "posicao": item["position"],
            "time": item["team"]["name"],
            "pontos": item["points"],
            "jogos": item["playedGames"],
            "vitorias": item["won"],
            "empates": item["draw"],
            "derrotas": item["lost"],
            "gols_pro": item["goalsFor"],
            "gols_contra": item["goalsAgainst"],
            "saldo_gols": item["goalDifference"]
        })
    return pd.DataFrame(lista)

def processar_partidas(data):
    if not data or "matches" not in data:
        print("Aviso: Nenhum dado de partidas encontrado.")
        return None
    
    matches = data["matches"]
    lista = []
    for match in matches:
        # Tratamento seguro para partidas que ainda não ocorreram (placar nulo)
        score_ft = match.get("score", {}).get("fullTime", {})
        gols_mandante = score_ft.get("home") if score_ft else None
        gols_visitante = score_ft.get("away") if score_ft else None
        
        lista.append({
            "id_partida": match["id"],
            "rodada": match["matchday"],
            "data_utc": match["utcDate"],
            "status": match["status"],
            "mandante": match["homeTeam"]["name"],
            "visitante": match["awayTeam"]["name"],
            "gols_mandante": gols_mandante if gols_mandante is not None else 0,
            "gols_visitante": gols_visitante if gols_visitante is not None else 0,
            "vencedor": match.get("score", {}).get("winner")
        })
    return pd.DataFrame(lista)

def carregar_no_sqlite(df_tabela, df_partidas):
    conn = sqlite3.connect("futebol.db")
    
    if df_tabela is not None:
        df_tabela.to_sql("tabela_brasileirao", conn, if_exists="replace", index=False)
        print("-> Tabela de classificação salva com sucesso!")
        
    if df_partidas is not None:
        df_partidas.to_sql("partidas_brasileirao", conn, if_exists="replace", index=False)
        print("-> Dados de partidas salvos com sucesso!")
        
    conn.close()
    print("Processo ETL completo finalizado!")

if __name__ == "__main__":
    print("Iniciando extração da API de Futebol...")
    
    # Extrai Classificação
    dados_standings = extrair_dados_api("standings")
    df_tabela = processar_tabela(dados_standings)
    
    # Extrai Partidas
    dados_matches = extrair_dados_api("matches")
    df_partidas = processar_partidas(dados_matches)
    
    # Carga no Banco
    carregar_no_sqlite(df_tabela, df_partidas)