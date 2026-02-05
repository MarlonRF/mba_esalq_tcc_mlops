# Módulo de Treinamento - Guia de Uso

## Estrutura Modular

```
src/treinamento/
├── __init__.py                 # Interface pública
├── constantes.py              # Constantes e configurações
├── logger_config.py           # Configuração de logging
│
├── configuracao/              # Configuração de experimentos
│   ├── criar_experimento_classificacao.py
│   └── configurar_parametros.py  ⭐ NOVO
│
├── treino/                    # Funções de treinamento
│   ├── treinar_modelo_base.py
│   ├── otimizar_modelo.py
│   ├── finalizar_modelo.py
│   └── treinar_pipeline_completo.py  ⭐ NOVO
│
├── avaliacao/                 # Avaliação e métricas
│   ├── avaliar_modelo.py
│   ├── classificar_metricas.py
│   └── fazer_predicoes.py
│
├── persistencia/              # Salvar/carregar modelos
│   ├── salvar_modelo.py
│   └── carregar_modelo.py
│
├── visualizacao/              # Plots e gráficos
│   └── salvar_plots_modelo.py
│
└── utils/                     # Utilitários
    ├── extrair_estimador.py
    ├── extrair_info_modelo.py
    └── extrair_importancia_features.py
```

## 🚀 Início Rápido

### 1. Treinamento Simples (Auto)

```python
from src.treinamento import treinar_rapido
import pandas as pd

# Carrega dados
df = pd.read_csv('dados.csv')

# Treina automaticamente o melhor modelo (rápido!)
exp, modelo = treinar_rapido(df, coluna_alvo='classe')

# Faz predições
predicoes = exp.predict_model(modelo, data=df_teste)
```

### 2. Pipeline Completo (Recomendado)

```python
from src.treinamento import treinar_pipeline_completo

# Executa pipeline completo: compare → tune → finalize → save
resultado = treinar_pipeline_completo(
    dados=df_treino,
    coluna_alvo='target',
    n_modelos_comparar=5,          # Compara top 5 modelos
    otimizar_hiperparametros=True, # Otimiza o melhor
    n_iter_otimizacao=20,          # 20 iterações de tunagem
    finalizar=True,                # Treina em dataset completo
    salvar_modelo_final=True,      # Salva em disco
    nome_modelo='modelo_v1',
)

# Acessa componentes
modelo_final = resultado['melhor_modelo']
metricas = resultado['metricas_melhor']
tabela = resultado['tabela_comparacao']
caminho = resultado['caminho_modelo']

print(f"Acurácia: {metricas['Accuracy']:.4f}")
print(f"Modelo salvo em: {caminho}")
```

### 3. Configuração Personalizada

```python
from src.treinamento import (
    configurar_parametros,
    criar_experimento_classificacao,
    treinar_modelo_base,
    otimizar_modelo,
)

# Configura parâmetros customizados
params = configurar_parametros(
    fold=10,
    normalize=True,
    remove_outliers=True,
    pca=True,
    pca_components=15,
    session_id=42,
)

# Cria experimento
exp = criar_experimento_classificacao(
    dados=df,
    coluna_alvo='classe',
    params=params
)

# Treina modelos específicos
modelos, tabela = treinar_modelo_base(
    exp=exp,
    n_select=3,
    include=['rf', 'xgboost', 'lightgbm'],  # Apenas estes modelos
    sort='F1'  # Ordena por F1-score
)

# Otimiza o melhor
melhor = modelos[0]
otimizado, metricas_opt = otimizar_modelo(
    exp=exp,
    modelo=melhor,
    n_iter=30,
    optimize='AUC'  # Otimiza para AUC
)
```

### 4. Presets Rápidos

```python
from src.treinamento import parametros_rapidos

# Preset "fast" - para desenvolvimento/protótipo
params_fast = parametros_rapidos("fast")
# fold=2, sem outliers, rápido

# Preset "thorough" - para análise completa
params_thorough = parametros_rapidos("thorough")
# fold=10, remove outliers, detalhado

# Preset "production" - para produção
params_prod = parametros_rapidos("production")
# fold=5, sem verbose, com logging

# Usa no experimento
exp = criar_experimento_classificacao(
    dados=df,
    coluna_alvo='target',
    params=params_prod
)
```

## 🎯 Casos de Uso Comuns

### Treinamento para Produção

