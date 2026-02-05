"""
Demonstração rápida do módulo de treinamento - versão simplificada
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from sklearn.datasets import make_classification
import warnings
warnings.filterwarnings('ignore')

# Criar dataset
print("=" * 70)
print("DEMONSTRAÇÃO MÓDULO DE TREINAMENTO")
print("=" * 70)
print()

X, y = make_classification(
    n_samples=500, n_features=8, n_informative=6,
    n_classes=2, random_state=42
)
df = pd.DataFrame(X, columns=[f'f{i}' for i in range(8)])
df['target'] = y

print(f"✓ Dataset: {df.shape} - {df['target'].value_counts().to_dict()}")
print()

# ==============================================================================
# 1. Treinamento Rápido
# ==============================================================================
print("1️⃣  TREINAMENTO RÁPIDO")
print("-" * 70)

from src.treinamento import treinar_rapido

exp, modelo = treinar_rapido(
    dados=df,
    coluna_alvo='target',
    modelo='lr',  # Logistic Regression
    salvar=False
)

print(f"✓ Modelo treinado: {type(modelo).__name__}")
print(f"✓ Experimento configurado com sucesso")
print()

# ==============================================================================
# 2. Utilitários
# ==============================================================================
print("2️⃣  UTILITÁRIOS")
print("-" * 70)

from src.treinamento import (
    extrair_info_modelo,
    extrair_estimador,
    extrair_importancia_features
)

# Info do modelo
info = extrair_info_modelo(modelo)
print(f"✓ Tipo: {info['modelo_nome']}")
print(f"✓ Parâmetros: {len(info['params'])} configurações")

# Estimador sklearn
estimador = extrair_estimador(modelo)
print(f"✓ Estimador extraído: {type(estimador).__name__}")

# Importância de features
importancias = extrair_importancia_features(df, 'target')
print(f"✓ Top 3 features:")
for feat in importancias['Feature'][:3].values:
    print(f"   - {feat}")
print()

# ==============================================================================
# 3. Configuração Personalizada
# ==============================================================================
print("3️⃣  CONFIGURAÇÃO PERSONALIZADA")
print("-" * 70)

from src.treinamento import configurar_parametros, parametros_rapidos

# Criar config customizada
config = configurar_parametros(
    fold=3,
    normalize=True,
    feature_selection=True
)
print(f"✓ Config criada: {len(config)} parâmetros")

# Usar preset
config_fast = parametros_rapidos('fast')
print(f"✓ Preset 'fast': fold={config_fast['fold']}, n_select={config_fast['n_select']}")
print()

# ==============================================================================
# Resumo Final
# ==============================================================================
print("=" * 70)
print("✅ DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
print("=" * 70)
print()
print("Módulos disponíveis:")
print("  • treinar_rapido() - Treinamento em 1 linha")
print("  • treinar_pipeline_completo() - Pipeline completo")
print("  • configurar_parametros() - Configs customizadas")
print("  • extrair_info_modelo() - Info detalhada")
print("  • extrair_estimador() - Estimador sklearn")
print("  • extrair_importancia_features() - Feature importance")
print()
