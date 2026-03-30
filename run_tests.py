import pytest
import sys
import os

# Fix para Windows: força UTF-8 no stdout para suportar emojis
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def run_all_tests():
    """Executa todos os testes do projeto usando pytest"""
    print("\n" + "="*60)
    print("🚀 INICIANDO TESTES AUTOMATIZADOS")
    print("="*60)
    
    # Adicionar diretório atual ao path para garantir que src seja encontrado
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Argumentos base do pytest
    args = ['-v', 'tests/']
    
    # Verificar se o plugin pytest-cov está instalado antes de adicionar argumentos de cobertura
    try:
        import pytest_cov
        args.extend(['--cov=src', '--cov-report=term-missing'])
    except ImportError:
        print("⚠️  Aviso: 'pytest-cov' não encontrado. Executando testes sem relatório de cobertura.")
    
    # Executa o pytest e retorna o código de saída
    return pytest.main(args)

if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)