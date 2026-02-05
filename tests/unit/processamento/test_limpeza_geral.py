"""
Testes unitários para módulo de limpeza de dados.
"""
import pandas as pd
import pytest
import numpy as np

from src.processamento.limpeza import (
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    aplicar_substituicoes,
    converter_colunas_float,
    converter_colunas_int,
    converter_colunas_categoricas,
)


class TestAplicarSubstituicoes:
    """Testes para função aplicar_substituicoes."""
    
    def test_substitui_valores_simples(self):
        df = pd.DataFrame({'a': [1, 99, 3]})
        result = aplicar_substituicoes(df, {99: 0})
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    remover_duplicatas,
    remover_linhas_vazias,
    substituir_valores,
    converter_tipos,
)


class TestRemoverDuplicatas:
    """Testes para função remover_duplicatas."""
    
    def test_remove_duplicatas_completas(self):
        df = pd.DataFrame({
            'a': [1, 1, 2],
            'b': ['x', 'x', 'y']
        })
        result = remover_duplicatas(df)
        assert len(result) == 2
        
    def test_remove_duplicatas_subset(self):
        df = pd.DataFrame({
            'a': [1, 1, 2],
            'b': ['x', 'y', 'y']
        })
        result = remover_duplicatas(df, subset=['a'])
        assert len(result) == 2


class TestRemoverLinhasVazias:
    """Testes para função remover_linhas_vazias."""
    
    def test_remove_linhas_totalmente_vazias(self):
        df = pd.DataFrame({
            'a': [1, np.nan, 3],
            'b': ['x', np.nan, 'z']
        })
        result = remover_linhas_vazias(df)
        assert len(result) == 2
        
    def test_nao_remove_linhas_parcialmente_vazias(self):
        df = pd.DataFrame({
            'a': [1, np.nan, 3],
            'b': ['x', 'y', 'z']
        })
        result = remover_linhas_vazias(df)
        assert len(result) == 3


class TestSubstituirValores:
    """Testes para função substituir_valores."""
    
    def test_substitui_valores_simples(self):
        df = pd.DataFrame({'a': [1, 99, 3]})
        result = substituir_valores(df, {99: 0})
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
        assert result['a'].tolist() == [1, 0, 3]
        
    def test_substitui_multiplos_valores(self):
        df = pd.DataFrame({'a': [1, 99, 'x']})
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        result = aplicar_substituicoes(df, {99: 0, 'x': 'y'})
        assert result['a'].tolist() == [1, 0, 'y']
        
    def test_preserva_valores_nao_mapeados(self):
        df = pd.DataFrame({'a': [1, 2, 3]})
        result = aplicar_substituicoes(df, {99: 0})
        assert result['a'].tolist() == [1, 2, 3]


class TestConverterColunasFloat:
    """Testes para função converter_colunas_float."""
    
    def test_converte_string_para_float(self):
        df = pd.DataFrame({'a': ['1.5', '2.5', '3.5']})
        result = converter_colunas_float(df, ['a'])
        assert result['a'].dtype == 'float64'
        assert result['a'].tolist() == [1.5, 2.5, 3.5]
        
    def test_trata_valores_invalidos(self):
        df = pd.DataFrame({'a': ['1.5', 'invalid', '3.5']})
        result = converter_colunas_float(df, ['a'])
        assert pd.isna(result['a'].iloc[1])


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
        assert result['sexo'].dtype == 'string'
        
    def test_preserva_valores(self):
        df = pd.DataFrame({'sexo': ['m', 'f', 'm']})
        result = converter_colunas_categoricas(df, ['sexo'])
        assert result['sexo'].tolist() == ['m', 'f', 'm']
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
        result = substituir_valores(df, {99: 0, 'x': 'y'})
        assert result['a'].tolist() == [1, 0, 'y']


class TestConverterTipos:
    """Testes para função converter_tipos."""
    
    def test_converte_para_int(self):
        df = pd.DataFrame({'a': ['1', '2', '3']})
        result = converter_tipos(df, {'a': 'int64'})
        assert result['a'].dtype == 'int64'
        
    def test_converte_para_float(self):
        df = pd.DataFrame({'a': ['1.5', '2.5', '3.5']})
        result = converter_tipos(df, {'a': 'float64'})
        assert result['a'].dtype == 'float64'
        
    def test_converte_para_datetime(self):
        df = pd.DataFrame({'a': ['2024-01-01', '2024-01-02']})
        result = converter_tipos(df, {'a': 'datetime64[ns]'})
        assert pd.api.types.is_datetime64_any_dtype(result['a'])
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
