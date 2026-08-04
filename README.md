# ☀️ Análise de Potencial Solar vs. Geração Fotovoltaica Real (Belém-PA)

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Power BI](https://img.shields.io/badge/Power_BI-Dashboard-yellow?style=for-the-badge&logo=powerbi)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?style=for-the-badge&logo=pandas)

## 📌 Sobre o Projeto

Este projeto nasceu da ideia de validar se os dados meteorológicos públicos (radiação solar, temperatura e umidade) seriam capazes de prever com precisão a eficiência de geração de energia no mundo real. 

Para isso, construí uma pipeline de dados em Python para consumir a API REST da Open-Meteo para a região de Belém-PA e criei um dashboard no Power BI para a visualização. A validação prática do modelo foi feita comparando os indicadores climáticos simulados diretamente com os **relatórios de produção diária do meu próprio sistema fotovoltaico residencial (8.5 kW)**.

---

## ⚡ Validação Prática: Modelo Climático vs. Placas Solares

A grande virada analítica do projeto foi confrontar a teoria dos dados com a prática da geração solar real:

| Dashboard Climático (Power BI) | Relatório Real do Inversor |
| :---: | :---: |
| ![Dashboard Power BI](dashboard.png) | ![Relatório Inversor](painel_solar.png.jpeg) |

* **Aderência da Curva:** A janela de pico de radiação prevista no dashboard (entre **10h e 15h**) coincide com o período de máxima geração registrada pelo aplicativo das placas.
* **Sensibilidade às Nuvens:** As oscilações bruscas no gráfico de produção real (efeito "dente de serra") refletem as flutuações instantâneas de cobertura de nuvens e umidade capturadas pelo modelo.

---

## 🏗️ Arquitetura da Pipeline de Dados
