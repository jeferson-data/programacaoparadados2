#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script focado na geração das visualizações de dados (gráficos) do projeto.
Carrega os dados, pré-processa e salva as figuras definidas no módulo de visualizações.
"""

import os
from src.data_loader import load_data_from_zip
from src.preprocessing import preprocess_all
from src.visualizations import (
    create_graph1_os_support, 
    create_graph2_indie_strategy,
    create_graph3_price_distribution
)
from src.config import FIGURES_PATH

def main():
    print("="*60)
    print("🎨 GERADOR DE VISUALIZAÇÕES E GRÁFICOS")
    print("="*60)
    print("\n⏳ Carregando os dados do projeto...")
    df_raw = load_data_from_zip()
    
    print("🧹 Realizando o pré-processamento dos dados...")
    df = preprocess_all(df_raw)
    
    # Garante que a pasta de gráficos exista
    os.makedirs(FIGURES_PATH, exist_ok=True)
    
    print(f"\n📊 Gerando gráficos e salvando em: {FIGURES_PATH}")
    
    print("   [1/3] Criando Gráfico 1: Suporte por Sistema Operacional...")
    create_graph1_os_support(df, show=True)
    
    print("   [2/3] Criando Gráfico 2: Evolução Indie vs Estratégia...")
    create_graph2_indie_strategy(df, show=True)
    
    print("   [3/3] Criando Gráfico 3: Distribuição de Preços...")
    create_graph3_price_distribution(df, show=True)
    
    print("\n✅ Sucesso! Todos os gráficos foram criados.")
    print(f"📁 Confira os arquivos na pasta: {FIGURES_PATH}")

if __name__ == "__main__":
    main()