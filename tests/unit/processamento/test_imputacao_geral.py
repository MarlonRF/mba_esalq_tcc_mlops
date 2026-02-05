"""
Testes unitários para módulo de imputação de dados.
"""
import pandas as pd
import pytest
import numpy as np

from src.processamento.imputacao import (
    imputar_numericos,
    imputar_categoricos,
)


class TestImputarNumericos:
    """Testes para função imputar_numericos."""
    
    def test_imputacao_media(self):
        df = pd.DataFrame({'a': [1.0, np.nan, 3.0]})
        result = imputar_numericos(df, ['a'], metodo='mean')
        assert result['a'].isna().sum() == 0
        assert result['a'].iloc[1] == 2.0
        
    def test_imputacao_mediana(self):
        df = pd.DataFrame({'a': [1.0, np.nan, 3.0]})
        result = imputar_numericos(df, ['a'], metodo='median')
        assert result['a'].isna().sum() == 0
        assert result['a'].iloc[1] == 2.0
        
    def test_imputacao_constante(self):
        df = pd.DataFrame({'a': [1.0, np.nan, 3.0]})
        result = imputar_numericos(df, ['a'], metodo='constant', valor=999)
        assert result['a'].iloc[1] == 999


class TestImputarCategoricos:
    """Testes para função imputar_categoricos."""
    
    def test_imputacao_moda(self):
        df = pd.DataFrame({'a': ['x', np.nan, 'x', 'y']})
        result = imputar_categoricos(df, ['a'], metodo='most_frequent')
        assert result['a'].isna().sum() == 0
        assert result['a'].iloc[1] == 'x'
        
    def test_imputacao_constante(self):
        df = pd.DataFrame({'a': ['x', np.nan, 'y']})
        result = imputar_categoricos(df, ['a'], metodo='constant', valor='unknown')
        assert result['a'].iloc[1] == 'unknown'
