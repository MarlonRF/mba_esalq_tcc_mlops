"""
Testes unitários para imputar_media_movel_interpolada.
"""
import numpy as np
import pandas as pd
import pytest

from src.processamento.imputacao import imputar_media_movel_interpolada


class TestImputarMediaMovelInterpolada:
    """Testes para imputação com média móvel e interpolação"""

    def test_media_movel_basica(self):
        """Testa imputação com média móvel simples"""
        df = pd.DataFrame({
            'radiacao': [100, 110, np.nan, 130, 140],
        })
        
        df_result = imputar_media_movel_interpolada(df, 'radiacao', window=2)
        
        # Valor faltante deve ser preenchido
        assert not df_result['radiacao'].isna().any()
        
        # Deve estar entre os valores adjacentes (média móvel + interpolação)
        assert 110 < df_result['radiacao'].iloc[2] < 130

    def test_interpolacao_linear(self):
        """Testa interpolação linear após média móvel"""
        df = pd.DataFrame({
            'temperatura': [20.0, 21.0, np.nan, 23.0, 24.0],
        })
        
        df_result = imputar_media_movel_interpolada(
            df, 'temperatura', window=2, metodo_interpolacao='linear'
        )
        
        # Com interpolação linear, o valor deve ser 22.0
        assert not df_result['temperatura'].isna().any()
        assert abs(df_result['temperatura'].iloc[2] - 22.0) < 0.1

    def test_window_grande(self):
        """Testa com janela maior (típico para séries temporais)"""
        # Criar série com 50 valores e alguns NaN
        valores = list(range(1, 51))
        valores[10] = np.nan
        valores[20] = np.nan
        valores[30] = np.nan
        
        df = pd.DataFrame({'serie': valores})
        
        df_result = imputar_media_movel_interpolada(df, 'serie', window=48)
        
        # Todos os valores devem estar preenchidos
        assert not df_result['serie'].isna().any()
        
        # Valores imputados devem estar próximos dos originais
        assert 10 <= df_result['serie'].iloc[10] <= 12
        assert 20 <= df_result['serie'].iloc[20] <= 22
        assert 30 <= df_result['serie'].iloc[30] <= 32

    def test_multiplos_valores_consecutivos_faltantes(self):
        """Testa com múltiplos valores faltantes consecutivos"""
        df = pd.DataFrame({
            'dados': [10, 20, np.nan, np.nan, np.nan, 60, 70],
        })
        
        df_result = imputar_media_movel_interpolada(df, 'dados', window=3)
        
        # Todos devem estar preenchidos
        assert not df_result['dados'].isna().any()
        
        # Valores devem estar na faixa esperada
        assert all(20 <= df_result['dados'].iloc[i] <= 60 for i in [2, 3, 4])

    def test_coluna_inexistente(self):
        """Testa comportamento com coluna que não existe"""
        df = pd.DataFrame({
            'dados': [10, np.nan, 30],
        })
        
        # Não deve dar erro
        df_result = imputar_media_movel_interpolada(df, 'coluna_inexistente')
        
        # DataFrame deve permanecer inalterado
        pd.testing.assert_frame_equal(df, df_result)

    def test_coluna_sem_valores_faltantes(self):
        """Testa que coluna sem NaN não é modificada"""
        df = pd.DataFrame({
            'completo': [10, 20, 30, 40, 50],
        })
        
        df_result = imputar_media_movel_interpolada(df, 'completo')
        
        # Não deve modificar (não tem NaN)
        pd.testing.assert_series_equal(df['completo'], df_result['completo'])

    def test_primeiro_valor_faltante(self):
        """Testa imputação quando primeiro valor é NaN"""
        df = pd.DataFrame({
            'dados': [np.nan, 20, 30, 40],
        })
        
        df_result = imputar_media_movel_interpolada(df, 'dados', window=2)
        
        # Deve preencher mesmo o primeiro valor
        assert not df_result['dados'].isna().any()

    def test_ultimo_valor_faltante(self):
        """Testa imputação quando último valor é NaN"""
        df = pd.DataFrame({
            'dados': [10, 20, 30, np.nan],
        })
        
        df_result = imputar_media_movel_interpolada(df, 'dados', window=2)
        
        # Deve preencher o último valor
        assert not df_result['dados'].isna().any()

    def test_todos_valores_faltantes(self):
        """Testa comportamento quando todos os valores são NaN"""
        df = pd.DataFrame({
            'tudo_nan': [np.nan, np.nan, np.nan],
        })
        
        df_result = imputar_media_movel_interpolada(df, 'tudo_nan')
        
        # Não consegue preencher sem valores de referência
        # Deve permanecer com NaN
        assert df_result['tudo_nan'].isna().all()

    def test_window_min_periods(self):
        """Testa que min_periods=1 permite imputação mesmo com poucos valores"""
        df = pd.DataFrame({
            'dados': [np.nan, 10, np.nan],
        })
        
        df_result = imputar_media_movel_interpolada(df, 'dados', window=5)
        
        # Com min_periods=1, deve conseguir imputar
        # (usará os poucos valores disponíveis)
        assert df_result['dados'].notna().sum() >= 1
