import streamlit as st
from google.cloud import bigquery
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go

# Configuração da página (Layout Amplo)
st.set_page_config(
    page_title="Dashboard de Análise de Potencial Solar & Clima",
    page_icon="☀️",
    layout="wide"
)

# Estilização visual compacta para caber em uma tela
st.markdown("""
    <style>
        .main {
            background-color: #0b192c;
        }
        h1, h2, h3 {
            color: #ffffff !important;
        }
        /* Reduz espaçamentos gerais para caber em uma única tela */
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 1rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Configuração de credenciais para ambiente local (se houver o arquivo)
if os.path.exists("credenciais.json"):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credenciais.json"

PROJECT_ID = "potencial-solar-belem"
DATASET_ID = "clima_belem"
TABLE_ID = "potencial_solar"

@st.cache_data(ttl=1800)
def carregar_dados_bigquery():
    """Consulta os dados diretamente do BigQuery."""
    client = bigquery.Client(project=PROJECT_ID)
    query = f"""
        SELECT data, hora, temperatura_c, umidade_pct, irradiancia_solar, status_geracao_solar
        FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
        ORDER BY data, hora
    """
    df = client.query(query).to_dataframe()
    return df

# Título Principal mais compacto
st.markdown("<h3 style='text-align: center; color: white;'>Dashboard de Análise de Potencial Solar & Clima</h3>", unsafe_allow_html=True)
st.markdown("---")

try:
    df = carregar_dados_bigquery()
    
    if df.empty:
        st.warning("A tabela no BigQuery está vazia.")
    else:
        # Filtro de Data na Barra Lateral
        st.sidebar.header("Filtros do Painel")
        datas_disponiveis = df["data"].unique()
        data_selecionada = st.sidebar.selectbox("Selecione a Data:", datas_disponiveis)
        
        # Filtrando o DataFrame para o dia escolhido
        df_filtrado = df[df["data"] == data_selecionada]
        
        # ==========================================
        # CARDS DE MÉTRICAS (KPIs) SUPERIORES
        # ==========================================
        col1, col2, col3 = st.columns(3)
        
        temp_media = df_filtrado["temperatura_c"].mean()
        irradiancia_max = df_filtrado["irradiancia_solar"].max()
        umidade_media = df_filtrado["umidade_pct"].mean()
        
        with col1:
            st.metric(label="MÉDIA TEMPERATURA", value=f"{temp_media:.2f} °C")
        with col2:
            st.metric(label="RADIAÇÃO SOLAR MÁXIMA", value=f"{irradiancia_max:.2f} W/m²")
        with col3:
            st.metric(label="MÉDIA UMIDADE", value=f"{umidade_media:.2f} %")
            
        # ==========================================
        # SEÇÃO DE GRÁFICOS (Compactados para caber na tela)
        # ==========================================
        col_graf1, col_graf2 = st.columns(2)
        
        with col_graf1:
            st.markdown("<p style='color: white; font-weight: bold; margin-bottom: 0px;'>RADIAÇÃO SOLAR X TEMPERATURA/HORA</p>", unsafe_allow_html=True)
            
            fig_linha = go.Figure()
            
            fig_linha.add_trace(go.Scatter(
                x=df_filtrado["hora"], 
                y=df_filtrado["irradiancia_solar"],
                name="Irradiância",
                line=dict(color="#ffd700", width=2.5)
            ))
            
            fig_linha.add_trace(go.Scatter(
                x=df_filtrado["hora"], 
                y=df_filtrado["temperatura_c"],
                name="Temperatura",
                yaxis="y2",
                line=dict(color="#ff4d4d", width=2.5)
            ))
            
            fig_linha.update_layout(
                paper_bgcolor="#0b192c",
                plot_bgcolor="#0b192c",
                font=dict(color="white", size=10),
                xaxis=dict(title="", gridcolor="#223a5e"),
                yaxis=dict(title="", gridcolor="#223a5e"),
                yaxis2=dict(title="", overlaying="y", side="right", showgrid=False),
                legend=dict(orientation="h", y=1.2, x=0, font=dict(size=9)),
                margin=dict(l=10, r=10, t=10, b=10),
                height=280  # Altura reduzida para compactar
            )
            st.plotly_chart(fig_linha, use_container_width=True, key="grafico_linhas_solar")
            
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
                
                fig_pizza.update_layout(
                    paper_bgcolor="#0b192c",
                    plot_bgcolor="#0b192c",
                    font=dict(color="white", size=10),
                    legend=dict(orientation="v", y=0.5, x=1.0, font=dict(size=9)),
                    margin=dict(l=10, r=10, t=10, b=10),
                    height=280  # Altura reduzida para compactar
                )
                st.plotly_chart(fig_pizza, use_container_width=True, key="grafico_rosca_solar")
            else:
                st.info("Sem dados de status solar para esta data.")

except Exception as e:
    st.error(f"Erro ao conectar com o BigQuery ou carregar os dados: {e}")