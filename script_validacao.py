import pandas as pd
import os
from database import subir_dados
import shutil

# 1. Configuração de caminhos DINÂMICA
pasta_data = 'data'

# Em vez de lista fixa, pegamos todos os CSVs da pasta
arquivos_lotes = [f for f in os.listdir(pasta_data) if f.endswith('.csv')]

print(f"--- Iniciando: {len(arquivos_lotes)} arquivos encontrados ---")

for arquivo in arquivos_lotes:
    caminho_arquivo = os.path.join(pasta_data, arquivo)
    
    # Adicione este log para debugar no GitHub
    print(f"Lendo arquivo: {caminho_arquivo}")
    
    if os.path.exists(caminho_arquivo):
        print(f"\nProcessando: {arquivo}")
        df = pd.read_csv(caminho_arquivo)

        # --- REGRAS DE QUALIDADE ---
        duplicados = df.duplicated(subset=['id_transacao'], keep='first')
        nulos = df['valor'].isnull()
        negativos = df['valor'].fillna(0) < 0

        mask_erros = duplicados | nulos | negativos
        
        df_bom = df[~mask_erros]
        df_erro = df[mask_erros].copy()

        # --- ENVIO PARA O SUPABASE (DENTRO DO LOOP) ---
        
        # 1. Se houver dados bons, sobe para a tabela principal
        if not df_bom.empty:
            print(f"✅ {len(df_bom)} linhas validadas. Subindo para Supabase...")
            subir_dados(df_bom, "transacoes")
            # Log local
            df_bom.to_csv('dados_limpos_silver.csv', mode='a', index=False, header=not os.path.exists('dados_limpos_silver.csv'))

        # 2. Se houver erros, sobe para a quarentena
        if not df_erro.empty:
            print(f"⚠️ {len(df_erro)} erros encontrados! Enviando para quarentena...")
            df_erro['motivo_erro'] = "Duplicado, Nulo ou Negativo"
            subir_dados(df_erro, "quarentena_erros")
            # Log local
            df_erro.to_csv('log_erros_geral.csv', mode='a', index=False, header=not os.path.exists('log_erros_geral.csv'))

        # --- LIMPEZA AUTOMÁTICA ---
        pasta_processados = os.path.join(pasta_data, 'processados')
        if not os.path.exists(pasta_processados):
            os.makedirs(pasta_processados)
        
        # Move o arquivo para não ser lido novamente amanhã
        shutil.move(caminho_arquivo, os.path.join(pasta_processados, arquivo))
        print(f"📦 Arquivo {arquivo} arquivado com sucesso.")
            
    else:
        print(f"Arquivo {arquivo} não encontrado.")

print("\n--- Processo Finalizado com Sucesso ---")