"""
Módulo para pré-processamento dos dados
AULA 10: Limpeza e transformação de dados com Pandas
"""
import pandas as pd
import numpy as np
from .analysis import _print
from .config import COLUMN_MAPPING, PRICE_BINS, PRICE_LABELS

def rename_columns(df):
    """
    Renomeia colunas para snake_case com suporte a variações de case/espaços
    AULA 10: Renomeação de colunas com rename()
    """
    df_renamed = df.copy()
    current_cols = df_renamed.columns.tolist()
    existing_mapping = {}

    # Mapeamento robusto ignorando espaços e case
    for old_target, new_name in COLUMN_MAPPING.items():
        target_norm = old_target.strip().lower()
        for real_col in current_cols:
            if real_col.strip().lower() == target_norm:
                existing_mapping[real_col] = new_name
                break

    # AULA 10: rename() - Renomeia colunas
    df_renamed.rename(columns=existing_mapping, inplace=True)
    _print(f"✅ {len(existing_mapping)} colunas renomeadas")

    return df_renamed

def process_dates(df):
    """
    Processa datas de lançamento

    AULA 10: Accessor .dt para manipulação de datas
    pd.to_datetime() - Conversão para datetime
    """
    df_dates = df.copy()

    if 'release_date' not in df_dates.columns:
        _print("⚠️ Coluna 'release_date' não encontrada")
        return df_dates

    # AULA 10: to_datetime() - Converte string para datetime
    # format='%b %d, %Y' especifica o formato: Oct 21, 2008
    # errors='coerce' converte valores inválidos para NaT
    df_dates['release_date'] = pd.to_datetime(
        df_dates['release_date'],
        format='%b %d, %Y',
        errors='coerce'
    )

    # AULA 10: .dt accessor - Acessa propriedades de data
    # .dt.year - Extrai o ano da data
    df_dates['release_year'] = df_dates['release_date'].dt.year

    valid_dates = df_dates['release_date'].notna().sum()
    _print(f"✅ Datas processadas: {valid_dates:,} válidas")

    return df_dates

def process_media_assets(df):
    """
    Processa materiais de demonstração (screenshots e movies)

    AULA 10: apply() - Aplica funções a cada elemento
    AULA 07: NumPy - Operações vetorizadas
    """
    df_media = df.copy()

    # Initialize columns to 0 to avoid KeyError if original columns are missing
    df_media['n_screenshots'] = 0
    df_media['n_movies'] = 0

    # AULA 10: apply() com função lambda
    # lambda x: função anônima que processa cada valor
    # str(x).split(',') - Divide string pela vírgula
    if 'screenshots' in df_media.columns:
        df_media['n_screenshots'] = df_media['screenshots'].apply(
            lambda x: len(str(x).split(',')) if pd.notna(x) else 0
        )

    if 'movies' in df_media.columns:
        df_media['n_movies'] = df_media['movies'].apply(
            lambda x: len(str(x).split(',')) if pd.notna(x) else 0
        )

    # Criar coluna combinada
    df_media['demo_materials'] = df_media['n_screenshots'] + df_media['n_movies']

    # AULA 10: mean() - Média aritmética
    _print(f"✅ Materiais de demonstração processados")
    _print(f"   Média de screenshots: {df_media['n_screenshots'].mean():.1f}")
    _print(f"   Média de movies: {df_media['n_movies'].mean():.1f}")

    return df_media

def create_price_category(df):
    """
    Cria categorias de preço

    AULA 10: pd.cut() - Discretização de variáveis contínuas
    Criação de coluna booleana com operações vetorizadas
    """
    df_price = df.copy()

    if 'price' in df_price.columns:
        # Preencher inicialmente com 'Free'
        df_price['price_category'] = 'Free'
        df_price['is_paid'] = df_price['price'] > 0

        # Aplicar pd.cut apenas aos jogos pagos
        paid_mask = df_price['is_paid']
        if paid_mask.any():
            # AULA 10: pd.cut() categoriza valores numéricos
            categories = pd.cut(
                df_price.loc[paid_mask, 'price'],
                bins=PRICE_BINS,
                labels=PRICE_LABELS,
                right=False
            )
            # Converter para string para evitar problemas de compatibilidade entre pandas versions
            df_price.loc[paid_mask, 'price_category'] = categories.astype(str)

        _print(f"✅ Categorias de preço criadas")
        _print(f"   Jogos pagos: {df_price['is_paid'].sum():,}")
        _print(f"   Jogos gratuitos: {(~df_price['is_paid']).sum():,}")

    return df_price

def clean_numeric_columns(df):
    """
    Limpa e converte colunas numéricas removendo caracteres não numéricos
    e preenchendo NaNs com zero.

    AULA 07: NumPy - Uso de np.where para preenchimento condicional
    AULA 10: astype() - Conversão de tipo de dados
    """
    df_clean = df.copy()

    numeric_cols_to_clean = [
        'achievements', 'screenshots', 'movies', 'price',
        'positive', 'negative', 'dlc_count', 'metacritic_score'
    ]

    for col in numeric_cols_to_clean:
        if col in df_clean.columns:
            # Converte para string e remove caracteres não numéricos
            df_clean[col] = df_clean[col].astype(str).str.replace(r'[^0-9.]', '', regex=True)
            # Converte para numérico, tratando vírgulas como decimais se presentes
            df_clean[col] = pd.to_numeric(df_clean[col].str.replace(',', '.'), errors='coerce')
            # Preenche NaNs com 0 para colunas numéricas após a limpeza
            df_clean[col] = df_clean[col].fillna(0)

    _print("✅ Colunas numéricas limpas")

    return df_clean

def preprocess_all(df):
    """
    Executa todas as etapas de pré-processamento sequencialmente.
    """
    df = rename_columns(df)
    df = process_dates(df)
    df = clean_numeric_columns(df)
    df = process_media_assets(df)
    df = create_price_category(df)

    return df