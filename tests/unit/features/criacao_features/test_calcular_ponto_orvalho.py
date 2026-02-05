"""
Testes unitários para função calcular_ponto_orvalho.
"""
import numpy as np
import pytest


@pytest.mark.unit
class TestCalcularPontoOrvalho:
    """Testes para função calcular_ponto_orvalho"""

    def test_ponto_orvalho_basico(self):
        """Testa cálculo básico do ponto de orvalho"""
        from src.processamento.derivadas.calcular_ponto_orvalho import calcular_ponto_orvalho
        
        # Com 100% umidade, ponto de orvalho = temperatura
        po = calcular_ponto_orvalho(25.0, 100.0)
        assert po == 25.0
        
    def test_ponto_orvalho_menor_que_temperatura(self):
        """Testa que ponto de orvalho é menor que temperatura (exceto 100% UR)"""
        from src.processamento.derivadas.calcular_ponto_orvalho import calcular_ponto_orvalho
        
        po = calcular_ponto_orvalho(30.0, 50.0)
        assert po < 30.0
        
    def test_valores_nulos(self):
        """Testa tratamento de valores nulos"""
        from src.processamento.derivadas.calcular_ponto_orvalho import calcular_ponto_orvalho
        
        assert np.isnan(calcular_ponto_orvalho(None, 60))
        assert np.isnan(calcular_ponto_orvalho(25, None))
