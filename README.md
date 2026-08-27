# ☀️ Análise de Potencial Solar vs. Geração Fotovoltaica Real (Belém-PA)

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
[![Streamlit App](https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge&logo=streamlit)](https://potencial-solar-belem-higor.streamlit.app/)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-BigQuery-orange?style=for-the-badge&logo=googlecloud)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?style=for-the-badge&logo=pandas)

## 📌 Sobre o Projeto

Este projeto nasceu da ideia de validar se os dados meteorológicos públicos (radiação solar, temperatura e umidade) seriam capazes de prever com precisão a eficiência de geração de energia no mundo real. 

Para isso, construí uma pipeline de dados em Python para consumir a API REST da Open-Meteo para a região de Belém-PA, armazenei e gerenciei os dados em um Data Warehouse na nuvem (**Google BigQuery**) e desenvolvi um Data App interativo e em tempo real utilizando **Streamlit** e **Plotly**. A validação prática do modelo foi feita comparando os indicadores climáticos diretamente com os **relatórios de produção diária do meu próprio sistema fotovoltaico residencial (~8.5 kW)**.

---

## ⚡ Validação Prática: Modelo Climático vs. Placas Solares

A grande virada analítica do projeto foi confrontar a teoria dos dados com a prática da geração solar real:

* **Aderência da Curva:** A janela de pico de radiação prevista no dashboard (entre **10h e 15h**) coincide com o período de máxima geração registrada pelo aplicativo das placas.
* **Sensibilidade às Nuvens:** As oscilações bruscas no gráfico de produção real refletem as flutuações instantâneas de cobertura de nuvens e umidade capturadas pelo modelo.

---

## 🏗️ Arquitetura da Pipeline de Dados
[🌐 API Open-Meteo] ➔ [🐍 Script ETL em Python] ➔ [☁️ Google BigQuery (Data Warehouse)] ➔ [⚡ Streamlit App (Cloud Deploy)]

1. **Extração e Carga (ETL):** Consumo automatizado via API REST meteorológica da Open-Meteo e ingestão no Google BigQuery.
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
* **Data App & Cloud:** Streamlit Cloud, Google Cloud Platform (BigQuery)
* **Fontes de Dados:** API REST (Open-Meteo Weather Forecast) & Inversor Fotovoltaico Residencial
