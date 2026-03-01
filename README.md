# 🛣️ Pipeline de Pedágio Automático: Ingestão & Governança de Dados

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)

Este projeto simula um sistema de **Data Toll (Pedágio de Dados)**, onde arquivos brutos de transações bancárias passam por um rigoroso processo de limpeza, validação e tipagem antes de serem consolidados em um banco de dados relacional.

## 🎯 Objetivo do Projeto
Automatizar a chegada de dados diários, garantindo que apenas registros íntegros cheguem à camada final de análise (Silver/Gold), enquanto dados corrompidos são isolados para auditoria.

---

## 🏗️ Arquitetura da Solução

1.  **Source:** Arquivos `.csv` depositados na pasta `/data`.
2.  **Orquestração:** O **GitHub Actions** monitora o repositório e dispara o pipeline automaticamente a cada 30 minutos (ou via gatilho manual).
3.  **Processing (Python):** * Leitura dinâmica de múltiplos arquivos.
    * Tratamento de nulos e conversão de tipos (Datas, Valores, IDs).
    * Aplicação de regras de negócio para separar dados "Limpis" de "Erros".
4.  **Destination (Cloud Database):** Ingestão via API para o **Supabase (PostgreSQL)**.
5.  **Data Governance:** Uso de *Primary Keys* para prevenir duplicidade de dados (Idempotência).

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.11
* **Manipulação de Dados:** Pandas
* **Banco de Dados:** Supabase / PostgreSQL
* **Automação:** GitHub Actions (YAML)
* **Segurança:** GitHub Secrets (para ocultar credenciais de API)

---

## 📊 Visualização dos Resultados

### Painel de Controle no Supabase
Os dados processados podem ser visualizados em tempo real no dashboard do Supabase, permitindo auditoria rápida de transações processadas vs. erros encontrados.

> **Status do Pipeline:** Atualmente, o fluxo de ingestão e limpeza está 100% operacional. O arquivamento físico de logs no repositório está em roadmap de melhorias de infraestrutura.

---

## 🚀 Como Executar

1. Clone o repositório:
   ```bash
   git clone [https://github.com/SEU_USUARIO/pipeline-banc-rio-automatizado.git](https://github.com/SEU_USUARIO/pipeline-banc-rio-automatizado.git)
