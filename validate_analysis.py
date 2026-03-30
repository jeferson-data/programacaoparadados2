"""
Script de validação para conferência manual de resultados
AULA 10: Verificação de consistência e integridade dos dados
"""
from src.data_loader import load_data_from_zip, get_data_info
from src.preprocessing import preprocess_all
from src.analysis import set_silent_mode
import os

def run_validation():
    print("\n" + "="*60)
    print("🔍 VALIDANDO RESULTADOS DA ANÁLISE")
    print("="*60)
    
    # Desativar mensagens internas para focar no resumo
    set_silent_mode(True)
    
    try:
        # 1. Carregar
        print("1. Carregando dados...")
        df_raw = load_data_from_zip()
        
        # 2. Pré-processar
        print("2. Aplicando pré-processamento...")
        df = preprocess_all(df_raw)
        
        # 3. Validar métricas básicas
        print("\n📈 MÉTRICAS DE VALIDAÇÃO:")
        print(f"   - Total de jogos: {len(df):,}")
        
        # Validação de tipos
        print(f"   - Coluna 'price' é numérica: {df['price'].dtype.kind in 'if'}")
        print(f"   - Coluna 'release_year' ok: {df['release_year'].notna().any()}")
        
        # Validação de lógica
        jogos_pagos = df['is_paid'].sum()
        jogos_gratis = (~df['is_paid']).sum()
        total = len(df)
        
        print(f"   - Soma de pagos ({jogos_pagos:,}) + grátis ({jogos_gratis:,}) = Total ({total:,})")
        
        if (jogos_pagos + jogos_gratis) == total:
            print("\n✅ CONSISTÊNCIA DE DADOS: OK")
        else:
            print("\n❌ INCONSISTÊNCIA DETECTADA na contagem de jogos!")
            
        print("\n" + "="*60)
        print("✨ VALIDAÇÃO CONCLUÍDA")
        print("="*60)

    except Exception as e:
        print(f"\n❌ ERRO DURANTE A VALIDAÇÃO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_validation()
