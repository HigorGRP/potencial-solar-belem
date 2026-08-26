import os
import json
import requests
import numpy as np
import pandas as pd
from google.cloud import bigquery
from typing import Optional

# Se estiver rodando no GitHub Actions, cria o arquivo temporário com a chave da Secret
if "GCP_SA_KEY" in os.environ:
    creds_json = os.environ["GCP_SA_KEY"]
    with open("credenciais.json", "w") as f:
        f.write(creds_json)


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credenciais.json"

def extrair_dados_clima(lat: float, lon: float) -> Optional[dict]:
    """Realiza a requisição dos dados de previsão do tempo na API Open-Meteo."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relative_humidity_2m,direct_normal_irradiance",
        "timezone": "America/Sao_Paulo",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição da API: {e}")
        return None

def tratar_dados(dados_json: dict) -> pd.DataFrame:
    """Realiza a limpeza, tratamento e engenharia de atributos."""
    df_clean = pd.DataFrame(dados_json["hourly"])

    df_clean["time"] = pd.to_datetime(df_clean["time"])
    df_clean["data"] = df_clean["time"].dt.date.astype(str)
    df_clean["hora"] = df_clean["time"].dt.hour

    novos_nomes = {
        "temperature_2m": "temperatura_c",
        "relative_humidity_2m": "umidade_pct",
        "direct_normal_irradiance": "irradiancia_solar",
    }
    df_clean.rename(columns=novos_nomes, inplace=True)

    condicoes = [
        (df_clean["irradiancia_solar"] > 200),
        ((df_clean["irradiancia_solar"] > 0) & (df_clean["irradiancia_solar"] <= 200)),
        (df_clean["irradiancia_solar"] == 0),
    ]
    categorias = ["Alto Potencial", "Baixo Potencial", "Sem Geração (Noite)"]

    df_clean["status_geracao_solar"] = np.select(condicoes, categorias, default="Outro")

    colunas_finais = [
        "data",
        "hora",
        "temperatura_c",
        "umidade_pct",
        "irradiancia_solar",
        "status_geracao_solar",
    ]

    return df_clean[colunas_finais]

def carregar_no_bigquery(df: pd.DataFrame, project_id: str, dataset_id: str, table_id: str) -> None:
    """Carrega o DataFrame tratado diretamente para uma tabela no Google Cloud BigQuery."""
    client = bigquery.Client(project=project_id)
    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
    )

    try:
        job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        job.result()
        print(f"Dados carregados com sucesso para: {table_ref}")
    except Exception as e:
        print(f"Erro ao carregar dados no BigQuery: {e}")

if __name__ == "__main__":
    LATITUDE_BELEM = -1.4558
    LONGITUDE_BELEM = -48.4902
    
    PROJECT_ID = "potencial-solar-belem" 
    DATASET_ID = "clima_belem"
    TABLE_ID = "potencial_solar"

    dados_brutos = extrair_dados_clima(LATITUDE_BELEM, LONGITUDE_BELEM)
    
    if dados_brutos and "hourly" in dados_brutos:
        df_tratado = tratar_dados(dados_brutos)
        
        # Backup local em CSV
        df_tratado.to_csv("dados_clima_energia.csv", index=False, encoding="utf-8-sig", sep=";")
        
        # Envio ativo para o Google Cloud BigQuery
        carregar_no_bigquery(df_tratado, PROJECT_ID, DATASET_ID, TABLE_ID)