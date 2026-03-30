import pytest
import pandas as pd
from src.analysis import (
    answer_question1, answer_question2, answer_question3, 
    answer_question4, set_silent_mode
)

@pytest.fixture
def test_df():
    """Cria um DF simples para testes de análise"""
    data = {
        'app_id': [1, 2, 3],
        'name': ['Game1', 'Game2', 'Game3'],
        'release_date': ['Oct 21, 2020', 'Jan 1, 2021', 'Feb 1, 2022'],
        'release_year': [2020, 2021, 2022],
        'windows': [True, True, False],
        'mac': [True, False, False],
        'linux': [False, False, False],
        'genres': ['Action,Indie,RPG', 'Strategy,Indie', 'Action'],
        'publishers': ['Pub1', 'Pub2', 'Pub1'],
        'price': [10.0, 0.0, 20.0],
        'is_paid': [True, False, True],
        'price_category': ['USD 5-10', 'Free', 'USD 10-20'],
        'positive': [1500, 200, 5000],
        'metacritic_score': [80, 0, 90]
    }
    return pd.DataFrame(data)

def test_answer_question1_top10(test_df):
    """Testa se retorna o top 10 (ou menos) por score"""
    set_silent_mode(True)
    result = answer_question1(test_df)
    # Entre Game1 (80) e Game3 (90), o Game3 deve vir primeiro
    assert result.iloc[0]['name'] == 'Game3'
    assert result.iloc[0]['metacritic_score'] == 90

def test_answer_question2_rpg(test_df):
    """Testa estatísticas de RPG"""
    result = answer_question2(test_df)
    # Apenas Game1 é RPG
    assert result.iloc[0]['total_rpg'] == 1
    assert result.iloc[0]['windows_support'] == 100.0

def test_answer_question3_publishers(test_df):
    """Testa as top publicadoras de jogos pagos"""
    result = answer_question3(test_df)
    # Jogos pagos: Game1 (Pub1) e Game3 (Pub1). Pub1 tem 2 jogos.
    assert result.iloc[0]['main_publisher'] == 'Pub1'
    assert result.iloc[0]['game_count'] == 2

def test_answer_question4_linux(test_df):
    """Testa suporte Linux por ano"""
    result = answer_question4(test_df)
    # Suporte Linux: 2020 (0%), 2021 (0%), 2022 (0%)
    # No caso do test_df, todos windows/mac/linux são False para Linux
    assert result[result['release_year'] == 2020]['linux_support_pct'].iloc[0] == 0.0