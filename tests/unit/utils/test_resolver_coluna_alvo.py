"""
Testes unitários para resolver_coluna_alvo.py
"""
import pytest
import pandas as pd
from src.utils.resolver_coluna_alvo import resolver_coluna_alvo


@pytest.fixture
def df_exemplo():
    """DataFrame de exemplo para testes."""
    return pd.DataFrame({
        'feature1': [1, 2, 3],
        'feature2': [4, 5, 6],
        'Target': [0, 1, 0]
    })


def test_resolver_coluna_alvo_correspondencia_exata(df_exemplo):
    """Testa resolução com correspondência exata do nome."""
    resultado = resolver_coluna_alvo(df_exemplo, 'Target')
    
    assert resultado == 'Target'


def test_resolver_coluna_alvo_case_insensitive(df_exemplo):
    """Testa resolução insensível a maiúsculas/minúsculas."""
    resultado = resolver_coluna_alvo(df_exemplo, 'target')
    
    assert resultado == 'Target'


def test_resolver_coluna_alvo_uppercase(df_exemplo):
    """Testa resolução com nome em maiúsculas."""
    resultado = resolver_coluna_alvo(df_exemplo, 'TARGET')
    
    assert resultado == 'Target'


def test_resolver_coluna_alvo_nao_encontrada(df_exemplo):
    """Testa que retorna None quando coluna não existe."""
    resultado = resolver_coluna_alvo(df_exemplo, 'coluna_inexistente')
    
    assert resultado is None


def test_resolver_coluna_alvo_com_underscores():
    """Testa resolução com diferentes separadores."""
    df = pd.DataFrame({
        'feature_1': [1, 2],
        'target_variable': [0, 1]
    })
    
    # Testa com hífen (deve encontrar com underscore)
    resultado = resolver_coluna_alvo(df, 'target-variable')
    
    assert resultado == 'target_variable'


def test_resolver_coluna_alvo_com_hifens():
    """Testa resolução de coluna com hífen quando configurado com underscore."""
    df = pd.DataFrame({
        'feature-1': [1, 2],
        'target-variable': [0, 1]
    })
    
    resultado = resolver_coluna_alvo(df, 'target_variable')
    
    assert resultado == 'target-variable'


def test_resolver_coluna_alvo_string_vazia():
    """Testa comportamento com string vazia."""
    df = pd.DataFrame({'col1': [1, 2]})
    
    resultado = resolver_coluna_alvo(df, '')
    
    assert resultado is None


def test_resolver_coluna_alvo_multiplas_colunas_similares():
    """Testa que retorna a correspondência mais próxima."""
    df = pd.DataFrame({
        'target': [1, 2],
        'Target': [3, 4],
        'TARGET': [5, 6]
    })
    
    # Deve encontrar exatamente 'target'
    resultado = resolver_coluna_alvo(df, 'target')
    assert resultado == 'target'
    
    # Deve encontrar exatamente 'Target'
    resultado = resolver_coluna_alvo(df, 'Target')
    assert resultado == 'Target'
