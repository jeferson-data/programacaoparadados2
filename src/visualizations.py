import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

from src.config import FIGURES_PATH, apply_custom_style

def create_os_support_percentage_plot(df: pd.DataFrame, output_path: str = FIGURES_PATH):
    """
    Gera um gráfico de barras mostrando o percentual de jogos com suporte
    para cada sistema operacional (Windows, Mac, Linux).
    """
    apply_custom_style()

    # Calcula o percentual de jogos para cada SO
    total_games = len(df)
    windows_support = (df['windows'].sum() / total_games) * 100
    mac_support = (df['mac'].sum() / total_games) * 100
    linux_support = (df['linux'].sum() / total_games) * 100

    os_data = pd.DataFrame({
        'OS': ['Windows', 'Mac', 'Linux'],
        'Percentage': [windows_support, mac_support, linux_support]
    })

    plt.figure(figsize=(10, 6))
    sns.barplot(x='OS', y='Percentage', data=os_data, palette='viridis')
    plt.title('Percentual de Jogos com Suporte para Cada Sistema Operacional')
    plt.xlabel('Sistema Operacional')
    plt.ylabel('Percentual de Jogos (%)')
    plt.ylim(0, 100) # Garante que o eixo Y vá de 0 a 100
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, 'grafico1_os_support_percentage.png'))
    plt.close()
    print(f"✅ Gráfico 'grafico1_os_support_percentage.png' salvo em {output_path}")

def create_indie_strategy_single_player_plot(df: pd.DataFrame, output_path: str = FIGURES_PATH):
    """
    Gera um gráfico de linha mostrando o número total de jogos single-player
    do gênero Indie e Estratégia lançados por ano entre 2010 e 2020.
    """
    apply_custom_style()

    # Filtrar jogos para os gêneros 'Indie' e 'Strategy' (case-insensitive) e 'Single-player'
    # Assumindo que 'Categories' contém 'Single-player' e 'Genres' contém 'Indie' ou 'Strategy'
    filtered_games = df[
        df['release_year'].between(2010, 2020) &
        df['genres'].str.contains('Indie|Strategy', na=False, case=False) &
        df['categories'].str.contains('Single-player', na=False, case=False)
    ].copy()

    # Contar jogos por ano
    games_by_year = filtered_games.groupby('release_year').size().reset_index(name='total_games')

    plt.figure(figsize=(12, 7))
    sns.lineplot(x='release_year', y='total_games', data=games_by_year, marker='o', color='purple')
    plt.title('Número de Jogos Single-player Indie e Estratégia por Ano (2010-2020)')
    plt.xlabel('Ano de Lançamento')
    plt.ylabel('Número Total de Jogos')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(games_by_year['release_year'].unique(), rotation=45) # Garante que todos os anos sejam exibidos
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, 'grafico2_indie_strategy_single_player_yearly.png'))
    plt.close()
    print(f"✅ Gráfico 'grafico2_indie_strategy_single_player_yearly.png' salvo em {output_path}")

def create_metacritic_score_distribution_plot(df: pd.DataFrame, output_path: str = FIGURES_PATH):
    """
    Gera um histograma da distribuição dos Metacritic scores.
    """
    apply_custom_style()

    # Filtrar jogos com Metacritic score > 0 para análise relevante
    rated_games = df[df['metacritic_score'] > 0]

    plt.figure(figsize=(12, 7))
    sns.histplot(rated_games['metacritic_score'], bins=20, kde=True, color='teal')
    plt.title('Distribuição dos Metacritic Scores')
    plt.xlabel('Metacritic Score')
    plt.ylabel('Número de Jogos')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, 'grafico3_metacritic_score_distribution.png'))
    plt.close()
    print(f"✅ Gráfico 'grafico3_metacritic_score_distribution.png' salvo em {output_path}")
