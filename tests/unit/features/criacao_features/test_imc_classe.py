"""
Testes unitários para função imc_classe.
"""
import numpy as np
import pytest


@pytest.mark.unit
class TestIMCClasse:
    """Testes para função imc_classe"""

    def test_abaixo_do_peso(self):
        """Testa classificação abaixo do peso"""
        from src.processamento.derivadas.imc_classe import imc_classe
        
        assert imc_classe(17.0) == "Abaixo do peso"
        assert imc_classe(18.4) == "Abaixo do peso"
        
    def test_peso_normal(self):
        """Testa classificação peso normal"""
        from src.processamento.derivadas.imc_classe import imc_classe
        
        assert imc_classe(18.5) == "Peso Normal"
        assert imc_classe(22.0) == "Peso Normal"
        assert imc_classe(24.9) == "Peso Normal"
        
    def test_sobrepeso(self):
        """Testa classificação sobrepeso"""
        from src.processamento.derivadas.imc_classe import imc_classe
        
        assert imc_classe(25.0) == "Sobrepeso"
        assert imc_classe(29.9) == "Sobrepeso"
        
    def test_obesidade_graus(self):
        """Testa diferentes graus de obesidade"""
        from src.processamento.derivadas.imc_classe import imc_classe
        
        assert imc_classe(30.0) == "Obesidade Grau I"
        assert imc_classe(35.0) == "Obesidade Grau II"
        assert imc_classe(40.0) == "Obesidade Grau III"
        assert imc_classe(45.0) == "Obesidade Grau III"
        
    def test_valor_nulo(self):
        """Testa tratamento de valor nulo"""
        from src.processamento.derivadas.imc_classe import imc_classe
        
        resultado = imc_classe(np.nan)
        assert np.isnan(resultado) if isinstance(resultado, float) else resultado is np.nan
