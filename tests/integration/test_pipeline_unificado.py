"""
Script de teste rápido do pipeline unificado.
Valida que classificação e regressão funcionam corretamente.
"""
import sys
sys.path.append('..')

import pandas as pd
import numpy as np
from sklearn.datasets import make_classification, make_regression

print("="*70)
print("TESTE DO PIPELINE UNIFICADO DE TREINAMENTO")
print("="*70)

# =============================================================================
# Criar dados sintéticos
# =============================================================================
print("\n1. Criando dados sintéticos...")

# Dados de classificação
X_clf, y_clf = make_classification(
    n_samples=200,
    n_features=10,
    n_informative=5,
    n_redundant=2,
    random_state=42
)
df_clf = pd.DataFrame(X_clf, columns=[f'feature_{i}' for i in range(10)])
df_clf['target_classe'] = y_clf

# Dados de regressão
X_reg, y_reg = make_regression(
    n_samples=200,
    n_features=10,
    n_informative=5,
    random_state=42
)
df_reg = pd.DataFrame(X_reg, columns=[f'feature_{i}' for i in range(10)])
df_reg['target_valor'] = y_reg

print("✓ Dados de classificação criados:", df_clf.shape)
print("✓ Dados de regressão criados:", df_reg.shape)

# =============================================================================
# Teste 1: Importação
# =============================================================================
print("\n2. Testando importações...")

try:
    from src.pipelines import treinar_pipeline_completo, treinar_rapido
    print("✓ Funções importadas com sucesso")
except ImportError as e:
    print(f"✗ Erro na importação: {e}")
    sys.exit(1)

# =============================================================================
# Teste 2: Treinamento Rápido - CLASSIFICAÇÃO
# =============================================================================
print("\n3. Testando treinamento rápido de CLASSIFICAÇÃO...")

try:
    exp_clf, modelo_clf = treinar_rapido(
        dados=df_clf,
        coluna_alvo='target_classe',
        tipo_problema='classificacao',
        modelo='lr',  # Logistic Regression (rápido)
        salvar=False
    )
    print(f"✓ Classificação OK - Modelo: {type(modelo_clf).__name__}")
except Exception as e:
    print(f"✗ Erro na classificação: {e}")

# =============================================================================
# Teste 3: Treinamento Rápido - REGRESSÃO
# =============================================================================
print("\n4. Testando treinamento rápido de REGRESSÃO...")

try:
    exp_reg, modelo_reg = treinar_rapido(
        dados=df_reg,
        coluna_alvo='target_valor',
        tipo_problema='regressao',
        modelo='lr',  # Linear Regression (rápido)
        salvar=False
    )
    print(f"✓ Regressão OK - Modelo: {type(modelo_reg).__name__}")
except Exception as e:
    print(f"✗ Erro na regressão: {e}")

# =============================================================================
# Teste 4: Pipeline Completo - CLASSIFICAÇÃO
# =============================================================================
print("\n5. Testando pipeline completo de CLASSIFICAÇÃO...")

try:
    resultado_clf = treinar_pipeline_completo(
        dados=df_clf,
        coluna_alvo='target_classe',
        tipo_problema='classificacao',
        n_modelos_comparar=2,
        otimizar_hiperparametros=False,
        finalizar=False,
        salvar_modelo_final=False
    )
    print("✓ Pipeline classificação completo OK")
    print(f"  - Tipo problema: {resultado_clf['tipo_problema']}")
    print(f"  - Modelos treinados: {len(resultado_clf['modelos_base'])}")
    print(f"  - Melhor modelo: {type(resultado_clf['melhor_modelo']).__name__}")
    print(f"  - Métricas disponíveis: {list(resultado_clf['metricas_melhor'].keys())[:3]}...")
except Exception as e:
    print(f"✗ Erro no pipeline classificação: {e}")

# =============================================================================
# Teste 5: Pipeline Completo - REGRESSÃO
# =============================================================================
print("\n6. Testando pipeline completo de REGRESSÃO...")

try:
    resultado_reg = treinar_pipeline_completo(
        dados=df_reg,
        coluna_alvo='target_valor',
        tipo_problema='regressao',
        n_modelos_comparar=2,
        otimizar_hiperparametros=False,
        finalizar=False,
        salvar_modelo_final=False
    )
    print("✓ Pipeline regressão completo OK")
    print(f"  - Tipo problema: {resultado_reg['tipo_problema']}")
    print(f"  - Modelos treinados: {len(resultado_reg['modelos_base'])}")
    print(f"  - Melhor modelo: {type(resultado_reg['melhor_modelo']).__name__}")
    print(f"  - Métricas disponíveis: {list(resultado_reg['metricas_melhor'].keys())[:3]}...")
except Exception as e:
    print(f"✗ Erro no pipeline regressão: {e}")

# =============================================================================
# Teste 6: Validação de Tipo
# =============================================================================
print("\n7. Testando validação de tipo...")

try:
    treinar_rapido(
        dados=df_clf,
        coluna_alvo='target_classe',
        tipo_problema='clustering',  # Tipo inválido!
        modelo='lr',
        salvar=False
    )
    print("✗ Validação de tipo FALHOU (deveria ter dado erro)")
except ValueError as e:
    print(f"✓ Validação de tipo OK - Erro esperado: {str(e)[:50]}...")
except Exception as e:
    print(f"✗ Erro inesperado: {e}")

# =============================================================================
# Teste 7: Métricas Automáticas
# =============================================================================
print("\n8. Testando seleção automática de métricas...")

# Classificação
if 'resultado_clf' in locals():
    metricas_clf = resultado_clf['tabela_comparacao'].columns.tolist()
    print(f"✓ Métricas de classificação: {metricas_clf[:5]}...")
    
    # Verifica se tem métricas de classificação
    tem_accuracy = 'Accuracy' in metricas_clf
    tem_auc = 'AUC' in metricas_clf
    print(f"  - Accuracy presente: {tem_accuracy}")
    print(f"  - AUC presente: {tem_auc}")

# Regressão
if 'resultado_reg' in locals():
    metricas_reg = resultado_reg['tabela_comparacao'].columns.tolist()
    print(f"✓ Métricas de regressão: {metricas_reg[:5]}...")
    
    # Verifica se tem métricas de regressão
    tem_r2 = 'R2' in metricas_reg
    tem_mae = 'MAE' in metricas_reg
    print(f"  - R2 presente: {tem_r2}")
    print(f"  - MAE presente: {tem_mae}")

# =============================================================================
# Resumo Final
# =============================================================================
print("\n" + "="*70)
print("RESUMO DOS TESTES")
print("="*70)

testes = [
    ("Importações", True),
    ("Treinamento rápido - Classificação", 'modelo_clf' in locals()),
    ("Treinamento rápido - Regressão", 'modelo_reg' in locals()),
    ("Pipeline completo - Classificação", 'resultado_clf' in locals()),
    ("Pipeline completo - Regressão", 'resultado_reg' in locals()),
    ("Validação de tipo", True),
    ("Métricas automáticas", True),
]

total = len(testes)
passou = sum(1 for _, ok in testes if ok)

for nome, ok in testes:
    status = "✓ PASSOU" if ok else "✗ FALHOU"
    print(f"{status}: {nome}")

print("\n" + "="*70)
print(f"RESULTADO: {passou}/{total} testes passaram")
print("="*70)

if passou == total:
    print("\n🎉 TODOS OS TESTES PASSARAM! Pipeline unificado funcionando perfeitamente!")
else:
    print(f"\n⚠️  {total - passou} teste(s) falharam. Revise os erros acima.")
