# Pipeline Unificado de Treinamento

## 🎯 Visão Geral

O pipeline de treinamento foi **refatorado** para ter uma **arquitetura unificada** que suporta tanto **classificação** quanto **regressão** através de um único código base.

## ✨ Principais Melhorias

### Antes (Duplicado)
```python
# Classificação
from src.pipelines import treinar_pipeline_completo
resultado = treinar_pipeline_completo(df, 'classe')

# Regressão - arquivo e função separados!
from src.pipelines import treinar_pipeline_completo_regressao
resultado = treinar_pipeline_completo_regressao(df, 'preco')
```

### Depois (Unificado) ✅
```python
# Classificação
from src.pipelines import treinar_pipeline_completo
resultado = treinar_pipeline_completo(
    dados=df,
    coluna_alvo='classe',
    tipo_problema='classificacao'  # <-- Único parâmetro diferente!
)

# Regressão - mesma função!
resultado = treinar_pipeline_completo(
    dados=df,
    coluna_alvo='preco',
    tipo_problema='regressao'  # <-- Único parâmetro diferente!
)
```

## 📁 Arquitetura

### Novos Arquivos Criados

```
src/
├── pipelines/
│   └── pipeline_treinamento_unified.py  # Pipeline unificado principal
│
├── treinamento/
│   ├── configuracao/
│   │   └── criar_experimento.py        # Factory unificado
│   │
│   └── treino/
│       ├── treinar_modelo_base_unified.py
│       ├── otimizar_modelo_unified.py
│       └── finalizar_modelo_unified.py
│
exemplos/
└── exemplo_pipeline_unificado.py        # Exemplos de uso
```

### Arquivos Legados Mantidos

Os arquivos antigos **foram mantidos** para **retrocompatibilidade**:
- `pipeline_treinamento.py` (classificação)
- `criar_experimento_classificacao.py`
- `treinar_modelo_base.py`
- etc.

## 🚀 Como Usar

### 1. Classificação Completa

```python
from src.pipelines import treinar_pipeline_completo

resultado = treinar_pipeline_completo(
    dados=df_treino,
    coluna_alvo='classe_target',
    tipo_problema='classificacao',
    n_modelos_comparar=3,
    metrica_ordenacao='Accuracy',  # Padrão automático
    otimizar_hiperparametros=True,
    n_iter_otimizacao=20,
    finalizar=True,
    salvar_modelo_final=True,
    nome_modelo='modelo_clf_v1'
)

print(resultado['metricas_melhor'])
print(resultado['tabela_comparacao'])
```

### 2. Regressão Completa

```python
from src.pipelines import treinar_pipeline_completo

resultado = treinar_pipeline_completo(
    dados=df_treino,
    coluna_alvo='preco',
    tipo_problema='regressao',
    n_modelos_comparar=3,
    metrica_ordenacao='R2',  # Padrão automático
    otimizar_hiperparametros=True,
    n_iter_otimizacao=20,
    finalizar=True,
    salvar_modelo_final=True,
    nome_modelo='modelo_reg_v1'
)
```

### 3. Treinamento Rápido

```python
from src.pipelines import treinar_rapido

# Classificação rápida
exp, modelo = treinar_rapido(
    dados=df,
    coluna_alvo='classe',
    tipo_problema='classificacao',
    modelo='rf'  # ou 'auto'
)

# Regressão rápida
exp, modelo = treinar_rapido(
    dados=df,
    coluna_alvo='preco',
    tipo_problema='regressao',
    modelo='auto'
)
```

### 4. Modelos Específicos

```python
resultado = treinar_pipeline_completo(
    dados=df,
    coluna_alvo='target',
    tipo_problema='regressao',
    modelos_incluir=['rf', 'xgboost', 'lightgbm'],  # Apenas estes
    n_modelos_comparar=1,
    metrica_ordenacao='RMSE'
)
```

## 📊 Métricas Automáticas

O pipeline **seleciona automaticamente** as métricas corretas:

### Classificação
- Accuracy (padrão)
- AUC
- Recall
- Precision
- F1
- Kappa
- MCC

