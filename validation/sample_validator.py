"""
Módulo de validação de resultados em amostras
AULA 10: Comparação de DataFrames e verificação de integridade
"""
import pandas as pd
import os
import sys

# Adicionar o diretório pai (raiz) ao path para importar src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import load_data_from_zip
from src.preprocessing import preprocess_all
from src.config import TABLES_PATH

def validate_rpg_sample():
    """Valida se as estatísticas de RPG em rpg_stats.csv estão corretas"""
    print("🧪 Verificando integridade de 'rpg_stats.csv'...")
    
    # 1. Carregar o resultado gerado
    stats_file = os.path.join(TABLES_PATH, 'rpg_stats.csv')
    if not os.path.exists(stats_file):
        print("❌ Erro: Arquivo 'rpg_stats.csv' não encontrado! Execute main.py primeiro.")
        return False
        
    df_results = pd.read_csv(stats_file)
    
    # 2. Recalcular a partir dos dados brutos
    df_raw = load_data_from_zip()
    df = preprocess_all(df_raw)
    
    # Filtrar RPGs
    df_rpg = df[df['genres'].str.contains('role-playing', case=False, na=False)]
    
    # Validar média de DLCs
    media_real = round(df_rpg['dlc_count'].mean(), 2)
    media_no_csv = df_results[df_results['Métrica'] == 'DLCs']['Média'].values[0]
    
    if abs(media_real - media_no_csv) < 0.01:
        print(f"✅ Média de DLCs confirmada: {media_real}")
    else:
        print(f"❌ Inconsistência na média de DLCs: {media_no_csv} (CSV) vs {media_real} (Real)")
        return False
        
    # Validar máximo de avaliações positivas
    max_real = int(df_rpg['positive'].max())
    max_no_csv = int(df_results[df_results['Métrica'] == 'Avaliações Positivas']['Máximo'].values[0])
    
    if max_real == max_no_csv:
        print(f"✅ Máximo de avaliações confirmada: {max_real}")
    else:
        print(f"❌ Inconsistência no máximo de avaliações: {max_no_csv} (CSV) vs {max_real} (Real)")
        return False

    print("\n✨ Validação de amostra concluída com sucesso!")
    return True

if __name__ == "__main__":
    validate_rpg_sample()