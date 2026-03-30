"""
Configuração dos testes automatizados
AULA 10: Testes com pytest
"""
import pytest
import pandas as pd
import numpy as np
import os
import sys

# Adicionar diretório pai ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analysis import set_silent_mode
from src.preprocessing import preprocess_all
from src.data_loader import load_data_from_zip


# Configurar modo silencioso para todos os testes
set_silent_mode(True)


@pytest.fixture
def sample_data():
    """Cria um pequeno conjunto de dados de amostra para testes"""
    data = {
        'name': ['Game1', 'Game2', 'Game3', 'Game4', 'Game5'],
        'release_date': ['Jan 15, 2020', 'Feb 20, 2021', 'Mar 10, 2019', 
                         'Apr 05, 2022', 'May 30, 2018'],
        'price': [29.99, 0, 59.99, 19.99, 9.99],
        'metacritic_score': [85, 0, 92, 78, 88],
        'positive': [1500, 0, 5000, 800, 2000],
        'negative': [150, 0, 300, 100, 150],
        'dlc_count': [3, 0, 5, 1, 2],
        'windows': [True, True, True, True, True],
        'mac': [True, False, True, False, True],
        'linux': [False, False, True, False, True],
        'genres': ['Action,RPG', 'Indie', 'RPG,Strategy', 'Action', 'Indie,RPG'],
        'categories': ['Single-player', 'Multi-player', 'Single-player', 
                       'Single-player', 'Single-player'],
        'publishers': ['PublisherA', 'PublisherB', 'PublisherA,PublisherC', 
                       'PublisherB', 'PublisherA'],
        'screenshots': ['url1,url2,url3', '', 'url1,url2', 'url1', 'url1,url2,url3,url4'],
        'movies': ['', '', 'url1', '', 'url1,url2']
    }
    
    df = pd.DataFrame(data)
    return df


@pytest.fixture
def processed_sample(sample_data):
    """Aplica pré-processamento na amostra de dados"""
    df = sample_data.copy()
    
    # Processar datas
    df['release_date'] = pd.to_datetime(df['release_date'], format='%b %d, %Y', errors='coerce')
    df['release_year'] = df['release_date'].dt.year
    
    # Processar materiais de demonstração
    df['n_screenshots'] = df['screenshots'].apply(
        lambda x: len(str(x).split(',')) if pd.notna(x) and x != '' else 0
    )
    df['n_movies'] = df['movies'].apply(
        lambda x: len(str(x).split(',')) if pd.notna(x) and x != '' else 0
    )
    df['demo_materials'] = df['n_screenshots'] + df['n_movies']
    
    # Categorias de preço
    df['is_paid'] = df['price'] > 0
    df['price_category'] = 'Free'
    
    paid_mask = df['is_paid']
    if paid_mask.any():
        bins = [0.01, 5, 10, 20, 30, 60, float('inf')]
        labels = ['USD 0-5', 'USD 5-10', 'USD 10-20', 'USD 20-30', 'USD 30-60', 'USD 60+']
        df.loc[paid_mask, 'price_category'] = pd.cut(
            df.loc[paid_mask, 'price'],
            bins=bins,
            labels=labels,
            right=False
        ).astype(str)
    
    return df


@pytest.fixture
def real_data_sample():
    """Carrega uma amostra real dos dados (primeiras 1000 linhas)"""
    try:
        df = load_data_from_zip()
        return df.head(1000)
    except:
        return None