### Regressão
- R2 (padrão)
- MAE
- MSE
- RMSE
- RMSLE
- MAPE

## 🔧 Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `dados` | DataFrame | Dados de treinamento | **Obrigatório** |
| `coluna_alvo` | str | Nome da coluna target | **Obrigatório** |
| `tipo_problema` | str | 'classificacao' ou 'regressao' | **Obrigatório** |
| `params_setup` | dict | Parâmetros PyCaret.setup() | None |
| `n_modelos_comparar` | int | Quantos modelos selecionar | 3 |
| `modelos_incluir` | list | IDs de modelos para incluir | None (todos) |
| `modelos_excluir` | list | IDs de modelos para excluir | None |
| `metrica_ordenacao` | str | Métrica para ordenar | Auto |
| `otimizar_hiperparametros` | bool | Se deve otimizar | True |
| `n_iter_otimizacao` | int | Iterações de otimização | 10 |
| `finalizar` | bool | Se treina em dataset completo | True |
| `salvar_modelo_final` | bool | Se salva em disco | True |
| `nome_modelo` | str | Nome do arquivo | 'modelo_final' |
| `pasta_modelos` | str | Pasta de destino | 'modelos' |

## 🎁 Benefícios

1. ✅ **DRY** - Don't Repeat Yourself (sem duplicação de código)
2. ✅ **Manutenção** - Correções em um único lugar
3. ✅ **Consistência** - Mesma API para ambos os tipos
4. ✅ **Flexibilidade** - Fácil adicionar novos tipos (clustering, etc)
5. ✅ **Type Safety** - Validação de tipo embutida
6. ✅ **Retrocompatibilidade** - Código antigo continua funcionando

## 🔄 Migração

### Código Antigo (ainda funciona)
```python
# Classificação - ainda funciona!
from src.pipelines.pipeline_treinamento import treinar_pipeline_completo
resultado = treinar_pipeline_completo(df, 'classe')
```

### Código Novo (recomendado)
```python
# Use o pipeline unificado
from src.pipelines import treinar_pipeline_completo
resultado = treinar_pipeline_completo(
    dados=df,
    coluna_alvo='classe',
    tipo_problema='classificacao'
)
```

## 📝 Exemplos Completos

Veja o arquivo [`exemplos/exemplo_pipeline_unificado.py`](../exemplos/exemplo_pipeline_unificado.py) para exemplos completos de:
- Classificação completa
- Regressão completa
- Treinamento rápido
- Modelos específicos
- Diferentes métricas
- E muito mais!

## 🧪 Testando

```python
# Teste rápido
import pandas as pd
from src.pipelines import treinar_rapido

df = pd.read_csv('dados.csv')

# Classificação
exp_clf, modelo_clf = treinar_rapido(df, 'classe', 'classificacao', 'rf')

# Regressão
exp_reg, modelo_reg = treinar_rapido(df, 'valor', 'regressao', 'rf')

print("✓ Tudo funcionando!")
```

## 🐛 Troubleshooting

### Erro: "tipo_problema deve ser 'classificacao' ou 'regressao'"
**Solução:** Verifique o spelling. Use exatamente: `'classificacao'` ou `'regressao'`

### Erro: Import não encontrado
**Solução:** Certifique-se de importar de `src.pipelines`:
```python
from src.pipelines import treinar_pipeline_completo
```

### Métricas incorretas
**Solução:** As métricas são selecionadas automaticamente. Para customizar:
```python
metrica_ordenacao='F1'  # Para classificação
metrica_ordenacao='MAE'  # Para regressão
```

## 📚 Referências

- Arquivo principal: [`src/pipelines/pipeline_treinamento_unified.py`](../src/pipelines/pipeline_treinamento_unified.py)
- Factory: [`src/treinamento/configuracao/criar_experimento.py`](../src/treinamento/configuracao/criar_experimento.py)
- Exemplos: [`exemplos/exemplo_pipeline_unificado.py`](../exemplos/exemplo_pipeline_unificado.py)
