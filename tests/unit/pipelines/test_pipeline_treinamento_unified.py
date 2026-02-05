"""
Testes unitários para pipeline_treinamento_unified.py
"""
import pytest
from unittest.mock import MagicMock, patch
import pandas as pd


@pytest.fixture
def df_treino():
    """DataFrame de exemplo para treinamento."""
    return pd.DataFrame({
        'feature1': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'feature2': [2, 4, 6, 8, 10, 12, 14, 16, 18, 20],
        'target': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
    })


@patch('src.pipelines.pipeline_treinamento_unified.criar_experimento')
@patch('src.pipelines.pipeline_treinamento_unified.treinar_modelo_base')
@patch('src.pipelines.pipeline_treinamento_unified.otimizar_modelo')
@patch('src.pipelines.pipeline_treinamento_unified.finalizar_modelo')
@patch('src.pipelines.pipeline_treinamento_unified.salvar_modelo')
def test_treinar_pipeline_completo_classificacao(
    mock_salvar, mock_finalizar, mock_otimizar, mock_treinar, mock_criar_exp, df_treino
):
    """Testa pipeline de treinamento completo para classificação."""
    from src.pipelines.pipeline_treinamento_unified import treinar_pipeline_completo
    
    # Configura mocks
    mock_exp = MagicMock()
    mock_criar_exp.return_value = mock_exp
    
    mock_modelos = [MagicMock(), MagicMock()]
    mock_tabela = pd.DataFrame({'Model': ['lr', 'dt'], 'Accuracy': [0.85, 0.80]})
    mock_treinar.return_value = (mock_modelos, mock_tabela)
    
    mock_modelo_otimizado = MagicMock()
    mock_metricas = pd.DataFrame({'Accuracy': [0.88]})
    mock_otimizar.return_value = (mock_modelo_otimizado, mock_metricas)
    
    mock_modelo_final = MagicMock()
    mock_finalizar.return_value = mock_modelo_final
    
    mock_salvar.return_value = 'modelos/teste.pkl'
    
    # Executa pipeline
    resultado = treinar_pipeline_completo(
        dados=df_treino,
        coluna_alvo='target',
        tipo_problema='classificacao',
        n_modelos_comparar=2,
        otimizar_hiperparametros=True,
        finalizar=True,
        salvar_modelo_final=True
    )
    
    # Verifica chamadas
    mock_criar_exp.assert_called_once()
    mock_treinar.assert_called_once()
    mock_otimizar.assert_called()
    mock_finalizar.assert_called_once()
    mock_salvar.assert_called_once()
    
    # Verifica resultado
    assert 'experimento' in resultado
    assert 'modelos_base' in resultado
    assert 'tabela_comparacao' in resultado
    assert 'melhor_modelo' in resultado
    assert 'tipo_problema' in resultado
    assert resultado['tipo_problema'] == 'classificacao'


@patch('src.pipelines.pipeline_treinamento_unified.criar_experimento')
@patch('src.pipelines.pipeline_treinamento_unified.treinar_modelo_base')
def test_treinar_pipeline_completo_regressao(mock_treinar, mock_criar_exp):
    """Testa pipeline de treinamento para regressão."""
    from src.pipelines.pipeline_treinamento_unified import treinar_pipeline_completo
    
    df_regressao = pd.DataFrame({
        'feature1': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'target': [10.5, 20.3, 30.1, 40.7, 50.2, 60.8, 70.4, 80.9, 90.6, 100.1]
    })
    
    # Configura mocks
    mock_exp = MagicMock()
    mock_criar_exp.return_value = mock_exp
    
    mock_modelos = [MagicMock()]
    mock_tabela = pd.DataFrame({'Model': ['lr'], 'R2': [0.85]})
    mock_treinar.return_value = (mock_modelos, mock_tabela)
    
    # Executa pipeline sem otimização/finalização para teste rápido
    resultado = treinar_pipeline_completo(
        dados=df_regressao,
        coluna_alvo='target',
        tipo_problema='regressao',
        n_modelos_comparar=1,
        otimizar_hiperparametros=False,
        finalizar=False,
        salvar_modelo_final=False
    )
    
    # Verifica tipo de problema
    assert resultado['tipo_problema'] == 'regressao'
    assert 'experimento' in resultado


@patch('src.pipelines.pipeline_treinamento_unified.criar_experimento')
@patch('src.pipelines.pipeline_treinamento_unified.treinar_modelo_base')
def test_treinar_rapido(mock_treinar, mock_criar_exp):
    """Testa função treinar_rapido."""
    from src.pipelines.pipeline_treinamento_unified import treinar_rapido
    
    df = pd.DataFrame({
        'f1': [1, 2, 3, 4, 5],
        'target': [0, 1, 0, 1, 0]
    })
    
    # Configura mocks
    mock_exp = MagicMock()
    mock_criar_exp.return_value = mock_exp
    
    mock_modelos = [MagicMock()]
    mock_tabela = pd.DataFrame({'Model': ['lr'], 'Accuracy': [0.80]})
    mock_treinar.return_value = (mock_modelos, mock_tabela)
    
    # Executa treino rápido
    resultado = treinar_rapido(
        dados=df,
        coluna_alvo='target',
        tipo_problema='classificacao'
    )
    
    # Verifica que não otimizou nem salvou
    assert resultado['modelo_otimizado'] is None
    assert resultado['caminho_modelo'] is None
