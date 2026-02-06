"""Testes para normalizar."""
import pytest
import pandas as pd
import numpy as np
from src.features.normalizacao.normalizar import normalizar


def test_normalizar_sem_agrupamento():
    """Testa normalização sem agrupamento."""
    df = pd.DataFrame({
        'valor': [10.0, 20.0, 30.0, 40.0]
    })
    
    result, scaler = normalizar(df, ['valor'], metodo='standard')
    
    assert 'valor' in result.columns
    assert scaler is not None
    assert abs(result['valor'].mean()) < 0.01  # Próximo de 0
    assert abs(result['valor'].std() - 1.0) < 0.01  # Próximo de 1


def test_normalizar_com_agrupamento():
    """Testa normalização com agrupamento."""
    df = pd.DataFrame({
        'valor': [10.0, 20.0, 30.0, 40.0],
        'grupo': ['A', 'A', 'B', 'B']
    })
    
    result, scalers = normalizar(
        df, 
        ['valor'], 
        metodo='standard',
        agrupamento='grupo'
    )
    
    assert 'valor' in result.columns
    assert isinstance(scalers, dict)
    assert 'A' in scalers
    assert 'B' in scalers
