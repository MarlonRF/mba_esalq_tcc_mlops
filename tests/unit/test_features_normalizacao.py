"""
Testes unitários para normalização de features.
"""
import pandas as pd
import pytest
import numpy as np

from src.features.normalizacao import (
    pick_scaler,
    normalizar,
    SCALERS,
)


class TestPickScaler:
    """Testes para seleção de scaler."""
    
    def test_retorna_standard_scaler(self):
        scaler = pick_scaler('standard')
        assert scaler.__class__.__name__ == 'StandardScaler'
        
    def test_retorna_minmax_scaler(self):
        scaler = pick_scaler('minmax')
        assert scaler.__class__.__name__ == 'MinMaxScaler'
        
    def test_retorna_robust_scaler(self):
        scaler = pick_scaler('robust')
        assert scaler.__class__.__name__ == 'RobustScaler'
        
    def test_levanta_erro_metodo_invalido(self):
        with pytest.raises((ValueError, KeyError)):
            pick_scaler('invalid_method')


class TestNormalizar:
    """Testes para normalização de dados."""
    
    def test_normaliza_com_standard(self):
        df = pd.DataFrame({
            'a': [1, 2, 3, 4, 5],
            'b': [10, 20, 30, 40, 50]
        })
        result, scaler = normalizar(df, ['a', 'b'], metodo='standard')
        
        # Média deve ser próxima de 0
        assert np.abs(result['a'].mean()) < 0.01
        assert np.abs(result['b'].mean()) < 0.01
        
        # Desvio padrão deve ser próximo de 1
        assert np.abs(result['a'].std() - 1.0) < 0.01
        assert np.abs(result['b'].std() - 1.0) < 0.01
        
    def test_normaliza_com_minmax(self):
        df = pd.DataFrame({
            'a': [1, 2, 3, 4, 5]
        })
        result, scaler = normalizar(df, ['a'], metodo='minmax')
        
        # Valores devem estar entre 0 e 1
        assert result['a'].min() >= 0
        assert result['a'].max() <= 1
        
    def test_preserva_colunas_nao_normalizadas(self):
        df = pd.DataFrame({
            'a': [1, 2, 3],
            'b': ['x', 'y', 'z']
        })
        result, _ = normalizar(df, ['a'], metodo='standard')
        
        assert 'b' in result.columns
        assert result['b'].tolist() == ['x', 'y', 'z']
        
    def test_normaliza_por_agrupamento(self):
        df = pd.DataFrame({
            'grupo': ['A', 'A', 'B', 'B'],
            'valor': [1, 2, 10, 20]
        })
        result, scalers = normalizar(
            df, 
            ['valor'], 
            metodo='standard',
            agrupamento='grupo'
        )
        
        # Cada grupo deve ter média ~0
        for grupo in ['A', 'B']:
            grupo_data = result[result['grupo'] == grupo]['valor']
            assert np.abs(grupo_data.mean()) < 0.01
