"""Testes para calcular_tu_stull."""
import pytest
import pandas as pd
import numpy as np
from src.processamento.derivadas.calcular_tu_stull import calcular_tu_stull


def test_calcular_tu_stull():
    """Testa cálculo da temperatura x umidade (Stull)."""
    df = pd.DataFrame({
        'tmedia': [25.0, 30.0],
        'ur': [60.0, 70.0]
    })
    
    result = calcular_tu_stull(df)
    
    assert 't*u' in result.columns
    assert not result['t*u'].isna().any()
    assert result['t*u'].dtype == np.float64
