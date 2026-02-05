"""
Testes unitários para classificar_metricas.py
"""
import pytest
import pandas as pd
from src.treinamento.avaliacao.classificar_metricas import classificar_metricas


@pytest.fixture
def tabela_metricas():
    """Tabela de métricas para testes."""
    return pd.DataFrame({
        'Model': ['model_a', 'model_b', 'model_c'],
        'Accuracy': [0.85, 0.90, 0.80],
        'F1': [0.83, 0.88, 0.82],
        'Precision': [0.86, 0.89, 0.84]
    })


def test_classificar_metricas_colunas_classificacao(tabela_metricas):
    """Testa que colunas de classificação são criadas."""
    resultado = classificar_metricas(
        tabela=tabela_metricas,
        metricas=['Accuracy', 'F1']
    )
    
    assert 'classificacao_Accuracy' in resultado.columns
    assert 'classificacao_F1' in resultado.columns
    assert 'classificacao_media' in resultado.columns


def test_classificar_metricas_ranking_correto(tabela_metricas):
    """Testa que ranking está correto (1 = melhor)."""
    resultado = classificar_metricas(
        tabela=tabela_metricas,
        metricas=['Accuracy']
    )
    
    # model_b tem maior Accuracy (0.90), deve ter rank 1
    idx_model_b = resultado[resultado['Model'] == 'model_b'].index[0]
    assert resultado.loc[idx_model_b, 'classificacao_Accuracy'] == 1


def test_classificar_metricas_ordenado_por_media(tabela_metricas):
    """Testa que resultado está ordenado por classificação média."""
    resultado = classificar_metricas(
        tabela=tabela_metricas,
        metricas=['Accuracy', 'F1', 'Precision']
    )
    
    # model_b deve estar primeiro (melhores métricas)
    assert resultado.iloc[0]['Model'] == 'model_b'
    
    # Classificação média deve estar em ordem crescente
    assert resultado['classificacao_media'].is_monotonic_increasing


def test_classificar_metricas_erro_metrica_inexistente(tabela_metricas):
    """Testa erro quando métrica não existe."""
    with pytest.raises(ValueError, match="Métricas não encontradas"):
        classificar_metricas(
            tabela=tabela_metricas,
            metricas=['Accuracy', 'MetricaInexistente']
        )


def test_classificar_metricas_multiplas_metricas(tabela_metricas):
    """Testa classificação com múltiplas métricas."""
    resultado = classificar_metricas(
        tabela=tabela_metricas,
        metricas=['Accuracy', 'F1', 'Precision']
    )
    
    # Deve ter 3 colunas de classificação + 1 média
    cols_classificacao = [c for c in resultado.columns if c.startswith('classificacao_')]
    assert len(cols_classificacao) == 4  # 3 métricas + média


def test_classificar_metricas_nao_modifica_original(tabela_metricas):
    """Testa que tabela original não é modificada."""
    original_cols = tabela_metricas.columns.tolist()
    
    classificar_metricas(
        tabela=tabela_metricas,
        metricas=['Accuracy']
    )
    
    # Tabela original deve permanecer inalterada
    assert tabela_metricas.columns.tolist() == original_cols
