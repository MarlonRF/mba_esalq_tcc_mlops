"""
Testes unitários para função calcular_imc.
"""
import numpy as np
import pytest


@pytest.mark.unit
class TestCalcularIMC:
    """Testes para função calcular_imc"""

    def test_calculo_imc_normal(self):
        """Testa cálculo de IMC com valores normais"""
        from src.processamento.derivadas.calcular_imc import calcular_imc
        
        # IMC = peso / (altura_m)^2
        # 70kg / (1.75m)^2 = 22.86
        imc = calcular_imc(70, 175)
        
        assert pytest.approx(imc, rel=0.01) == 22.86
        
    def test_imc_valores_nulos(self):
        """Testa que valores nulos retornam NaN"""
        from src.processamento.derivadas.calcular_imc import calcular_imc
        
        assert np.isnan(calcular_imc(None, 175))
        assert np.isnan(calcular_imc(70, None))
        assert np.isnan(calcular_imc(np.nan, 175))
        
    def test_altura_zero(self):
        """Testa proteção contra divisão por zero"""
        from src.processamento.derivadas.calcular_imc import calcular_imc
        
        assert np.isnan(calcular_imc(70, 0))
        
    def test_imc_diferentes_pesos(self):
        """Testa que IMC aumenta com o peso"""
        from src.processamento.derivadas.calcular_imc import calcular_imc
        
        imc1 = calcular_imc(60, 170)
        imc2 = calcular_imc(80, 170)
        
        assert imc2 > imc1
