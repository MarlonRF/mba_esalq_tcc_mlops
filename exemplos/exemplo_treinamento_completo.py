"""
Exemplo de uso completo do módulo de treinamento modularizado.

Este script demonstra todos os níveis de abstração:
1. Treinamento rápido (treinar_rapido)
2. Pipeline completo (treinar_pipeline_completo)
3. Configuração personalizada (passo a passo)
4. Integração com ClearML
"""
import sys
from pathlib import Path

# Adiciona o diretório raiz do projeto ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
from sklearn.datasets import make_classification

# Cria dataset de exemplo
X, y = make_classification(
    n_samples=1000,
    n_features=10,
    n_informative=7,
    n_redundant=2,
    n_classes=3,
    random_state=42
)

df = pd.DataFrame(
    X, 
    columns=[f'feature_{i}' for i in range(10)]
)
df['target'] = y

print("Dataset criado:")
print(f"  Shape: {df.shape}")
print(f"  Classes: {df['target'].value_counts().to_dict()}")
print()

# ==============================================================================
# EXEMPLO 1: Treinamento Rápido (Ideal para Protótipo)
# ==============================================================================
print("="*70)
print("EXEMPLO 1: Treinamento Rápido")
print("="*70)

from src.treinamento import treinar_rapido

# Treina automaticamente o melhor modelo
exp1, modelo1 = treinar_rapido(
    dados=df,
    coluna_alvo='target',
    modelo='auto',  # Deixa PyCaret escolher
    salvar=False
)

print("\n✓ Modelo treinado rapidamente!")
print(f"  Tipo: {type(modelo1).__name__}")

# ==============================================================================
# EXEMPLO 2: Pipeline Completo (Recomendado para Produção)
# ==============================================================================
print("\n" + "="*70)
print("EXEMPLO 2: Pipeline Completo com Otimização")
print("="*70)

from src.treinamento import treinar_pipeline_completo

resultado2 = treinar_pipeline_completo(
    dados=df,
    coluna_alvo='target',
    n_modelos_comparar=3,          # Compara top 3
    modelos_incluir=['rf', 'lr', 'dt'],  # Apenas estes modelos
    otimizar_hiperparametros=True, # Otimiza o melhor
    n_iter_otimizacao=5,          # 5 iterações (rápido)
    finalizar=True,                # Treina em dataset completo
    salvar_modelo_final=True,      # Salva em disco
    nome_modelo='exemplo_modelo',
    pasta_modelos='modelos_exemplo',
)

print("\n✓ Pipeline completo executado!")
print("\nResumo:")
print(f"  Modelos comparados: {len(resultado2['modelos_base'])}")
print(f"  Melhor modelo: {resultado2['tabela_comparacao'].index[0]}")
print(f"  Accuracy: {resultado2['metricas_melhor']['Accuracy']:.4f}")
print(f"  Modelo salvo em: {resultado2['caminho_modelo']}")

print("\nTabela de Comparação (Top 3):")
print(resultado2['tabela_comparacao'][['Accuracy', 'AUC', 'Recall', 'F1']])

# ==============================================================================
# EXEMPLO 3: Configuração Personalizada (Máximo Controle)
# ==============================================================================
print("\n" + "="*70)
print("EXEMPLO 3: Configuração Personalizada")
print("="*70)

from src.treinamento import (
    configurar_parametros,
    parametros_rapidos,
    criar_experimento_classificacao,
    treinar_modelo_base,
    otimizar_modelo,
    finalizar_modelo,
    avaliar_modelo,
)

# Opção 3A: Usar preset
print("\n3A: Usando preset 'thorough' (análise completa):")
params_thorough = parametros_rapidos("thorough")
print(f"  Folds: {params_thorough['fold']}")
print(f"  Remove outliers: {params_thorough['remove_outliers']}")

# Opção 3B: Configuração customizada
print("\n3B: Configuração customizada:")
params_custom = configurar_parametros(
    fold=5,
    normalize=True,
    remove_outliers=True,
    pca=False,
    session_id=123,
)
print(f"  Parâmetros: {list(params_custom.keys())}")

# Cria experimento com parâmetros customizados
exp3 = criar_experimento_classificacao(
    dados=df,
    coluna_alvo='target',
    params=params_custom
)

print("\n✓ Experimento configurado")

# Treina modelos específicos
modelos3, tabela3 = treinar_modelo_base(
    exp=exp3,
    n_select=2,
    include=['rf', 'dt'],
    sort='Accuracy'
)

print(f"✓ {len(modelos3)} modelos treinados")
print(f"  Melhor: {tabela3.index[0]} (Acc: {tabela3['Accuracy'].iloc[0]:.4f})")

