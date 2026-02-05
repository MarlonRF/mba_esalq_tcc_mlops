"""
Testes unitários para aplicar_dummy.py
"""
import pytest
import pandas as pd
from src.features.codificacao.aplicar_dummy import aplicar_dummy_encoding


@pytest.fixture
def df_categorico():
    """DataFrame com variáveis categóricas para testes."""
    return pd.DataFrame({
        'cor': ['azul', 'vermelho', 'azul', 'verde', 'vermelho'],
        'tamanho': ['P', 'M', 'G', 'P', 'M'],
        'valor': [10, 20, 15, 25, 30]
    })


def test_aplicar_dummy_basico(df_categorico):
    """Testa aplicação básica de dummy encoding."""
    resultado = aplicar_dummy_encoding(
        df=df_categorico,
        colunas=['cor']
    )
    
    # Verifica que novas colunas foram criadas
    assert 'cor_azul' in resultado.columns or 'cor_vermelho' in resultado.columns
    assert 'valor' in resultado.columns  # Mantém colunas não categóricas


def test_aplicar_dummy_multiplas_colunas(df_categorico):
    """Testa dummy encoding em múltiplas colunas."""
    resultado = aplicar_dummy_encoding(
        df=df_categorico,
        colunas=['cor', 'tamanho']
    )
    
    # Verifica que colunas foram expandidas
    assert len(resultado.columns) > len(df_categorico.columns)


def test_aplicar_dummy_drop_first(df_categorico):
    """Testa opção drop_first=True."""
    resultado = aplicar_dummy_encoding(
        df=df_categorico,
        colunas=['cor'],
        drop_first=True
    )
    
    # Com drop_first, deve ter n-1 colunas por categoria
    colunas_cor = [c for c in resultado.columns if c.startswith('cor_')]
    assert len(colunas_cor) == 2  # 3 cores - 1 = 2


def test_aplicar_dummy_valores_binarios(df_categorico):
    """Testa que valores das dummies são 0 ou 1."""
    resultado = aplicar_dummy_encoding(
        df=df_categorico,
        colunas=['cor']
    )
    
    colunas_dummy = [c for c in resultado.columns if c.startswith('cor_')]
    for col in colunas_dummy:
        assert resultado[col].isin([0, 1]).all()
