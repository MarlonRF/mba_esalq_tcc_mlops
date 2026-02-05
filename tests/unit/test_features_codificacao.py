"""
Testes unitários para módulo de codificação de features.
"""
import pandas as pd
import pytest
import numpy as np

from src.features.codificacao import (
    aplicar_codificacao_rotulos,
    aplicar_dummy,
)


class TestAplicarCodificacaoRotulos:
    """Testes para função aplicar_codificacao_rotulos."""
    
    def test_codifica_coluna_categorica(self):
        df = pd.DataFrame({'sexo': ['m', 'f', 'm', 'f']})
        result, mapa = aplicar_codificacao_rotulos(df, ['sexo'], sufixo='_cod')
        
        assert 'sexo_cod' in result.columns
        assert len(mapa) == 1
        assert 'sexo' in mapa
        assert result['sexo_cod'].nunique() == 2
        
    def test_preserva_coluna_original(self):
        df = pd.DataFrame({'sexo': ['m', 'f']})
        result, _ = aplicar_codificacao_rotulos(df, ['sexo'])
        
        assert 'sexo' in result.columns
        assert 'sexo_cod' in result.columns


class TestAplicarDummy:
    """Testes para função aplicar_dummy."""
    
    def test_cria_colunas_dummy(self):
        df = pd.DataFrame({'cor': ['red', 'blue', 'red']})
        result = aplicar_dummy(df, ['cor'], prefixo='cor')
        
        assert 'cor_red' in result.columns
        assert 'cor_blue' in result.columns
        assert result['cor_red'].iloc[0] == 1
        assert result['cor_blue'].iloc[0] == 0
        
    def test_drop_first(self):
        df = pd.DataFrame({'cor': ['red', 'blue', 'green']})
        result = aplicar_dummy(df, ['cor'], drop_first=True)
        
        # Com drop_first=True, deve ter n-1 colunas
        dummy_cols = [c for c in result.columns if c.startswith('cor_')]
        assert len(dummy_cols) == 2