```python
from src.treinamento import treinar_pipeline_completo, parametros_rapidos

# Usa preset de produção
params = parametros_rapidos("production")

resultado = treinar_pipeline_completo(
    dados=df_treino,
    coluna_alvo='sensacao_termica',
    params_setup=params,
    n_modelos_comparar=5,
    modelos_incluir=['rf', 'xgboost', 'lightgbm', 'catboost'],
    otimizar_hiperparametros=True,
    n_iter_otimizacao=50,  # Mais iterações = melhor resultado
    finalizar=True,
    salvar_modelo_final=True,
    nome_modelo='conforto_termico_v1',
    pasta_modelos='modelos_producao',
)

# Modelo pronto para deploy
modelo = resultado['melhor_modelo']
caminho = resultado['caminho_modelo']
```

### Comparação de Modelos Específicos

```python
resultado = treinar_pipeline_completo(
    dados=df,
    coluna_alvo='target',
    modelos_incluir=['rf', 'lr', 'dt', 'et', 'gbm'],
    n_modelos_comparar=5,  # Compara todos os 5
    otimizar_hiperparametros=False,  # Sem otimização (mais rápido)
    finalizar=False,
)

# Visualiza comparação
print(resultado['tabela_comparacao'])
print(resultado['tabela_classificada'])  # Classificação por múltiplas métricas
```

### Experimento Rápido com GPU

```python
params = configurar_parametros(
    use_gpu=True,
    fold=3,
    normalize=True,
)

resultado = treinar_pipeline_completo(
    dados=df_grande,
    coluna_alvo='classe',
    params_setup=params,
    modelos_incluir=['xgboost', 'lightgbm', 'catboost'],  # Modelos com suporte GPU
    n_modelos_comparar=3,
    otimizar_hiperparametros=True,
)
```

## 🔧 Funções Utilitárias

### Extrair Informações do Modelo

```python
from src.treinamento import extrair_info_modelo, extrair_estimador

# Extrai metadados
info = extrair_info_modelo(modelo)
print(info['modelo_nome'])       # Ex: 'RandomForestClassifier'
print(info['parametros'])        # Hiperparâmetros
print(info['classes'])           # Classes do problema
print(info['n_features'])        # Número de features

# Acessa estimador sklearn subjacente
estimador = extrair_estimador(modelo)
probabilidades = estimador.predict_proba(X_test)
```

### Importância de Features

```python
from src.treinamento import extrair_importancia_features

# Extrai importâncias (treina RF internamente)
resultado_imp = extrair_importancia_features(
    dados=df_treino,
    coluna_alvo='target',
    atributos=['feat1', 'feat2', 'feat3'],
    n_top_features=10,  # Top 10 mais importantes
)

df_importancias = resultado_imp['importancias']
top_features = resultado_imp['top_features']

print(df_importancias.head(10))
```

### Classificar Modelos por Múltiplas Métricas

```python
from src.treinamento import classificar_metricas

# Tabela de comparação do PyCaret
tabela = resultado['tabela_comparacao']

# Classifica por múltiplas métricas
metricas_importantes = ['Accuracy', 'F1', 'AUC', 'Recall']
tabela_classificada = classificar_metricas(tabela, metricas_importantes)

# Modelo com melhor classificação média
melhor_geral = tabela_classificada.iloc[0]
print(f"Melhor modelo geral: {melhor_geral.name}")
print(f"Classificação média: {melhor_geral['classificacao_media']:.2f}")
```

## 📊 Avaliação e Métricas

### Avaliar Modelo em Dados de Teste

```python
from src.treinamento import avaliar_modelo

resultado_aval = avaliar_modelo(
    exp=exp,
    modelo=modelo_final,
    dados_teste=df_teste,
    coluna_alvo='classe',
    average='weighted',  # Para multiclasse
)

# Acessa métricas
print("Métricas:")
print(f"  Accuracy: {resultado_aval['metricas']['accuracy']:.4f}")
print(f"  Precision: {resultado_aval['metricas']['precision']:.4f}")
print(f"  Recall: {resultado_aval['metricas']['recall']:.4f}")
print(f"  F1-Score: {resultado_aval['metricas']['f1_score']:.4f}")

# Relatório detalhado
print("\nRelatório de Classificação:")
print(resultado_aval['relatorio'])

# Matriz de confusão
matriz = resultado_aval['matriz_confusao']
print("\nMatriz de Confusão:")
print(matriz)

# DataFrame com predições
predicoes_df = resultado_aval['predicoes']
```

