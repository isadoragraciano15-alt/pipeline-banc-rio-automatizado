import os
import pandas as pd # Adicionamos esse import para o tratamento de nulos
from supabase import create_client
from dotenv import load_dotenv

# O comando abaixo lê o arquivo .env e carrega as informações na memória
load_dotenv()

def get_supabase_client():
    # Buscamos os valores usando os nomes das etiquetas definidas no .env
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        raise ValueError("ERRO: O Python não encontrou as chaves no arquivo .env!")
        
    return create_client(url, key)

def subir_dados(df, nome_tabela):
    supabase = get_supabase_client()
    
    # --- A ÚNICA MUDANÇA É AQUI ---
    # Convertemos o que é NaN (vazio) para None (nulo do banco)
    df_limpo = df.astype(object).where(pd.notnull(df), None)
    dados = df_limpo.to_dict(orient='records')

    try:
        response = supabase.table(nome_tabela).insert(dados).execute()
        print(f"✅ Sucesso! Dados inseridos em: {nome_tabela}")
        return response
    except Exception as e:
        print(f"❌ Erro ao subir dados: {e}")
        raise e