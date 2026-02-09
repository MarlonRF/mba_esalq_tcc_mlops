"""
Testes unitários para módulo de processamento temporal.
"""
import pandas as pd
import pytest
import numpy as np

from src.processamento.temporal import (
    converter_colunas_temporais,
    adicionar_mes_ano,
    garantir_agrupamento_temporal,
)


class TestAdicionarMesAno:
    """Testes para função adicionar_mes_ano."""
    
    def test_cria_mes_ano(self):
        df = pd.DataFrame({
            'data': pd.to_datetime(['2024-01-15', '2024-02-20', '2024-01-25'])
        })
        result = adicionar_mes_ano(df, coluna_data='data')
        assert 'mes-ano' in result.columns or 'mes_ano' in result.columns
    
    def test_com_dados_validos(self):
        df = pd.DataFrame({
            'data': pd.to_datetime(['2024-01-15', '2024-02-20'])
        })
        result = adicionar_mes_ano(df, coluna_data='data')
        assert len(result) == len(df)


class TestConverterColunasTemporais:
    """Testes para função converter_colunas_temporais."""
    
    def test_converte_string_para_datetime(self):
        df = pd.DataFrame({
            'data': ['2024-01-15', '2023-06-20']
        })
        result = converter_colunas_temporais(df, coluna_data='data')
        assert pd.api.types.is_datetime64_any_dtype(result['data'])
    
    def test_mantém_dados_validos(self):
        df = pd.DataFrame({
            'data': ['2024-01-15', '2024-06-20']
        })
        result = converter_colunas_temporais(df, coluna_data='data')
        assert len(result) == len(df)


class TestGarantirAgrupamentoTemporal:
    """Testes para função garantir_agrupamento_temporal."""
    
    def test_cria_agrupamento_se_necessario(self):
        df = pd.DataFrame({
            'data': pd.to_datetime(['2024-01-15', '2024-01-20', '2024-02-15'])
        })
        result = garantir_agrupamento_temporal(df, coluna_data='data')
        assert len(result.columns) >= len(df.columns)

