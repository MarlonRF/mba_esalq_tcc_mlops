"""
Testes unitários para módulo de limpeza de dados.
"""
import pandas as pd
import pytest
import numpy as np

from src.processamento.limpeza import (
    aplicar_substituicoes,
    converter_colunas_categoricas,
    converter_colunas_float,
    converter_colunas_int,
)


class TestAplicarSubstituicoes:
    """Testes para função aplicar_substituicoes."""
    
    def test_substitui_valores_simples(self):
        df = pd.DataFrame({'a': [1, 99, 3]})
        result = aplicar_substituicoes(df, {99: 0})
        assert result['a'].tolist() == [1, 0, 3]
        
    def test_substitui_multiplos_valores(self):
        df = pd.DataFrame({'a': [1, 99, 'x']})
        result = aplicar_substituicoes(df, {99: 0, 'x': 'y'})
        assert result['a'].tolist() == [1, 0, 'y']
    
    def test_nao_modifica_sem_substituicoes(self):
        df = pd.DataFrame({'a': [1, 2, 3]})
        result = aplicar_substituicoes(df, {99: 0})
        assert result['a'].tolist() == [1, 2, 3]


class TestConverterColunasCategoricas:
    """Testes para função converter_colunas_categoricas."""
    
    def test_converte_para_string(self):
        df = pd.DataFrame({'a': [1, 2, 3]})
        result = converter_colunas_categoricas(df, ['a'])
        assert result['a'].dtype == 'object' or result['a'].dtype == 'string'
        
    def test_converte_multiplas_colunas(self):
        df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
        result = converter_colunas_categoricas(df, ['a', 'b'])
        assert result['a'].dtype == 'object' or result['a'].dtype == 'string'
        assert result['b'].dtype == 'object' or result['b'].dtype == 'string'
    
    def test_ignora_coluna_inexistente(self):
        df = pd.DataFrame({'a': [1, 2]})
        result = converter_colunas_categoricas(df, ['a', 'b'])
        assert 'b' not in result.columns


class TestConverterColunasFloat:
    """Testes para função converter_colunas_float."""
    
    def test_converte_para_float(self):
        df = pd.DataFrame({'a': ['1.5', '2.5', '3.5']})
        result = converter_colunas_float(df, ['a'])
        assert result['a'].dtype == 'float64'
        
    def test_converte_com_valores_nulos(self):
        df = pd.DataFrame({'a': ['1.5', np.nan, '3.5']})
        result = converter_colunas_float(df, ['a'])
        assert result['a'].dtype == 'float64'
        assert pd.isna(result['a'].iloc[1])


class TestConverterColunasInt:
    """Testes para função converter_colunas_int."""
    
    def test_converte_para_int(self):
        df = pd.DataFrame({'a': [1.0, 2.0, 3.0]})
        result = converter_colunas_int(df, ['a'])
        assert result['a'].dtype in ['int64', 'Int64']
        
    def test_converte_com_valores_nulos(self):
        df = pd.DataFrame({'a': [1.0, np.nan, 3.0]})
        result = converter_colunas_int(df, ['a'])
        assert result['a'].dtype == 'Int64'
        assert pd.isna(result['a'].iloc[1])
