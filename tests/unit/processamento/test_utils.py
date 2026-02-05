"""
Testes unitários para funções utilitárias de processamento.

Testa funções puras de cálculo que não dependem de
recursos externos ou estado global.
"""

import numpy as np
import pandas as pd
import pytest

from funcoes.processamento import (_calcular_imc, _calcular_indice_calor,
                                   _calcular_ponto_orvalho,
                                   _codificar_com_labels,
                                   _converter_para_float, _imc_classe)


class TestConverterParaFloat:
    """Testes para função _converter_para_float"""

    @pytest.mark.unit
    def test_conversao_basica(self):
        """Testa conversão básica de string para float"""
        serie = pd.Series(["1.5", "2.3", "10.0"])
        resultado = _converter_para_float(serie)
        
        assert isinstance(resultado, pd.Series)
        assert resultado.iloc[0] == 1.5
        assert resultado.iloc[1] == 2.3
        assert resultado.iloc[2] == 10.0

    @pytest.mark.unit
    def test_conversao_virgula_decimal(self):
        """Testa conversão de números com vírgula como separador decimal"""
        serie = pd.Series(["1,5", "2,3", "10,7"])
        resultado = _converter_para_float(serie)
        
        assert resultado.iloc[0] == 1.5
        assert resultado.iloc[1] == 2.3
        assert resultado.iloc[2] == 10.7

    @pytest.mark.unit
    def test_valores_nulos_preservados(self):
        """Testa se valores nulos são preservados"""
        serie = pd.Series(["1.5", np.nan, "2.3", None])
        resultado = _converter_para_float(serie)
        
        assert resultado.iloc[0] == 1.5
        assert pd.isna(resultado.iloc[1])
        assert resultado.iloc[2] == 2.3
        assert pd.isna(resultado.iloc[3])

    @pytest.mark.unit
    def test_valores_invalidos_viram_nan(self):
        """Testa se valores inválidos são convertidos para NaN"""
        serie = pd.Series(["1.5", "abc", "xyz", "2.3"])
        resultado = _converter_para_float(serie)
        
        assert resultado.iloc[0] == 1.5
        assert pd.isna(resultado.iloc[1])
        assert pd.isna(resultado.iloc[2])
        assert resultado.iloc[3] == 2.3


class TestCalcularIMC:
    """Testes para função _calcular_imc"""

    @pytest.mark.unit
    def test_calculo_imc_normal(self):
        """Testa cálculo básico do IMC"""
        # IMC = peso / altura² (altura em centímetros)
        resultado = _calcular_imc(70.0, 175.0)  # altura em cm
        esperado = 70.0 / (1.75 * 1.75)  # conversão para metros
        assert abs(resultado - esperado) < 0.01

    @pytest.mark.unit
    def test_calculo_imc_valores_extremos(self):
        """Testa IMC com valores nos extremos"""
        resultado_baixo = _calcular_imc(40.0, 1.80)
        resultado_alto = _calcular_imc(120.0, 1.60)
        
        assert isinstance(resultado_baixo, (int, float))
        assert isinstance(resultado_alto, (int, float))
        assert resultado_baixo > 0
        assert resultado_alto > 0

    @pytest.mark.unit
    def test_imc_valores_nulos(self):
        """Testa comportamento com valores nulos"""
        assert pd.isna(_calcular_imc(None, 1.75))
        assert pd.isna(_calcular_imc(70.0, None))
        assert pd.isna(_calcular_imc(None, None))

    @pytest.mark.unit
    def test_imc_altura_zero(self):
        """Testa comportamento com altura zero (divisão por zero)"""
        resultado = _calcular_imc(70.0, 0.0)
        # Deve retornar inf ou nan, não deve dar erro
        assert np.isinf(resultado) or pd.isna(resultado)


class TestIMCClasse:
    """Testes para função _imc_classe"""

    @pytest.mark.unit
    def test_classificacao_imc_todas_categorias(self):
        """Testa todas as categorias de classificação do IMC"""
        assert _imc_classe(16.0) == "Abaixo do peso"
        assert _imc_classe(17.0) == "Abaixo do peso"
        assert _imc_classe(18.0) == "Abaixo do peso"
        assert _imc_classe(22.0) == "Peso Normal"
        assert _imc_classe(26.0) == "Sobrepeso"
        assert _imc_classe(32.0) == "Obesidade Grau I"
        assert _imc_classe(37.0) == "Obesidade Grau II"
        assert _imc_classe(42.0) == "Obesidade Grau III"

    @pytest.mark.unit
    def test_classificacao_imc_limites(self):
        """Testa classificação nos valores limites"""
        assert _imc_classe(16.99) == "Abaixo do peso"
        assert _imc_classe(17.0) == "Abaixo do peso"
        assert _imc_classe(24.99) == "Peso Normal"
        assert _imc_classe(25.0) == "Sobrepeso"


