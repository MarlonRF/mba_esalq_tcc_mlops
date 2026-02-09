"""Testes para calcular_tu_stull."""
import pytest
import pandas as pd
import numpy as np
from src.features.criacao_features.calcular_tu_stull import calcular_tu_stull


def test_calcular_tu_stull():
    """Testa cálculo da temperatura x umidade (Stull)."""
    result = calcular_tu_stull(25.0, 60.0)
    
    # A função retorna um float, não um DataFrame
    assert isinstance(result, (int, float, np.floating))
    assert not np.isnan(result)
    # Valor esperado aproximado para T=25°C e UR=60%
    assert 10.0 < result < 25.0

