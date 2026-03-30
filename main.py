#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Steam Games Analysis - Projeto Final Fase 2
Arquivo principal para execução completa da análise

Baseado nas aulas 6-10:
- AULA 06: Estruturação de projeto e ambiente
- AULA 07: NumPy para operações vetorizadas
- AULA 09: Matplotlib para visualizações
- AULA 10: Pandas para análise de dados
"""

import argparse
import sys
import os
import time
from datetime import datetime

# Adicionar diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar módulos do projeto
from src.config import apply_custom_style, OUTPUT_PATH, FIGURES_PATH, TABLES_PATH
from src.data_loader import load_data_from_zip, get_data_info, cleanup_temp_files
from src.preprocessing import preprocess_all
from src.analysis import (
    answer_question1, answer_question2, answer_question3,
    answer_question4, answer_question_extra
)
from src.visualizations import (
    create_graph1_os_support, create_graph2_indie_strategy,
    create_graph3_price_distribution
)


def print_header():
    """Imprime cabeçalho do programa"""
    print("=" * 70)
    print("🎮 STEAM GAMES ANALYSIS - PROJETO FINAL FASE 2")
    print("=" * 70)
    print(f"📅 Data e hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"📁 Diretório de saída: {OUTPUT_PATH}")
    print("=" * 70)
    print()


def print_section(title):
    """Imprime seção com destaque"""
    print("\n" + "=" * 70)
    print(f"📌 {title}")
    print("=" * 70)


def display_dataframe(df, title, max_rows=10):
    """
    Exibe um DataFrame formatado no console
    
    AULA 10: Exibição de dados
    """
    print(f"\n{title}:")
    print("-" * 50)
    print(df.to_string(index=False) if len(df) <= max_rows else df.head(max_rows).to_string(index=False))
    if len(df) > max_rows:
        print(f"... e mais {len(df) - max_rows} linhas")


def main():
    """Função principal do programa"""
    
    # AULA 06: argparse - Processamento de argumentos de linha de comando
    parser = argparse.ArgumentParser(
        description='Steam Games Analysis - Análise de dados de jogos da Steam',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--skip-plots', action='store_true',
                        help='Pular geração de gráficos')
    parser.add_argument('--output-dir', type=str, default=None,
                        help='Diretório para salvar os resultados (padrão: ./outputs)')
    parser.add_argument('--clean', action='store_true',
                        help='Limpar arquivos temporários após execução')
    
    args = parser.parse_args()
    
    # Atualizar diretório de saída se especificado
    if args.output_dir:
        from src.config import OUTPUT_PATH as CONFIG_OUTPUT_PATH
        import src.config as config
        config.OUTPUT_PATH = args.output_dir
        config.FIGURES_PATH = os.path.join(args.output_dir, 'figures')
        config.TABLES_PATH = os.path.join(args.output_dir, 'tables')
        config.TEMP_PATH = os.path.join(args.output_dir, 'temp')
        
        for path in [config.OUTPUT_PATH, config.FIGURES_PATH, 
                     config.TABLES_PATH, config.TEMP_PATH]:
            os.makedirs(path, exist_ok=True)
    
    # Imprimir cabeçalho
    print_header()
    
    # Iniciar timer
    start_time = time.time()
    
    # Dicionário para armazenar resultados
    results = {}
    
    try:
        # ============================================
        # PASSO 1: CARREGAR DADOS (AULA 10 - I/O)
        # ============================================
        print_section("PASSO 1: Carregando dados do arquivo ZIP")
        df_raw = load_data_from_zip()
        get_data_info(df_raw)
        
        # ============================================
        # PASSO 2: PRÉ-PROCESSAMENTO (AULA 10 - Limpeza)
        # ============================================
        print_section("PASSO 2: Pré-processamento dos dados")
        df = preprocess_all(df_raw)
        
        # ============================================
        # PASSO 3: ANÁLISES (AULA 10 - Agregações)
        # ============================================
        print_section("PASSO 3: Respondendo às perguntas de negócio")
        
        # Pergunta 1
        print("\n🔍 Pergunta 1: Top 10 jogos mais bem avaliados")
        results['top10'] = answer_question1(df)
        display_dataframe(results['top10'], "Top 10 Jogos")
        
        # Pergunta 2
        print("\n🔍 Pergunta 2: Análise de jogos de RPG")
        results['rpg_stats'] = answer_question2(df)
        display_dataframe(results['rpg_stats'], "Estatísticas RPG")
        
        # Pergunta 3
        print("\n🔍 Pergunta 3: Top 5 publicadoras de jogos pagos")
        results['top_publishers'] = answer_question3(df)
        display_dataframe(results['top_publishers'], "Top 5 Publicadoras")
        
        # Pergunta 4
        print("\n🔍 Pergunta 4: Crescimento do suporte Linux (2018-2022)")
        results['linux_growth'] = answer_question4(df)
        display_dataframe(results['linux_growth'], "Crescimento Linux")
        
        # Pergunta Extra
        print("\n🔍 Pergunta Extra: Relação preço × avaliações")
        results['price_analysis'] = answer_question_extra(df)
        display_dataframe(results['price_analysis'], "Análise Preço × Avaliações")
        
        # ============================================
        # PASSO 4: GERAR GRÁFICOS (AULA 09 - Visualizações)
        # ============================================
        if not args.skip_plots:
            print_section("PASSO 4: Gerando visualizações")
            
            print("\n📊 Gráfico 1: Percentual de jogos por SO")
            create_graph1_os_support(df)
            
            print("\n📊 Gráfico 2: Indie vs Estratégia (2010-2020)")
            create_graph2_indie_strategy(df)
            
            print("\n📊 Gráfico 3: Distribuição de preços")
            create_graph3_price_distribution(df)
        else:
            print_section("PASSO 4: Geração de gráficos pulada (--skip-plots)")
        
        # ============================================
        # PASSO 5: SALVAR RESULTADOS (AULA 10 - Exportação)
        # ============================================
        print_section("PASSO 5: Salvando resultados")
        
        print("\n💾 Salvando tabelas em CSV...")
        
        # AULA 10: to_csv() - Exporta DataFrame para CSV
        results['top10'].to_csv(
            os.path.join(TABLES_PATH, 'top10_games.csv'), 
            index=False, encoding='utf-8-sig'
        )
        results['rpg_stats'].to_csv(
            os.path.join(TABLES_PATH, 'rpg_stats.csv'), 
            index=False, encoding='utf-8-sig'
        )
        results['top_publishers'].to_csv(
            os.path.join(TABLES_PATH, 'top5_publishers.csv'), 
            index=False, encoding='utf-8-sig'
        )
        results['linux_growth'].to_csv(
            os.path.join(TABLES_PATH, 'linux_growth.csv'), 
            index=False, encoding='utf-8-sig'
        )
        results['price_analysis'].to_csv(
            os.path.join(TABLES_PATH, 'price_analysis.csv'), 
            index=False, encoding='utf-8-sig'
        )
        
        print("   ✅ Tabelas CSV salvas com sucesso!")
        print(f"   📁 Localização: {TABLES_PATH}")
        
        if not args.skip_plots:
            print(f"\n📊 Gráficos salvos em: {FIGURES_PATH}")
            print(f"   ├── grafico1_os_support.png")
            print(f"   ├── grafico2_indie_strategy.png")
            print(f"   └── grafico3_price_distribution.png")
        
        # ============================================
        # PASSO 6: LIMPEZA (opcional)
        # ============================================
        if args.clean:
            print_section("PASSO 6: Limpeza de arquivos temporários")
            cleanup_temp_files()
        
        # ============================================
        # RESUMO FINAL
        # ============================================
        elapsed_time = time.time() - start_time
        
        print_section("✅ ANÁLISE CONCLUÍDA COM SUCESSO!")
        print(f"\n⏱️  Tempo total de execução: {elapsed_time:.2f} segundos")
        
        print(f"\n📁 Resultados disponíveis em: {OUTPUT_PATH}")
        print(f"   ├── figures/     - {len(os.listdir(FIGURES_PATH)) if os.path.exists(FIGURES_PATH) else 0} gráficos")
        print(f"   └── tables/      - {len(os.listdir(TABLES_PATH))} tabelas CSV")
        
        print("\n📊 Resumo dos dados:")
        print(f"   ├── Total de jogos: {len(df):,}")
        print(f"   ├── Jogos pagos: {df['is_paid'].sum():,}")
        print(f"   ├── Jogos gratuitos: {(~df['is_paid']).sum():,}")
        
        # AULA 10: mean() - Média das notas
        if 'top10' in results and results['top10'] is not None:
            avg_score = results['top10']['metacritic_score'].mean()
            print(f"   └── Média das notas do Top 10: {avg_score:.1f}")
        
        print("\n🎉 Pronto! Agora você pode:")
        print("   1. Usar as tabelas CSV na pasta outputs/tables/")
        print("   2. Inserir os gráficos no seu relatório PDF")
        print("   3. Criar o relatório final conforme o template fornecido")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Execução interrompida pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro durante a execução: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()