class TestCalcularIndiceCalor:
    """Testes para função _calcular_indice_calor"""

    @pytest.mark.unit
    def test_indice_calor_condicoes_normais(self):
        """Testa cálculo do índice de calor em condições normais"""
        # Temperatura 30°C, umidade 60%
        indice = _calcular_indice_calor(30.0, 60.0)

        # Baseado na fórmula: -8.78469475556 + 1.61139411 * T + 2.33854883889 * UR - 0.14611605 * T * UR
        expected = -8.78469475556 + 1.61139411 * 30 + 2.33854883889 * 60 - 0.14611605 * 30 * 60
        assert abs(indice - expected) < 0.01

    @pytest.mark.unit
    def test_indice_calor_temperatura_baixa(self):
        """Testa índice de calor com temperatura baixa"""
        indice = _calcular_indice_calor(20.0, 50.0)
        # A fórmula sempre se aplica, não retorna a temperatura original
        expected = -8.78469475556 + 1.61139411 * 20 + 2.33854883889 * 50 - 0.14611605 * 20 * 50
        assert abs(indice - expected) < 0.01

    @pytest.mark.unit
    def test_indice_calor_valores_nulos(self):
        """Testa comportamento com valores nulos"""
        assert pd.isna(_calcular_indice_calor(None, 60.0))
        assert pd.isna(_calcular_indice_calor(25.0, None))


class TestCalcularPontoOrvalho:
    """Testes para função _calcular_ponto_orvalho"""

    @pytest.mark.unit
    def test_ponto_orvalho_calculo_basico(self):
        """Testa cálculo básico do ponto de orvalho"""
        ponto = _calcular_ponto_orvalho(25.0, 60.0)
        
        # Ponto de orvalho deve ser menor que a temperatura
        assert isinstance(ponto, (int, float))
        assert ponto < 25.0
        assert ponto > 0  # Deve ser positivo para condições normais

    @pytest.mark.unit
    def test_ponto_orvalho_umidade_alta(self):
        """Testa ponto de orvalho com umidade alta (próximo da temperatura)"""
        ponto = _calcular_ponto_orvalho(25.0, 95.0)
        
        # Com umidade muito alta, ponto de orvalho deve estar próximo da temperatura
        assert isinstance(ponto, (int, float))
        assert 20.0 <= ponto <= 25.0

    @pytest.mark.unit
    def test_ponto_orvalho_valores_nulos(self):
        """Testa comportamento com valores nulos"""
        assert pd.isna(_calcular_ponto_orvalho(None, 60.0))
        assert pd.isna(_calcular_ponto_orvalho(25.0, None))


class TestCodificarComLabels:
    """Testes para função _codificar_com_labels"""

    @pytest.mark.unit
    def test_codificacao_basica(self):
        """Testa codificação básica com labels"""
        serie = pd.Series(["a", "b", "c", "a", "b"])

        serie_codificada, mapeamento = _codificar_com_labels(serie)

        # Verifica se a codificação foi feita
        assert len(serie_codificada) == len(serie)
        assert str(serie_codificada.dtype) == "Int64"  # Pandas nullable integer

        # Verifica se o mapeamento foi criado
        assert isinstance(mapeamento, dict)
        assert len(mapeamento) == 3  # 'a', 'b', 'c'

        # Verifica consistência: mesmos valores devem ter mesmos códigos
        assert serie_codificada.iloc[0] == serie_codificada.iloc[3]  # 'a'
        assert serie_codificada.iloc[1] == serie_codificada.iloc[4]  # 'b'

    @pytest.mark.unit
    def test_codificacao_com_nulos(self):
        """Testa codificação com valores nulos"""
        serie = pd.Series(["a", np.nan, "b", "a"])

        serie_codificada, mapeamento = _codificar_com_labels(serie)

        # Valores nulos devem ser preservados
        # Verificar que nulos viram código específico (__faltante__)
        assert not pd.isna(serie_codificada.iloc[1])  # Não é mais NaN
        assert mapeamento[serie_codificada.iloc[1]] == "__faltante__"
        assert not pd.isna(serie_codificada.iloc[0])
        assert not pd.isna(serie_codificada.iloc[2])

    @pytest.mark.unit
    def test_codificacao_serie_vazia(self):
        """Testa codificação de série vazia"""
        serie = pd.Series([], dtype=object)

        serie_codificada, mapeamento = _codificar_com_labels(serie)

        assert len(serie_codificada) == 0
        assert isinstance(mapeamento, dict)
        assert len(mapeamento) == 0