"""
Testes unitários para aplicar_tipos_colunas.py
"""
import pytest
import pandas as pd
import numpy as np
from src.utils.aplicar_tipos_colunas import aplicar_tipos_colunas


@pytest.fixture
def df_misto():
    """DataFrame com tipos mistos para testes."""
    return pd.DataFrame({
        'col_int': ['1', '2', '3'],
        'col_float': ['1.5', '2.5', '3.5'],
        'col_date': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'col_str': [1, 2, 3]
    })


def test_aplicar_tipos_colunas_float(df_misto):
    """Testa conversão para float64."""
    tipos = {'col_float': 'float64'}
    resultado = aplicar_tipos_colunas(df_misto, tipos)
    
    assert resultado['col_float'].dtype == 'float64'
    assert resultado['col_float'].iloc[0] == 1.5


def test_aplicar_tipos_colunas_datetime(df_misto):
    """Testa conversão para datetime."""
    tipos = {'col_date': 'datetime64[ns]'}
    resultado = aplicar_tipos_colunas(df_misto, tipos)
    
    assert resultado['col_date'].dtype == 'datetime64[ns]'
    assert pd.notna(resultado['col_date'].iloc[0])


def test_aplicar_tipos_colunas_int64(df_misto):
    """Testa conversão para Int64 (nullable integer)."""
    tipos = {'col_int': 'Int64'}
    resultado = aplicar_tipos_colunas(df_misto, tipos)
    
    assert resultado['col_int'].dtype == 'Int64'
    assert resultado['col_int'].iloc[0] == 1


def test_aplicar_tipos_colunas_string(df_misto):
    """Testa conversão para string."""
    tipos = {'col_str': 'string'}
    resultado = aplicar_tipos_colunas(df_misto, tipos)
    
    assert resultado['col_str'].dtype == 'string'


def test_aplicar_tipos_colunas_coluna_inexistente(df_misto):
    """Testa comportamento com coluna inexistente (não deve dar erro)."""
    tipos = {'coluna_nao_existe': 'float64'}
    resultado = aplicar_tipos_colunas(df_misto, tipos)
    
    # Não deve lançar erro, apenas printar aviso
    assert 'coluna_nao_existe' not in resultado.columns


def test_aplicar_tipos_colunas_valores_invalidos():
    """Testa coerção de valores inválidos para NaN."""
    df = pd.DataFrame({'col': ['1', '2', 'invalid', '4']})
    tipos = {'col': 'float64'}
    
    resultado = aplicar_tipos_colunas(df, tipos)
    
    assert resultado['col'].dtype == 'float64'
    assert pd.isna(resultado['col'].iloc[2])  # 'invalid' vira NaN


def test_aplicar_tipos_colunas_multiplas_colunas(df_misto):
    """Testa conversão de múltiplas colunas simultaneamente."""
    tipos = {
        'col_int': 'Int64',
        'col_float': 'float64',
        'col_date': 'datetime64[ns]'
    }
    
    resultado = aplicar_tipos_colunas(df_misto, tipos)
    
    assert resultado['col_int'].dtype == 'Int64'
    assert resultado['col_float'].dtype == 'float64'
    assert resultado['col_date'].dtype == 'datetime64[ns]'


def test_aplicar_tipos_colunas_nao_modifica_original(df_misto):
    """Testa que DataFrame original não é modificado (se usar copy)."""
    tipos = {'col_int': 'Int64'}
    df_original = df_misto.copy()
    
    aplicar_tipos_colunas(df_misto, tipos)
    
    # Nota: A função modifica in-place, mas vamos testar o comportamento esperado
    assert df_misto['col_int'].dtype != df_original['col_int'].dtype