# Otimiza o melhor
print("\nOtimizando hiperparâmetros...")
modelo_otim, metricas_otim = otimizar_modelo(
    exp=exp3,
    modelo=modelos3[0],
    n_iter=5,
    optimize='Accuracy'
)

print(f"✓ Otimização concluída")
print(f"  Accuracy após otimização: {metricas_otim['Accuracy'].iloc[0]:.4f}")

# Finaliza modelo
print("\nFinalizando modelo (treino completo)...")
modelo_final = finalizar_modelo(exp3, modelo_otim)
print("✓ Modelo finalizado")

# Avalia modelo
print("\nAvaliando modelo...")
resultado_aval = avaliar_modelo(
    exp=exp3,
    modelo=modelo_final,
    dados_teste=df,  # Normalmente seria df_teste
    coluna_alvo='target',
)

print("✓ Avaliação concluída")
print(f"  Accuracy: {resultado_aval['metricas']['accuracy']:.4f}")
print(f"  Precision: {resultado_aval['metricas']['precision']:.4f}")
print(f"  Recall: {resultado_aval['metricas']['recall']:.4f}")
print(f"  F1-Score: {resultado_aval['metricas']['f1_score']:.4f}")

# ==============================================================================
# EXEMPLO 4: Funções Utilitárias
# ==============================================================================
print("\n" + "="*70)
print("EXEMPLO 4: Funções Utilitárias")
print("="*70)

from src.treinamento import (
    extrair_info_modelo,
    extrair_estimador,
    extrair_importancia_features,
    classificar_metricas,
)

# Extrai informações do modelo
print("\n4A: Informações do Modelo:")
info = extrair_info_modelo(modelo_final)
print(f"  Nome: {info['modelo_nome']}")
print(f"  Classes: {info['classes']}")
print(f"  Número de features: {info['n_features']}")

# Extrai estimador sklearn
estimador = extrair_estimador(modelo_final)
print(f"\n4B: Estimador sklearn extraído: {type(estimador).__name__}")

# Importância de features
print("\n4C: Importância de Features (Top 5):")
resultado_imp = extrair_importancia_features(
    dados=df,
    coluna_alvo='target',
    n_top_features=5,
)
print(resultado_imp['importancias'].head())

# Classifica modelos por múltiplas métricas
print("\n4D: Classificação por Múltiplas Métricas:")
tabela_class = classificar_metricas(
    tabela3,
    ['Accuracy', 'AUC', 'Recall', 'F1']
)
print(tabela_class[['Accuracy', 'classificacao_Accuracy', 'classificacao_media']])

# ==============================================================================
# EXEMPLO 5: Salvamento e Carregamento
# ==============================================================================
print("\n" + "="*70)
print("EXEMPLO 5: Salvamento e Carregamento")
print("="*70)

from src.treinamento import salvar_modelo, carregar_modelo

# Salva modelo
caminho = salvar_modelo(
    exp=exp3,
    modelo=modelo_final,
    nome_modelo='modelo_exemplo_final',
    pasta_destino='modelos_exemplo',
)
print(f"✓ Modelo salvo em: {caminho}")

# Carrega modelo
modelo_carregado = carregar_modelo(caminho)
print(f"✓ Modelo carregado: {type(modelo_carregado).__name__}")

# Faz predições com modelo carregado
predicoes = exp3.predict_model(modelo_carregado, data=df.head(5))
print("\nPredições (primeiras 5 linhas):")
print(predicoes[['target', 'prediction_label', 'prediction_score']].head())

# ==============================================================================
# RESUMO FINAL
# ==============================================================================
print("\n" + "="*70)
print("RESUMO DOS EXEMPLOS")
print("="*70)

print("""
1. Treinamento Rápido (treinar_rapido):
   ✓ Ideal para: Protótipos, testes rápidos
   ✓ Tempo: ~30 segundos
   ✓ Controle: Baixo (automático)

2. Pipeline Completo (treinar_pipeline_completo):
   ✓ Ideal para: Produção, experimentos sérios
   ✓ Tempo: ~2-5 minutos
   ✓ Controle: Médio (configurável)
   ✓ Inclui: Compare → Tune → Finalize → Save

3. Configuração Personalizada:
   ✓ Ideal para: Máximo controle, pesquisa
   ✓ Tempo: Variável
   ✓ Controle: Alto (passo a passo)

4. Funções Utilitárias:
   ✓ Extrair info, importâncias, classificar métricas

5. Persistência:
   ✓ Salvar e carregar modelos em formato PyCaret

Todos os exemplos funcionam e são intercambiáveis!
""")

print("\n✅ Exemplos concluídos com sucesso!")
