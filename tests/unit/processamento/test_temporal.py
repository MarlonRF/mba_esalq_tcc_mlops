"""
Testes unitários para módulo de processamento temporal.
"""
import pandas as pd
import pytest
import numpy as np

from src.processamento.temporal import (
    criar_coluna_temporal,
    extrair_componentes_temporais,
)


class TestCriarColunaTemporal:
    """Testes para função criar_coluna_temporal."""
    
    def test_cria_mes_ano(self):
        df = pd.DataFrame({
            'data': pd.to_datetime(['2024-01-15', '2024-02-20', '2024-01-25'])
        })
        result = criar_coluna_temporal(df, coluna_data='data', formato='mes-ano')
        assert 'mes-ano' in result.columns
        assert result['mes-ano'].tolist() == ['2024-01', '2024-02', '2024-01']
    
    def test_cria_ano_mes(self):
        df = pd.DataFrame({
            'data': pd.to_datetime(['2024-01-15', '2024-02-20'])
        })
        result = criar_coluna_temporal(df, coluna_data='data', formato='ano-mes')
        assert 'ano-mes' in result.columns
    
    def test_cria_com_nome_customizado(self):
        df = pd.DataFrame({
            'data': pd.to_datetime(['2024-01-15'])
        })
        result = criar_coluna_temporal(
            df, 
            coluna_data='data', 
            formato='mes-ano',
            nome_coluna='periodo'
        )
        assert 'periodo' in result.columns


class TestExtrairComponentesTemporais:
    """Testes para função extrair_componentes_temporais."""
    
    def test_extrai_ano(self):
        df = pd.DataFrame({
            'data': pd.to_datetime(['2024-01-15', '2023-06-20'])
        })
        result = extrair_componentes_temporais(df, coluna_data='data', componentes=['ano'])
        assert 'ano' in result.columns
        assert result['ano'].tolist() == [2024, 2023]
    
    def test_extrai_mes(self):
        df = pd.DataFrame({
            'data': pd.to_datetime(['2024-01-15', '2024-06-20'])
        })
        result = extrair_componentes_temporais(df, coluna_data='data', componentes=['mes'])
        assert 'mes' in result.columns
        assert result['mes'].tolist() == [1, 6]
    
    def test_extrai_multiplos_componentes(self):
        df = pd.DataFrame({
            'data': pd.to_datetime(['2024-01-15'])
        })
        result = extrair_componentes_temporais(
            df, 
            coluna_data='data', 
            componentes=['ano', 'mes', 'dia']
        )
        assert 'ano' in result.columns
        assert 'mes' in result.columns
        assert 'dia' in result.columns
