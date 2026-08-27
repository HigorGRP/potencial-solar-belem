# ☀️ Análise de Potencial Solar vs. Geração Fotovoltaica Real (Belém-PA)

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
[![Streamlit App](https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge&logo=streamlit)](https://potencial-solar-belem-higor.streamlit.app/)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-BigQuery-orange?style=for-the-badge&logo=googlecloud)
![Power BI](https://img.shields.io/badge/Power_BI-Prototipagem-yellow?style=for-the-badge&logo=powerbi)
![Automation](https://img.shields.io/badge/GitHub_Actions-Automated_ETL-green?style=for-the-badge&logo=githubactions)

> **🔗 Acesse o Dashboard Online:** https://potencial-solar-belem-higor.streamlit.app/

## 📌 Sobre o Projeto

Este projeto nasceu da ideia de validar se os dados meteorológicos públicos (radiação solar, temperatura e umidade) seriam capazes de prever com precisão a eficiência de geração de energia no mundo real. 

Inicialmente, **estruturei um protótipo de validação utilizando Power BI** com arquivos locais para confrontar os indicadores climáticos com os relatórios de produção diária do meu próprio sistema fotovoltaico residencial (~8.5 kW). Com o sucesso da prova de conceito, evoluí o projeto para uma arquitetura de dados: construí uma pipeline de ETL em Python consumindo a API da Open-Meteo, automatizei sua orquestração diária, armazenei os dados em um Data Warehouse na nuvem (**Google BigQuery**) e publiquei um Data App interativo e em tempo real utilizando **Streamlit** e **Plotly**.

---

## ⚡ Validação Prática: Modelo vs. Geração Real Residencial

A grande virada analítica do projeto foi confrontar a teoria dos dados com a prática da geração solar real da minha residência:

| Prototipagem Inicial (Power BI) | Relatório Real do Inversor (App Residencial) |
| :---: | :---: | :---: |
| ![Dashboard Power BI](dashboard.png) | ![Relatório Inversor](painel_solar.png.jpeg) | ![Painel Streamlit](painel_streamlit.png.)

* **Aderência da Curva:** A janela de pico de radiação prevista no modelo (entre **10h e 15h**) coincide perfeitamente com o período de máxima geração registrada pelo aplicativo das placas em casa.
* **Sensibilidade às Nuvens:** As oscilações bruscas no gráfico refletem as flutuações instantâneas de cobertura de nuvens e umidade capturadas pela API meteorológica.

---

## 🏗️ Arquitetura e Orquestração da Pipeline de Dados

Abaixo está o fluxo automatizado de engenharia de dados do projeto:

```mermaid
graph TD
    A["🌐 API Open-Meteo<br>(Fonte Meteorológica)"] -->|Consumo Diário| B["⚙️ GitHub Actions<br>(Orquestração & ETL Python)"]
    B -->|Carga de Dados| C["☁️ Google BigQuery<br>(Data Warehouse na Nuvem)"]
    C -->|Consulta em Tempo Real| D["⚡ Streamlit App<br>(Dashboard Interativo)"]
    
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333,stroke-width:2px
    style C fill:#ff9,stroke:#333,stroke-width:2px
    style D fill:#bfb,stroke:#333,stroke-width:2px
