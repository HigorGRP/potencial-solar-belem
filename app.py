# Módulo: app.py
# Descrição: Data App interativo desenvolvido em Streamlit para visualização e análise
#            de dados meteorológicos e de potencial de geração solar em Belém-PA.
#            Consome os dados diretamente do Google BigQuery em tempo real.
# Autor: Higor Gabriel
# Stack: Streamlit, Pandas, Plotly, Google Cloud BigQuery

import os
import json
import tempfile
import streamlit as st
from google.cloud import bigquery
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA E ESTILIZAÇÃO VISUAL
# ==========================================

# Configura o layout da página para modo expandido (wide) e define metadados da aba
st.set_page_config(
    page_title="Dashboard de Análise de Potencial Solar & Clima",
    page_icon="☀️",
    layout="wide"
)

# Injeção de CSS customizado para Dark Mode e padronização de margens/espaçamentos
st.markdown("""
    <style>
        .main {
            background-color: #0b192c;
        }
        h1, h2, h3 {
            color: #ffffff !important;
        }
        /* Reduz espaçamentos gerais para otimizar o layout em uma única tela */
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 1rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CONFIGURAÇÃO DE CREDENCIAIS E CONEXÃO
# ==========================================

# Se estiver rodando no Streamlit Cloud, cria o arquivo de credenciais dinamicamente via st.secrets
if "gcp_service_account" in st.secrets:
    creds_dict = dict(st.secrets["gcp_service_account"])
    
    # Cria um arquivo temporário seguro para o cliente do BigQuery ler
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as temp_cred_file:
        json.dump(creds_dict, temp_cred_file)
        temp_cred_path = temp_cred_file.name
        
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_cred_path

# Caso contrário, tenta usar o arquivo JSON local tradicional
elif os.path.exists("credenciais.json"):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credenciais.json"

# Constantes de infraestrutura do Google Cloud Platform (GCP)
PROJECT_ID = "potencial-solar-belem"
DATASET_ID = "clima_belem"
TABLE_ID = "potencial_solar"

@st.cache_data(ttl=1800)
def carregar_dados_bigquery() -> pd.DataFrame:
    """
    Realiza a consulta SQL diretamente no Google BigQuery com cache otimizado.
    O cache possui TTL de 30 minutos (1800 segundos) para evitar requisições excessivas.
    """
    client = bigquery.Client(project=PROJECT_ID)
    query = f"""
        SELECT data, hora, temperatura_c, umidade_pct, irradiancia_solar, status_geracao_solar
        FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
        ORDER BY data, hora
    """
    df = client.query(query).to_dataframe()
    return df

# ==========================================
# 3. CONSTRUÇÃO DA INTERFACE E DOS COMPONENTES
# ==========================================

# Título Principal do Dashboard
st.markdown("<h3 style='text-align: center; color: white;'>Dashboard de Análise de Potencial Solar & Clima</h3>", unsafe_allow_html=True)
st.markdown("---")

try:
    # Carrega os dados da nuvem
    df = carregar_dados_bigquery()
    
    if df.empty:
        st.warning("A tabela no BigQuery está vazia.")
    else:
        # ------------------------------------------
        # FILTROS (BARRA LATERAL)
        # ------------------------------------------
        st.sidebar.header("Filtros do Painel")
        datas_disponiveis = df["data"].unique()
        data_selecionada = st.sidebar.selectbox("Selecione a Data:", datas_disponiveis)
        
        # Filtra o DataFrame de acordo com a data escolhida pelo usuário
        df_filtrado = df[df["data"] == data_selecionada]
        
        # ------------------------------------------
        # CARDS DE MÉTRICAS (KPIS) SUPERIORES
        # ------------------------------------------
        col1, col2, col3 = st.columns(3)
        
        # Cálculo das métricas agregadas para o dia selecionado
        temp_media = df_filtrado["temperatura_c"].mean()
        irradiancia_max = df_filtrado["irradiancia_solar"].max()
        umidade_media = df_filtrado["umidade_pct"].mean()
        
        with col1:
            st.metric(label="MÉDIA TEMPERATURA", value=f"{temp_media:.2f} °C")
        with col2:
            st.metric(label="RADIAÇÃO SOLAR MÁXIMA", value=f"{irradiancia_max:.2f} W/m²")
        with col3:
            st.metric(label="MÉDIA UMIDADE", value=f"{umidade_media:.2f} %")
            
        # ------------------------------------------
        # SEÇÃO DE GRÁFICOS INTERATIVOS (PLOTLY)
        # ------------------------------------------
        col_graf1, col_graf2 = st.columns(2)
        
        # Gráfico 1: Linhas com Eixo Duplo (Irradiância Solar vs Temperatura por Hora)
        with col_graf1:
            st.markdown("<p style='color: white; font-weight: bold; margin-bottom: 0px;'>RADIAÇÃO SOLAR X TEMPERATURA/HORA</p>", unsafe_allow_html=True)
            
            fig_linha = go.Figure()
            
            # Traço principal: Irradiância Solar (Eixo Y esquerdo)
            fig_linha.add_trace(go.Scatter(
                x=df_filtrado["hora"], 
                y=df_filtrado["irradiancia_solar"],
                name="Irradiância",
                line=dict(color="#ffd700", width=2.5)
            ))
            
            # Traço secundário: Temperatura (Eixo Y direito)
            fig_linha.add_trace(go.Scatter(
                x=df_filtrado["hora"], 
                y=df_filtrado["temperatura_c"],
                name="Temperatura",
                yaxis="y2",
                line=dict(color="#ff4d4d", width=2.5)
            ))
            
            # Layout e estilização do gráfico de linhas
            fig_linha.update_layout(
                paper_bgcolor="#0b192c",
                plot_bgcolor="#0b192c",
                font=dict(color="white", size=10),
                xaxis=dict(title="", gridcolor="#223a5e"),
                yaxis=dict(title="", gridcolor="#223a5e"),
                yaxis2=dict(title="", overlaying="y", side="right", showgrid=False),
                legend=dict(orientation="h", y=1.2, x=0, font=dict(color="white", size=9)),
                margin=dict(l=10, r=10, t=10, b=10),
                height=280  # Altura compactada
            )
            st.plotly_chart(fig_linha, use_container_width=True, key="grafico_linhas_solar")
            
        # Gráfico 2: Gráfico de Rosca (Distribuição do Status de Geração Solar)
        with col_graf2:
            st.markdown("<p style='color: white; font-weight: bold; margin-bottom: 0px;'>DISTRIBUIÇÃO DE POTENCIAL SOLAR (DIÁRIO)</p>", unsafe_allow_html=True)
            
            df_status = df_filtrado["status_geracao_solar"].value_counts().reset_index()
            df_status.columns = ["status_geracao_solar", "quantidade"]
            
            if not df_status.empty:
                fig_pizza = px.pie(
                    df_status, 
                    names="status_geracao_solar", 
                    values="quantidade",
                    hole=0.5,
                    color_discrete_sequence=["#ffd700", "#555555", "#ff7f0e"]
                )
                
                # Layout e estilização do gráfico de rosca
                fig_pizza.update_layout(
                    paper_bgcolor="#0b192c",
                    plot_bgcolor="#0b192c",
                    font=dict(color="white", size=10),
                    legend=dict(orientation="v", y=0.5, x=1.0, font=dict(color="white", size=9)),
                    margin=dict(l=10, r=10, t=10, b=10),
                    height=280  
                )
                st.plotly_chart(fig_pizza, use_container_width=True, key="grafico_rosca_solar")
            else:
                st.info("Sem dados de status solar para esta data.")

except Exception as e:
    # Tratamento global de exceções para falhas de conexão com o Data Warehouse
    st.error(f"Erro ao conectar com o BigQuery ou carregar os dados: {e}")
