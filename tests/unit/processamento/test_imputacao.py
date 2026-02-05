"""
Testes unitários para módulo de imputação de dados.
"""
import pandas as pd
import pytest
import numpy as np

from src.processamento.imputacao import (
    imputar_numericos,
    imputar_categoricos,
    imputar_por_coluna,
    imputar_media_movel_interpolada,
)


class TestImputarNumericos:
    """Testes para função imputar_numericos."""
    
    def test_imputa_com_media(self):
        df = pd.DataFrame({'a': [1.0, np.nan, 3.0]})
        result = imputar_numericos(df, ['a'], metodo='mean')
        assert not pd.isna(result['a'].iloc[1])
        assert result['a'].iloc[1] == 2.0
    
    def test_imputa_com_mediana(self):
        df = pd.DataFrame({'a': [1.0, np.nan, 5.0]})
        result = imputar_numericos(df, ['a'], metodo='median')
        assert not pd.isna(result['a'].iloc[1])
        assert result['a'].iloc[1] == 3.0
    
    def test_imputa_com_constante(self):
        df = pd.DataFrame({'a': [1.0, np.nan, 3.0]})
        result = imputar_numericos(df, ['a'], metodo='constant', valor_constante=99)
        assert result['a'].iloc[1] == 99


class TestImputarCategoricos:
    """Testes para função imputar_categoricos."""
    
    def test_imputa_com_moda(self):
        df = pd.DataFrame({'a': ['x', np.nan, 'x', 'y']})
        result = imputar_categoricos(df, ['a'], metodo='most_frequent')
        assert not pd.isna(result['a'].iloc[1])
        assert result['a'].iloc[1] == 'x'
    
    def test_imputa_com_constante(self):
        df = pd.DataFrame({'a': ['x', np.nan, 'y']})
        result = imputar_categoricos(df, ['a'], metodo='constant', valor_constante='z')
        assert result['a'].iloc[1] == 'z'


class TestImputarPorColuna:
    """Testes para função imputar_por_coluna."""
    
    def test_imputa_diferentes_metodos(self):
        df = pd.DataFrame({
            'num': [1.0, np.nan, 3.0],
            'cat': ['a', np.nan, 'a']
        })
        config = {
            'num': {'metodo': 'mean'},
            'cat': {'metodo': 'most_frequent'}
        }
        result = imputar_por_coluna(df, config)
        assert not pd.isna(result['num'].iloc[1])
        assert not pd.isna(result['cat'].iloc[1])
        assert result['num'].iloc[1] == 2.0
        assert result['cat'].iloc[1] == 'a'


class TestImputarMediaMovelInterpolada:
    """Testes para função imputar_media_movel_interpolada."""
    
    def test_imputa_com_janela(self):
        df = pd.DataFrame({'a': [1.0, np.nan, 3.0, 4.0]})
        result = imputar_media_movel_interpolada(df, ['a'], janela=2)
        assert not pd.isna(result['a'].iloc[1])
    
    def test_preserva_valores_existentes(self):
        df = pd.DataFrame({'a': [1.0, 2.0, 3.0]})
        result = imputar_media_movel_interpolada(df, ['a'], janela=2)
        assert result['a'].tolist() == [1.0, 2.0, 3.0]
