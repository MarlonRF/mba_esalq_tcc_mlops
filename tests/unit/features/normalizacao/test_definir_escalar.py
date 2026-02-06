"""Testes para pick_scaler."""
import pytest
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from src.features.normalizacao.definir_escalar import pick_scaler


def test_pick_scaler_standard():
    """Testa seleção do StandardScaler."""
    scaler = pick_scaler('standard')
    assert isinstance(scaler, StandardScaler)


def test_pick_scaler_minmax():
    """Testa seleção do MinMaxScaler."""
    scaler = pick_scaler('minmax')
    assert isinstance(scaler, MinMaxScaler)


def test_pick_scaler_robust():
    """Testa seleção do RobustScaler."""
    scaler = pick_scaler('robust')
    assert isinstance(scaler, RobustScaler)


def test_pick_scaler_invalid():
    """Testa erro com método inválido."""
    with pytest.raises((ValueError, KeyError)):
        pick_scaler('invalid_method')
