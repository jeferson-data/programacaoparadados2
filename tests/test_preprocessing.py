import pytest
import pandas as pd
import numpy as np
from src.preprocessing import (
    rename_columns, process_dates, clean_numeric_columns, 
    process_media_assets, create_price_category, preprocess_all
)

def test_rename_columns(sample_data):
    """Testa a renomeação de colunas"""
    # Criar DF com nomes antigos
    df_old = pd.DataFrame({
        'AppID': [1, 2],
        'Name': ['A', 'B'],
        'Release date': ['Jan 1, 2020', 'Feb 1, 2020']
    })
    result = rename_columns(df_old)
    assert 'app_id' in result.columns
    assert 'name' in result.columns
    assert 'release_date' in result.columns

def test_process_dates(sample_data):
    """Testa o processamento de datas"""
    result = process_dates(sample_data)
    assert 'release_year' in result.columns
    assert result['release_year'].iloc[0] == 2020

def test_clean_numeric_columns():
    """Testa a limpeza de colunas numéricas"""
    df = pd.DataFrame({
        'price': ['$29.99', '19.99', 'free'],
        'positive': ['1,500', '200', '0']
    })
    result = clean_numeric_columns(df)
    assert result['price'].iloc[0] == 29.99
    assert result['price'].iloc[2] == 0
    assert result['positive'].iloc[0] == 1500

def test_process_media_assets(sample_data):
    """Testa o processamento de screenshots e movies"""
    result = process_media_assets(sample_data)
    assert 'n_screenshots' in result.columns
    assert 'demo_materials' in result.columns
    assert result['n_screenshots'].iloc[0] == 3

def test_create_price_category(sample_data):
    """Testa a criação de categorias de preço"""
    result = create_price_category(sample_data)
    assert 'price_category' in result.columns
    assert 'is_paid' in result.columns
    assert result['is_paid'].iloc[1] == False # Game2 price is 0

def test_preprocess_all(sample_data):
    """Testa o fluxo completo de pré-processamento"""
    # Simular colunas originais
    df_raw = pd.DataFrame({
        'AppID': [1],
        'Name': ['Game'],
        'Release date': ['Oct 21, 2008'],
        'Price': [19.99],
        'Screenshots': ['url1,url2'],
        'Movies': ['url1'],
        'Windows': [True],
        'Mac': [False],
        'Linux': [False]
    })
    result = preprocess_all(df_raw)
    assert 'release_year' in result.columns
    assert 'price_category' in result.columns
    assert 'demo_materials' in result.columns
    assert result['release_year'].iloc[0] == 2008