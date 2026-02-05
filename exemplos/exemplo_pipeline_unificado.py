"""
Exemplos de uso do pipeline unificado de treinamento.
Demonstra como usar o mesmo pipeline para classificação e regressão.
"""
import sys
sys.path.append('..')

import pandas as pd
from src.pipelines import treinar_pipeline_completo, treinar_rapido

# =============================================================================
# EXEMPLO 1: CLASSIFICAÇÃO - Pipeline Completo
# =============================================================================
print("="*70)
print("EXEMPLO 1: Treinamento Completo de CLASSIFICAÇÃO")
print("="*70)

# Carregar dados de classificação
df_classificacao = pd.read_csv('../dados/resultados/dados_processados_novas_features.csv')

# Treinar com pipeline completo
resultado_clf = treinar_pipeline_completo(
    dados=df_classificacao,
    coluna_alvo='classe_conforto',  # ou sua coluna target
    tipo_problema='classificacao',  # <-- Define tipo
    n_modelos_comparar=3,
    metrica_ordenacao='Accuracy',   # Padrão para classificação
    otimizar_hiperparametros=True,
    n_iter_otimizacao=10,
    finalizar=True,
    salvar_modelo_final=True,
    nome_modelo='modelo_classificacao_v1',
    pasta_modelos='../modelos'
)

print("\n✓ Melhor modelo de classificação:", resultado_clf['melhor_modelo'])
print("✓ Métricas:", resultado_clf['metricas_melhor'])
print("✓ Tabela de comparação:")
print(resultado_clf['tabela_comparacao'])


# =============================================================================
# EXEMPLO 2: REGRESSÃO - Pipeline Completo
# =============================================================================
print("\n" + "="*70)
print("EXEMPLO 2: Treinamento Completo de REGRESSÃO")
print("="*70)

# Carregar dados de regressão (mesmo arquivo, mas target diferente)
df_regressao = pd.read_csv('../dados/resultados/dados_processados_novas_features.csv')

# Treinar com pipeline completo
resultado_reg = treinar_pipeline_completo(
    dados=df_regressao,
    coluna_alvo='tmedia',  # Variável contínua
    tipo_problema='regressao',  # <-- Define tipo
    n_modelos_comparar=3,
    metrica_ordenacao='R2',  # Padrão para regressão
    otimizar_hiperparametros=True,
    n_iter_otimizacao=10,
    finalizar=True,
    salvar_modelo_final=True,
    nome_modelo='modelo_regressao_v1',
    pasta_modelos='../modelos'
)

print("\n✓ Melhor modelo de regressão:", resultado_reg['melhor_modelo'])
print("✓ Métricas:", resultado_reg['metricas_melhor'])
print("✓ Tabela de comparação:")
print(resultado_reg['tabela_comparacao'])


# =============================================================================
# EXEMPLO 3: Treinamento Rápido - CLASSIFICAÇÃO
# =============================================================================
print("\n" + "="*70)
print("EXEMPLO 3: Treinamento Rápido de CLASSIFICAÇÃO")
print("="*70)

exp_clf, modelo_clf = treinar_rapido(
    dados=df_classificacao,
    coluna_alvo='classe_conforto',
    tipo_problema='classificacao',
    modelo='rf',  # Random Forest
    salvar=False
)

print("✓ Modelo rápido treinado:", modelo_clf)


# =============================================================================
# EXEMPLO 4: Treinamento Rápido - REGRESSÃO
# =============================================================================
print("\n" + "="*70)
print("EXEMPLO 4: Treinamento Rápido de REGRESSÃO")
print("="*70)

exp_reg, modelo_reg = treinar_rapido(
    dados=df_regressao,
    coluna_alvo='tmedia',
    tipo_problema='regressao',
    modelo='auto',  # Deixa PyCaret escolher
    salvar=False
)

print("✓ Modelo rápido treinado:", modelo_reg)


# =============================================================================
# EXEMPLO 5: Customizando Modelos Específicos
# =============================================================================
print("\n" + "="*70)
print("EXEMPLO 5: Treinamento com Modelos Específicos")
print("="*70)

# Treinar apenas Random Forest, XGBoost e LightGBM para regressão
resultado_custom = treinar_pipeline_completo(
    dados=df_regressao,
    coluna_alvo='tmedia',
    tipo_problema='regressao',
    modelos_incluir=['rf', 'xgboost', 'lightgbm'],  # Apenas estes modelos
    n_modelos_comparar=1,  # Seleciona apenas o melhor
    metrica_ordenacao='RMSE',  # Ordena por RMSE
    otimizar_hiperparametros=False,
    finalizar=False,
    salvar_modelo_final=False
)

print("✓ Melhor modelo customizado:", resultado_custom['melhor_modelo'])
print("✓ Tabela de comparação:")
print(resultado_custom['tabela_comparacao'])


# =============================================================================
# EXEMPLO 6: Diferentes Métricas de Ordenação
# =============================================================================
print("\n" + "="*70)
print("EXEMPLO 6: Ordenação por Diferentes Métricas")
print("="*70)

# Classificação ordenada por F1
resultado_f1 = treinar_pipeline_completo(
    dados=df_classificacao,
    coluna_alvo='classe_conforto',
    tipo_problema='classificacao',
    n_modelos_comparar=1,
    metrica_ordenacao='F1',  # <-- Ordena por F1
    otimizar_hiperparametros=False,
    finalizar=False,
    salvar_modelo_final=False
)

print("✓ Melhor modelo por F1:", resultado_f1['melhor_modelo'])

# Regressão ordenada por MAE
resultado_mae = treinar_pipeline_completo(
    dados=df_regressao,
    coluna_alvo='tmedia',
    tipo_problema='regressao',
    n_modelos_comparar=1,
    metrica_ordenacao='MAE',  # <-- Ordena por MAE
    otimizar_hiperparametros=False,
    finalizar=False,
    salvar_modelo_final=False
)

print("✓ Melhor modelo por MAE:", resultado_mae['melhor_modelo'])


# =============================================================================
# VANTAGENS DO PIPELINE UNIFICADO
# =============================================================================
print("\n" + "="*70)
print("VANTAGENS DO PIPELINE UNIFICADO")
print("="*70)
print("""
1. ✓ Um único código para classificação e regressão
2. ✓ Mesma interface/API para ambos os tipos
3. ✓ Facilita manutenção (sem duplicação de código)
4. ✓ Troca de tipo é trivial (apenas 1 parâmetro)
5. ✓ Métricas padrão selecionadas automaticamente
6. ✓ Validação de tipo embutida
7. ✓ Extensível para outros tipos (ex: clustering)
""")

print("\nTIPO DE PROBLEMA:")
print(f"  Classificação: tipo_problema='classificacao'")
print(f"  Regressão:     tipo_problema='regressao'")

print("\nMÉTRICAS PADRÃO:")
print("  Classificação: Accuracy, AUC, Recall, Prec., F1, Kappa, MCC")
print("  Regressão:     MAE, MSE, RMSE, R2, RMSLE, MAPE")
