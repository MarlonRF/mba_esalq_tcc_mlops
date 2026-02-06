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
        df = pd.DataFrame({'a': [1, 99, -999]})
        result = aplicar_substituicoes(df, {99: 0, -999: 0})
        assert result['a'].tolist() == [1, 0, 0]


class TestConverterColunasFloat:
    """Testes para função converter_colunas_float."""
    
    def test_converte_string_para_float(self):
        df = pd.DataFrame({'a': ['1.5', '2.5', '3.5']})
        result = converter_colunas_float(df, ['a'])
        assert result['a'].dtype == 'float64'
        assert result['a'].tolist() == [1.5, 2.5, 3.5]
        
    def test_mantém_valores_numericos(self):
        df = pd.DataFrame({'a': [1.5, 2.5, 3.5]})
        result = converter_colunas_float(df, ['a'])
        assert result['a'].dtype == 'float64'


class TestConverterColunasInt:
    """Testes para função converter_colunas_int."""
    
    def test_converte_string_para_int(self):
        df = pd.DataFrame({'a': ['1', '2', '3']})
        result = converter_colunas_int(df, ['a'])
        assert pd.api.types.is_integer_dtype(result['a'])
        
    def test_converte_float_para_int(self):
        df = pd.DataFrame({'a': [1.0, 2.0, 3.0]})
        result = converter_colunas_int(df, ['a'])
        assert pd.api.types.is_integer_dtype(result['a'])


class TestConverterColunasCategoricas:
    """Testes para função converter_colunas_categoricas."""
    
    def test_converte_para_string(self):
        df = pd.DataFrame({'sexo': ['m', 'f', 'm']})
        result = converter_colunas_categoricas(df, ['sexo'])
        assert result['sexo'].dtype == 'string' or result['sexo'].dtype == 'object'
        
    def test_preserva_valores(self):
        df = pd.DataFrame({'sexo': ['m', 'f', 'm']})
        result = converter_colunas_categoricas(df, ['sexo'])
        assert result['sexo'].tolist() == ['m', 'f', 'm']
