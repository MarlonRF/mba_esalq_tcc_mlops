"""
Testes unitários para criação de features derivadas.
"""
import pandas as pd
import pytest
import numpy as np

from src.features.criacao_features import (
    calcular_valor_imc,
    imc_classe,
    calcular_heat_index,
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    calcular_ponto_orvalho,
    calcular_tu_stull,
    adicionar_features_derivadas,
=======
    calcular_dew_point,
    multiplicacao_colunas,
>>>>>>> Stashed changes
=======
    calcular_dew_point,
    multiplicacao_colunas,
>>>>>>> Stashed changes
=======
    calcular_dew_point,
    multiplicacao_colunas,
>>>>>>> Stashed changes
=======
    calcular_dew_point,
    multiplicacao_colunas,
>>>>>>> Stashed changes
)


class TestCalcularValorIMC:
    """Testes para cálculo de IMC."""
    
    def test_calcula_imc_correto(self):
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        peso = pd.Series([70, 80, 60])
        altura = pd.Series([1.75, 1.80, 1.65])
        
        result = calcular_valor_imc(peso, altura)
        
        expected_0 = 70 / (1.75 ** 2)
        expected_1 = 80 / (1.80 ** 2)
        expected_2 = 60 / (1.65 ** 2)
        
        assert np.isclose(result.iloc[0], expected_0, rtol=0.01)
        assert np.isclose(result.iloc[1], expected_1, rtol=0.01)
        assert np.isclose(result.iloc[2], expected_2, rtol=0.01)
        
    def test_imc_com_nan(self):
        peso = pd.Series([70, np.nan, 60])
        altura = pd.Series([1.75, 1.80, np.nan])
        
        result = calcular_valor_imc(peso, altura)
        
        assert not pd.isna(result.iloc[0])
        assert pd.isna(result.iloc[1])
        assert pd.isna(result.iloc[2])
        
    def test_imc_altura_zero(self):
        peso = pd.Series([70])
        altura = pd.Series([0])
        
        result = calcular_valor_imc(peso, altura)
        
        assert pd.isna(result.iloc[0]) or result.iloc[0] == np.inf
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
        df = pd.DataFrame({
            'peso': [70, 80],
            'altura': [1.75, 1.80]
        })
        result = calcular_valor_imc(df, 'peso', 'altura')
        
        expected_imc_0 = 70 / (1.75 ** 2)
        expected_imc_1 = 80 / (1.80 ** 2)
        
        assert np.isclose(result.iloc[0], expected_imc_0, rtol=0.01)
        assert np.isclose(result.iloc[1], expected_imc_1, rtol=0.01)
        
    def test_trata_valores_invalidos(self):
        df = pd.DataFrame({
            'peso': [70, 0, -10],
            'altura': [1.75, 1.80, 1.70]
        })
        result = calcular_valor_imc(df, 'peso', 'altura')
        
        assert not np.isnan(result.iloc[0])
        assert np.isnan(result.iloc[1]) or result.iloc[1] == 0
        assert np.isnan(result.iloc[2]) or result.iloc[2] == 0
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes


class TestIMCClasse:
    """Testes para classificação de IMC."""
    
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    def test_classificacao_magreza(self):
        imc = pd.Series([16, 17])
        result = imc_classe(imc)
        assert all(result == 'Magreza')
        
    def test_classificacao_normal(self):
        imc = pd.Series([18.5, 22, 24.9])
        result = imc_classe(imc)
        assert all(result == 'Normal')
        
    def test_classificacao_sobrepeso(self):
        imc = pd.Series([25, 27, 29.9])
        result = imc_classe(imc)
        assert all(result == 'Sobrepeso')
        
    def test_classificacao_obesidade(self):
        imc = pd.Series([30, 35, 40])
        result = imc_classe(imc)
        assert all(result == 'Obesidade')
        
    def test_classificacao_com_nan(self):
        imc = pd.Series([20, np.nan, 30])
        result = imc_classe(imc)
        assert result.iloc[0] == 'Normal'
        assert pd.isna(result.iloc[1])
        assert result.iloc[2] == 'Obesidade'
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    def test_classifica_baixo_peso(self):
        result = imc_classe(17.0)
        assert result == 'Baixo peso'
        
    def test_classifica_peso_normal(self):
        result = imc_classe(22.0)
        assert result == 'Peso normal'
        
    def test_classifica_sobrepeso(self):
        result = imc_classe(27.0)
        assert result == 'Sobrepeso'
        
    def test_classifica_obesidade(self):
        result = imc_classe(32.0)
        assert result == 'Obesidade'
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes


class TestCalcularHeatIndex:
    """Testes para cálculo de índice de calor."""
    
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    def test_calcula_heat_index_valores_normais(self):
        temperatura = pd.Series([30, 35, 25])
        umidade = pd.Series([70, 80, 60])
        
        result = calcular_heat_index(temperatura, umidade)
        
        assert len(result) == 3
        assert all(isinstance(x, (int, float)) or pd.isna(x) for x in result)
        
    def test_heat_index_com_nan(self):
        temperatura = pd.Series([30, np.nan])
        umidade = pd.Series([np.nan, 70])
        
        result = calcular_heat_index(temperatura, umidade)
        
        assert pd.isna(result.iloc[0])
        assert pd.isna(result.iloc[1])


class TestCalcularPontoOrvalho:
    """Testes para cálculo de ponto de orvalho."""
    
    def test_calcula_ponto_orvalho_valores_normais(self):
        temperatura = pd.Series([25, 30, 20])
        umidade = pd.Series([60, 70, 80])
        
        result = calcular_ponto_orvalho(temperatura, umidade)
        
        assert len(result) == 3
        assert all(isinstance(x, (int, float)) or pd.isna(x) for x in result)
        assert all(result <= temperatura)  # Dew point sempre <= temperatura
        
    def test_ponto_orvalho_com_nan(self):
        temperatura = pd.Series([25, np.nan])
        umidade = pd.Series([np.nan, 60])
        
        result = calcular_ponto_orvalho(temperatura, umidade)
        
        assert pd.isna(result.iloc[0])
        assert pd.isna(result.iloc[1])


class TestCalcularTUStull:
    """Testes para multiplicação T*U (Stull)."""
    
    def test_multiplica_temperatura_umidade(self):
        temperatura = pd.Series([30, 25, 20])
        umidade = pd.Series([70, 60, 80])
        
        result = calcular_tu_stull(temperatura, umidade)
        
        expected = temperatura * umidade
        pd.testing.assert_series_equal(result, expected)
        
    def test_tu_com_nan(self):
        temperatura = pd.Series([30, np.nan, 20])
        umidade = pd.Series([70, 60, np.nan])
        
        result = calcular_tu_stull(temperatura, umidade)
        
        assert not pd.isna(result.iloc[0])
        assert pd.isna(result.iloc[1])
        assert pd.isna(result.iloc[2])


class TestAdicionarFeaturesDerivadas:
    """Testes para função de adicionar múltiplas features."""
    
    @pytest.fixture
    def df_sample(self):
        return pd.DataFrame({
            'peso': [70, 80, 60],
            'altura': [1.75, 1.80, 1.65],
            'tbs': [30, 25, 20],
            'ur': [70, 60, 80],
        })
    
    def test_adicionar_imc(self, df_sample):
        result = adicionar_features_derivadas(df_sample, tipos=['imc'])
        assert 'imc' in result.columns
        assert len(result) == len(df_sample)
        
    def test_adicionar_imc_classe(self, df_sample):
        result = adicionar_features_derivadas(df_sample, tipos=['imc', 'imc_classe'])
        assert 'imc' in result.columns
        assert 'imc_classe' in result.columns
        
    def test_adicionar_heat_index(self, df_sample):
        result = adicionar_features_derivadas(df_sample, tipos=['heat_index'])
        assert 'heat_index' in result.columns
        
    def test_adicionar_dew_point(self, df_sample):
        result = adicionar_features_derivadas(df_sample, tipos=['dew_point'])
        assert 'dew_point' in result.columns
        
    def test_adicionar_tu(self, df_sample):
        result = adicionar_features_derivadas(df_sample, tipos=['t*u'])
        assert 't*u' in result.columns
        
    def test_adicionar_multiplas_features(self, df_sample):
        result = adicionar_features_derivadas(
            df_sample,
            tipos=['imc', 'heat_index', 't*u']
        )
        assert 'imc' in result.columns
        assert 'heat_index' in result.columns
        assert 't*u' in result.columns
        
    def test_sem_tipos(self, df_sample):
        result = adicionar_features_derivadas(df_sample, tipos=[])
        pd.testing.assert_frame_equal(result, df_sample)
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    def test_calcula_heat_index(self):
        result = calcular_heat_index(30, 70)
        assert isinstance(result, (int, float))
        assert result > 30  # Heat index deve ser maior que temperatura


class TestCalcularDewPoint:
    """Testes para cálculo de ponto de orvalho."""
    
    def test_calcula_dew_point(self):
        result = calcular_dew_point(25, 60)
        assert isinstance(result, (int, float))
        assert result < 25  # Dew point deve ser menor que temperatura


class TestMultiplicacaoColunas:
    """Testes para multiplicação de colunas."""
    
    def test_multiplica_duas_colunas(self):
        df = pd.DataFrame({
            'a': [2, 3, 4],
            'b': [5, 6, 7]
        })
        result = multiplicacao_colunas(df, 'a', 'b')
        
        assert result.tolist() == [10, 18, 28]
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