### Fazer Predições

```python
from src.treinamento import fazer_predicoes

# Faz predições em novos dados
predicoes = fazer_predicoes(
    exp=exp,
    modelo=modelo,
    dados=df_novos,
    raw_score=True,  # Inclui probabilidades
)

# Acessa colunas de predição
labels = predicoes['prediction_label']
scores = predicoes['prediction_score']
```

## 💾 Salvar e Carregar Modelos

```python
from src.treinamento import salvar_modelo, carregar_modelo

# Salva modelo
caminho = salvar_modelo(
    exp=exp,
    modelo=modelo_final,
    nome_modelo='meu_modelo',
    pasta_destino='modelos_salvos',
)
# Salva em: modelos_salvos/meu_modelo.pkl

# Carrega modelo
modelo_carregado = carregar_modelo('modelos_salvos/meu_modelo')

# Usa normalmente
predicoes = exp.predict_model(modelo_carregado, data=df_teste)
```

## 📈 Visualizações

```python
from src.treinamento import salvar_plots_modelo

# Gera e salva múltiplos plots
plots_desejados = [
    'auc',
    'confusion_matrix',
    'pr',
    'feature',
    'learning',
]

resultado_plots = salvar_plots_modelo(
    exp=exp,
    modelos=[modelo_otimizado],
    plots=plots_desejados,
    pasta='plots_modelo',
    scale=2.0,  # Maior resolução
    add_prefix=True,  # Adiciona nome do modelo ao arquivo
)

# Acessa caminhos dos plots salvos
for modelo_nome, plots_dict in resultado_plots.items():
    print(f"Plots para {modelo_nome}:")
    for plot_tipo, caminho in plots_dict.items():
        print(f"  {plot_tipo}: {caminho}")
```

## 🔍 Dicas e Boas Práticas

### 1. Reprodutibilidade

```python
# Sempre use session_id fixo para reproduzir resultados
params = configurar_parametros(session_id=42)
```

### 2. Validação Robusta

```python
# Use mais folds para datasets menores
params = configurar_parametros(fold=10)  # Mais robusto

# Use menos folds para datasets grandes (mais rápido)
params = configurar_parametros(fold=3)
```

### 3. Otimização Eficiente

```python
# Comece com poucas iterações para teste
resultado = treinar_pipeline_completo(
    dados=df,
    coluna_alvo='target',
    n_iter_otimizacao=10,  # Teste rápido
)

# Depois aumente para produção
resultado = treinar_pipeline_completo(
    dados=df,
    coluna_alvo='target',
    n_iter_otimizacao=50,  # Produção
)
```

### 4. Logging e Debugging

```python
from src.treinamento import logger

# Ajusta nível de log se necessário
import logging
logger.setLevel(logging.DEBUG)  # Mais detalhes

# Ou menos verbose
logger.setLevel(logging.WARNING)  # Apenas avisos/erros
```

## 🧪 Exemplos de Integração

### Com ClearML

```python
from src.pipelines.pipeline_treinamento_v2 import pipeline_treinamento_clearml

resultado = pipeline_treinamento_clearml(
    dados=df,
    coluna_alvo='classe',
    nome_projeto='ConfortoTermico',
    nome_tarefa='Experimento_RF_v1',
    tags=['producao', 'v1.0'],
    n_modelos_comparar=5,
    otimizar=True,
)

# Acessa task e modelo ClearML
task_id = resultado['clearml_task_id']
model_id = resultado['clearml_model_id']
```

### Com Pipelines de Dados

```python
from src.pipelines import executar_pipeline_processamento, executar_pipeline_features
from src.treinamento import treinar_pipeline_completo

# 1. Processa dados brutos
df_proc = executar_pipeline_processamento(df_raw)

# 2. Cria features
df_feat, artefatos = executar_pipeline_features(df_proc)

# 3. Treina modelo
resultado = treinar_pipeline_completo(
    dados=df_feat,
    coluna_alvo='target',
    otimizar_hiperparametros=True,
)
```

## 📚 Referências

- [Documentação PyCaret](https://pycaret.org/)
- [API Reference - Classification](https://pycaret.readthedocs.io/en/stable/api/classification.html)
- [ClearML Integration](https://clear.ml/docs/)
