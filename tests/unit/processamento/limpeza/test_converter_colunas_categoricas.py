"""Testes para converter_colunas_categoricas."""
import pytest
import pandas as pd
from src.processamento.limpeza.converter_colunas_categoricas import converter_colunas_categoricas


def test_converter_colunas_categoricas():
    """Testa conversão de colunas para categorical/string."""
    df = pd.DataFrame({
        'sexo': ['m', 'f', 'm'],
        'categoria': [1, 2, 1]
    })
    
    result = converter_colunas_categoricas(df, ['sexo', 'categoria'])
    
    assert result['sexo'].dtype == 'string'
    assert result['categoria'].dtype == 'string'
