import pytest
import os
import pandas as pd
from src.data_loader import load_data_from_zip, get_data_info, cleanup_temp_files
from src.config import DATA_PATH, TEMP_PATH

def test_data_loader_functions_exist():
    """Verifica se as funções essenciais estão definidas"""
    assert callable(load_data_from_zip)
    assert callable(get_data_info)
    assert callable(cleanup_temp_files)

def test_get_data_info_execution(sample_data):
    """Testa se get_data_info executa sem erros"""
    # Apenas verifica se não levanta exceção
    get_data_info(sample_data)

def test_cleanup_temp_files_creation():
    """Testa se clean_up_temp_files garante a existência da pasta"""
    cleanup_temp_files()
    assert os.path.exists(TEMP_PATH)