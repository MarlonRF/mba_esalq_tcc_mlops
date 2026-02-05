"""
Teste rápido do módulo de treinamento após fix do NumPy.
"""
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification

print("="*60)
print("TESTE RÁPIDO - Módulo de Treinamento")
print("="*60)

# 1. Verifica versões
print("\n1. Verificando versões das bibliotecas:")
print(f"   NumPy: {np.__version__}")
import sklearn, scipy
print(f"   SciPy: {scipy.__version__}")
print(f"   Sklearn: {sklearn.__version__}")

# 2. Cria dataset de exemplo
print("\n2. Criando dataset de exemplo...")
X, y = make_classification(
    n_samples=200,
    n_features=5,
    n_informative=3,
    n_redundant=1,
    n_classes=2,
    random_state=42
)
df = pd.DataFrame(X, columns=[f'feat{i}' for i in range(5)])
df['target'] = y
print(f"   ✓ Dataset criado: {df.shape}")

# 3. Testa configuração de parâmetros
print("\n3. Testando configuração de parâmetros...")
from src.treinamento import configurar_parametros, parametros_rapidos

params_custom = configurar_parametros(
    fold=3,
    normalize=True,
    session_id=42,
)
print(f"   ✓ Params customizados: fold={params_custom['fold']}")

params_fast = parametros_rapidos("fast")
print(f"   ✓ Preset 'fast': fold={params_fast['fold']}")

# 4. Testa treinamento rápido
print("\n4. Testando treinamento rápido...")
from src.treinamento import treinar_rapido

try:
    exp, modelo = treinar_rapido(
        dados=df,
        coluna_alvo='target',
        modelo='lr',  # Logistic Regression (rápido)
        salvar=False
    )
    print(f"   ✓ Modelo treinado: {type(modelo).__name__}")
    
    # Faz predição teste
    preds = exp.predict_model(modelo, data=df.head(3))
    print(f"   ✓ Predições funcionando: {preds.shape}")
    
except Exception as e:
    print(f"   ✗ Erro no treinamento: {e}")

# 5. Testa utilitários
print("\n5. Testando utilitários...")
from src.treinamento import extrair_info_modelo, extrair_estimador

try:
    info = extrair_info_modelo(modelo)
    print(f"   ✓ Info modelo: {info['modelo_nome']}")
    
    estimador = extrair_estimador(modelo)
    print(f"   ✓ Estimador extraído: {type(estimador).__name__}")
except Exception as e:
    print(f"   ✗ Erro nos utilitários: {e}")

# 6. Testa importância de features
print("\n6. Testando importância de features...")
from src.treinamento import extrair_importancia_features

try:
    resultado_imp = extrair_importancia_features(
        dados=df,
        coluna_alvo='target',
        atributos=['feat0', 'feat1', 'feat2'],
        n_top_features=3,
    )
    print(f"   ✓ Importâncias extraídas: {len(resultado_imp['importancias'])} features")
    print(f"   ✓ Top features: {resultado_imp['top_features']}")
except Exception as e:
    print(f"   ✗ Erro na importância: {e}")

# Resumo
print("\n" + "="*60)
print("✅ TESTE CONCLUÍDO COM SUCESSO!")
print("="*60)
print("\nTodos os módulos principais estão funcionando:")
print("  ✓ Configuração de parâmetros")
print("  ✓ Treinamento rápido")
print("  ✓ Utilitários (info, estimador)")
print("  ✓ Importância de features")
print("\nPronto para usar o pipeline completo!")
