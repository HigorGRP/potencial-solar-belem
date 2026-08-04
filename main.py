import os
import numpy as np
import pandas as pd
import requests

# 1. Requisição dos dados de clima na API (Belém-PA)
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": -1.4558,
    "longitude": -48.4902,
    "hourly": "temperature_2m,relative_humidity_2m,direct_normal_irradiance",
    "timezone": "America/Sao_Paulo",
}

print("🔌 Conectando à API...")
response = requests.get(url, params=params)

if response.status_code == 200:
    dados = response.json()
    df_raw = pd.DataFrame(dados["hourly"])
    print("✅ Dados extraídos com sucesso!")
else:
    print(f"❌ Erro: {response.status_code}")


# 2. Função de limpeza e tratamento dos dados
def tratar_dados(df):
    print("🧹 Tratando dados...")
    df_clean = df.copy()

    # Converter tempo e extrair Data e Hora
    df_clean["time"] = pd.to_datetime(df_clean["time"])
    df_clean["data"] = df_clean["time"].dt.date
    df_clean["hora"] = df_clean["time"].dt.hour

    # Renomear colunas para português
    novos_nomes = {
        "temperature_2m": "temperatura_c",
        "relative_humidity_2m": "umidade_pct",
        "direct_normal_irradiance": "irradiancia_solar",
    }
    df_clean.rename(columns=novos_nomes, inplace=True)

    # Classificar potencial solar baseado na radiação (W/m²)
    condicoes = [
        (df_clean["irradiancia_solar"] > 200),
        (
            (df_clean["irradiancia_solar"] > 0)
            & (df_clean["irradiancia_solar"] <= 200)
        ),
        (df_clean["irradiancia_solar"] == 0),
    ]
    categorias = ["Alto Potencial", "Baixo Potencial", "Sem Geração (Noite)"]

    df_clean["status_geracao_solar"] = np.select(
        condicoes, categorias, default="Outro"
    )

    # Selecionar e ordenar colunas finais
    colunas_finais = [
        "data",
        "hora",
        "temperatura_c",
        "umidade_pct",
        "irradiancia_solar",
        "status_geracao_solar",
    ]

    print("✅ Tratamento concluído!")
    return df_clean[colunas_finais]


# 3. Função para salvar em CSV
def salvar_dados(df, nome_arquivo="dados_clima_energia.csv"):
    print("💾 Salvando arquivo...")
    try:
        df.to_csv(nome_arquivo, index=False, encoding="utf-8-sig", sep=";")
        print(f"✅ Arquivo salvo em: {nome_arquivo}")
    except Exception as e:
        print(f"❌ Erro ao salvar: {e}")


# Execução do script
if "df_raw" in locals() or "df_raw" in globals():
    df_tratado = tratar_dados(df_raw)
    salvar_dados(df_tratado)
# %%
