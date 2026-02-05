"""Testes para converter_colunas_int."""
import pytest
import pandas as pd
from src.processamento.limpeza.converter_colunas_int import converter_colunas_int


def test_converter_colunas_int():
    """Testa conversão de colunas para int."""
    df = pd.DataFrame({
        'col1': ['1', '2', '3'],
        'col2': ['10.0', '20.0', '30.0']
    })
    
    result = converter_colunas_int(df, ['col1', 'col2'])
    
    assert result['col1'].dtype == 'Int64'
    assert result['col2'].dtype == 'Int64'
    assert result['col1'].tolist() == [1, 2, 3]
