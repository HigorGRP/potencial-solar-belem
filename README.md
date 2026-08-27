# ☀️ Análise de Potencial Solar vs. Geração Fotovoltaica Real (Belém-PA)

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
[![Streamlit App](https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge&logo=streamlit)](https://potencial-solar-belem-higor.streamlit.app/)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-BigQuery-orange?style=for-the-badge&logo=googlecloud)
![Power BI](https://img.shields.io/badge/Power_BI-Prototipagem-yellow?style=for-the-badge&logo=powerbi)
![Automation](https://img.shields.io/badge/GitHub_Actions-Automated_ETL-green?style=for-the-badge&logo=githubactions)

> **🔗 Acesse o Dashboard Online:** https://potencial-solar-belem-higor.streamlit.app/

## 📌 Sobre o Projeto

Este projeto nasceu da ideia de validar se os dados meteorológicos públicos (radiação solar, temperatura e umidade) seriam capazes de prever com precisão a eficiência de geração de energia no mundo real. 

Inicialmente, **estruturei um protótipo de validação utilizando Power BI** com arquivos locais para confrontar os indicadores climáticos com os relatórios de produção diária do meu próprio sistema fotovoltaico residencial (~8.5 kW). Com o sucesso da prova de conceito, evoluí o projeto para uma arquitetura de dados profissional e escalável: construí uma pipeline de ETL em Python consumindo a API da Open-Meteo, automatizei sua orquestração diária, armazenei os dados em um Data Warehouse na nuvem (**Google BigQuery**) e publiquei um Data App interativo e em tempo real utilizando **Streamlit** e **Plotly**.

---

## ⚡ Validação Prática: Prototipagem (Power BI) vs. Aplicação em Nuvem (Streamlit)

A grande virada analítica do projeto foi confrontar a teoria dos dados com a prática da geração solar real em diferentes etapas de maturidade:

| Prototipagem Inicial (Power BI) | Solução Final em Nuvem (Streamlit App) |
| :---: | :---: |
| ![Dashboard Power BI](dashboard.png) | ![Dashboard Streamlit](dashboard_streamlit.png) *(Substitua pelo nome da sua print do Streamlit, se tiver)* |

* **Aderência da Curva:** A janela de pico de radiação prevista (entre **10h e 15h**) coincide perfeitamente com o período de máxima geração registrada pelo inversor real.
* **Sensibilidade às Nuvens:** As oscilações bruscas no gráfico refletem as flutuações instantâneas de cobertura de nuvens e umidade capturadas pelo modelo meteorológico.

---

## 🏗️ Arquitetura e Orquestração da Pipeline de Dados
[🌐 API Open-Meteo] ➔ [⚙️ ETL Automatizado (GitHub Actions)] ➔ [☁️ Google BigQuery (Data Warehouse)] ➔ [⚡ Streamlit App (Cloud Deploy)]

1. **Extração e Orquestração (ETL Diário):** Pipeline em Python programada e orquestrada de forma automatizada (via GitHub Actions), buscando os dados atualizados na API Open-Meteo e injetando no BigQuery sem intervenção manual.
2. **Engenharia de Dados (Python):**
   * Tratamento de séries temporais com `pandas` (`data` e `hora`).
   * Aplicação de regras de negócio para classificar o **Status de Potencial Solar** em *Alto Potencial*, *Baixo Potencial* e *Sem Geração (Noite)*.
3. **Data App & Cloud (Streamlit):**
   * Dashboard interativo em Dark Mode hospedado na nuvem (Streamlit Community Cloud).
   * Conexão segura em tempo real com o BigQuery via secrets (`TOML`) e credenciais de serviço.
   * **Eixo Y Secundário** no gráfico de linhas de Plotly para cruzar a Irradiância Solar ($W/m^2$) com a Temperatura ($°C$).

---

## 🔍 Principais Insights

* **Máxima Irradiância:** A radiação solar atingiu o pico de **774,40 W/m²**.
* **Aproveitamento Operacional:** **45,83%** das horas monitoradas no dia apresentaram **Alto Potencial** de geração.
* **Produção Resultante:** A conjuntura climática analisada permitiu uma geração real diária de **45,3 kWh** no sistema fotovoltaico.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem & Bibliotecas:** Python (`pandas`, `numpy`, `requests`, `plotly`, `google-cloud-bigquery`)
* **Orquestração & Automação:** GitHub Actions (ETL Diário Automatizado)
* **Data Warehouse & Cloud:** Google Cloud Platform (BigQuery), Streamlit Cloud
* **Business Intelligence (Prototipagem):** Power BI (Power Query, DAX)
* **Fontes de Dados:** API REST (Open-Meteo Weather Forecast) & Inversor Fotovoltaico Residencial
