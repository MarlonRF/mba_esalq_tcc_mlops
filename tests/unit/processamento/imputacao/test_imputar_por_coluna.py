"""
Testes unitários para imputar_por_coluna.
"""
import numpy as np
import pandas as pd
import pytest

from src.processamento.imputacao import imputar_por_coluna


class TestImputarPorColuna:
    """Testes para imputação customizada por coluna"""

    def test_imputacao_median_coluna_especifica(self):
        """Testa imputação com mediana em coluna específica"""
        df = pd.DataFrame({
            'idade': [25, np.nan, 35, 40],
            'peso': [70, 80, np.nan, 75],
        })
        
        config = {'idade': 'median'}
        df_result = imputar_por_coluna(df, config)
        
        # idade deve ser imputada com mediana (32.5)
        assert not df_result['idade'].isna().any()
        assert df_result['idade'].iloc[1] == 32.5
        
        # peso não deve ser imputado (não está no config)
        assert df_result['peso'].isna().sum() == 1

    def test_imputacao_mode_coluna_categorica(self):
        """Testa imputação com moda em coluna categórica"""
        df = pd.DataFrame({
            'sexo': ['m', 'f', 'f', np.nan, 'f'],
            'idade': [25, 30, 35, 40, 45],
        })
        
        config = {'sexo': 'mode'}
        df_result = imputar_por_coluna(df, config)
        
        # sexo deve ser imputado com moda ('f')
        assert not df_result['sexo'].isna().any()
        assert df_result['sexo'].iloc[3] == 'f'

    def test_imputacao_backward_fill(self):
        """Testa imputação com backward fill"""
        df = pd.DataFrame({
            'p5': [1, np.nan, np.nan, 4, 5],
            'p6': [10, 20, 30, 40, 50],
        })
        
        config = {'p5': 'backward'}
        df_result = imputar_por_coluna(df, config)
        
        # p5 deve ser preenchido com backward fill
        assert not df_result['p5'].isna().any()
        assert df_result['p5'].iloc[1] == 4
        assert df_result['p5'].iloc[2] == 4

    def test_imputacao_forward_fill(self):
        """Testa imputação com forward fill"""
        df = pd.DataFrame({
            'temperatura': [20.0, 21.5, np.nan, np.nan, 22.0],
        })
        
        config = {'temperatura': 'forward'}
        df_result = imputar_por_coluna(df, config)
        
        # temperatura deve ser preenchida com forward fill
        assert df_result['temperatura'].iloc[2] == 21.5
        assert df_result['temperatura'].iloc[3] == 21.5

    def test_imputacao_valor_constante(self):
        """Testa imputação com valor constante customizado"""
        df = pd.DataFrame({
            'vestimenta': ['leve', np.nan, 'pesada', np.nan],
            'categoria': ['A', 'B', 'C', 'D'],
        })
        
        config = {'vestimenta': 'desconhecido'}
        df_result = imputar_por_coluna(df, config)
        
        # vestimenta deve ser imputada com 'desconhecido'
        assert not df_result['vestimenta'].isna().any()
        assert df_result['vestimenta'].iloc[1] == 'desconhecido'
        assert df_result['vestimenta'].iloc[3] == 'desconhecido'

    def test_imputacao_valor_numerico_constante(self):
        """Testa imputação com valor numérico constante"""
        df = pd.DataFrame({
            'score': [10.0, np.nan, 30.0, np.nan],
        })
        
        config = {'score': 0}
        df_result = imputar_por_coluna(df, config)
        
        # score deve ser imputado com 0
        assert df_result['score'].iloc[1] == 0
        assert df_result['score'].iloc[3] == 0

    def test_imputacao_multiplas_colunas_diferentes_metodos(self):
        """Testa imputação com métodos diferentes para várias colunas"""
        df = pd.DataFrame({
            'idade': [25, np.nan, 35, 40],
            'peso': [70, np.nan, 80, 75],
            'altura': [170, 165, np.nan, 175],
            'sexo': ['m', np.nan, 'f', 'm'],
        })
        
        config = {
            'idade': 'median',
            'peso': 'mean',
            'altura': 'zero',
            'sexo': 'mode',
        }
        df_result = imputar_por_coluna(df, config)
        
        # Verificar cada coluna
        assert not df_result['idade'].isna().any()
        assert not df_result['peso'].isna().any()
        assert not df_result['altura'].isna().any()
        assert not df_result['sexo'].isna().any()
        
        # idade → median
        assert df_result['idade'].iloc[1] == 32.5
        
        # peso → mean
        assert df_result['peso'].iloc[1] == 75.0
        
        # altura → zero
        assert df_result['altura'].iloc[2] == 0
        
        # sexo → mode
        assert df_result['sexo'].iloc[1] == 'm'

    def test_metodo_padrao_para_colunas_nao_especificadas(self):
        """Testa que método padrão é aplicado a colunas não especificadas"""
        df = pd.DataFrame({
            'idade': [25, np.nan, 35],
            'peso': [70, np.nan, 80],
            'altura': [170, np.nan, 175],
        })
        
        config = {'idade': 'mean'}  # Apenas idade especificada
        df_result = imputar_por_coluna(df, config, metodo_padrao='median')
        
        # idade usa mean
        assert df_result['idade'].iloc[1] == 30.0
        
        # peso e altura usam median (método padrão)
        assert df_result['peso'].iloc[1] == 75.0
        assert df_result['altura'].iloc[1] == 172.5

    def test_coluna_inexistente_no_config(self):
        """Testa que configuração para coluna inexistente é ignorada"""
        df = pd.DataFrame({
            'idade': [25, np.nan, 35],
        })
        
        config = {
            'idade': 'median',
            'coluna_inexistente': 'mean',  # Esta não existe
        }
        
        # Não deve dar erro
        df_result = imputar_por_coluna(df, config)
        assert not df_result['idade'].isna().any()

    def test_coluna_sem_valores_faltantes(self):
        """Testa que colunas sem NaN não são modificadas"""
        df = pd.DataFrame({
            'idade': [25, 30, 35],
            'peso': [70, np.nan, 80],
        })
        
        config = {
            'idade': 'mean',  # Não tem NaN
            'peso': 'median',
        }
        df_result = imputar_por_coluna(df, config)
        
        # idade não deve ser modificada (não tinha NaN)
        pd.testing.assert_series_equal(df['idade'], df_result['idade'])
        
        # peso deve ser imputado
        assert not df_result['peso'].isna().any()

    def test_config_vazio(self):
        """Testa comportamento com configuração vazia"""
        df = pd.DataFrame({
            'idade': [25, np.nan, 35],
        })
        
        config = {}
        df_result = imputar_por_coluna(df, config, metodo_padrao='median')
        
        # Deve usar método padrão
        assert not df_result['idade'].isna().any()
        assert df_result['idade'].iloc[1] == 30.0
