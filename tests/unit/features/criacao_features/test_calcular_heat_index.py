"""
Testes unitários para função calcular_heat_index.
"""
import numpy as np
import pytest


@pytest.mark.unit
class TestCalcularHeatIndex:
    """Testes para função calcular_heat_index"""

    def test_heat_index_valores_normais(self):
        """Testa cálculo com valores típicos"""
        from src.features.criacao_features.calcular_heat_index import calcular_heat_index
        
        # Temperatura moderada e umidade média
        hi = calcular_heat_index(25.0, 60.0)
        
        assert isinstance(hi, (int, float))
        assert not np.isnan(hi)
        
    def test_heat_index_valores_nulos(self):
        """Testa que valores nulos retornam NaN"""
        from src.features.criacao_features.calcular_heat_index import calcular_heat_index
        
        assert np.isnan(calcular_heat_index(None, 60))
        assert np.isnan(calcular_heat_index(25, None))
        assert np.isnan(calcular_heat_index(np.nan, 60))
        
    def test_heat_index_aumenta_com_umidade(self):
        """Testa que heat index aumenta com umidade"""
        from src.features.criacao_features.calcular_heat_index import calcular_heat_index
        
        hi_baixa = calcular_heat_index(30.0, 30.0)
        hi_alta = calcular_heat_index(30.0, 80.0)
        
        # Com mesma temperatura, maior umidade = maior heat index
        assert hi_alta > hi_baixa
