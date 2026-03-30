"""
Steam Games Analysis Package
Análise de dados de jogos da Steam - Projeto Final Fase 2
"""

__version__ = '1.0.0'
__author__ = 'Aluno'
__description__ = 'Análise exploratória de dados de jogos da Steam'

# Exportar principais funções
from .config import *
from .data_loader import *
from .preprocessing import *
from .analysis import *
from .visualizations import *

# Informações do pacote
__all__ = [
    # Config
    'apply_custom_style', 'DARK_BG', 'ACCENT1', 'ACCENT2', 'ACCENT3',
    
    # Data Loader
    'load_data_from_zip', 'load_data_in_chunks', 'get_data_info', 'cleanup_temp_files',
    
    # Preprocessing
    'preprocess_all', 'rename_columns', 'process_dates', 'create_price_category',
    
    # Analysis
    'answer_question1', 'answer_question2', 'answer_question3',
    'answer_question4', 'answer_question_extra',
    
    # Visualizations
    'create_graph1_os_support', 'create_graph2_indie_strategy',
    'create_graph3_price_distribution'
]