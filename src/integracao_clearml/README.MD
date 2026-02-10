# Módulo ClearML - Integração MLOps

Módulo completo para rastreamento de experimentos, versionamento de datasets e execução de pipelines com ClearML.

## 📁 Estrutura de Arquivos

```
src/integracao_clearml/
├── __init__.py                          # Exports principais do módulo
├── decorators.py                        # Decorators customizados (@pipeline, @component)
├── task_manager.py                      # Gerenciamento de tasks ClearML
├── dataset_manager.py                   # Gerenciamento de datasets versionados
├── registrar_modelo_clearml.py          # Registro standalone de modelos
├── pipeline_completo_decorators.py      # ⭐ Pipeline completo com @PipelineDecorator
└── README.md                            # Esta documentação
```

## 🎯 Arquivo Principal

### **pipeline_completo_decorators.py** (636 linhas)

Pipeline MLOps completo usando decorators oficiais do ClearML:
- `@PipelineDecorator.pipeline` - Pipeline orquestrado
- `@PipelineDecorator.component` - Componentes individuais (5 componentes)

**Componentes:**
1. `component_upload_dados_brutos` - Upload de dados brutos como Dataset
2. `component_pipeline_processamento` - Processamento e limpeza
3. `component_pipeline_features` - Engenharia de features
4. `component_pipeline_treinamento` - Treinamento e comparação de modelos
5. `component_registrar_modelo` - Registro do modelo com metadados

**Características:**
- ✅ Cria projeto automaticamente no ClearML
- ✅ 3 datasets versionados (bruto → processado → features)
- ✅ 5 tasks separadas (rastreáveis)
- ✅ Métrica principal (R²) para decisão de modelo vigente
- ✅ Artefatos completos (tabelas, gráficos, encoders, scalers)
- ✅ Execução local ou remota

**Uso:**
```python
from src.integracao_clearml.pipeline_completo_decorators import executar_pipeline

resultado = executar_pipeline(
    caminho_csv='dados/arquivo.csv',
    run_locally=True  # True = local, False = remoto
)
```

## 🔧 Módulos Utilitários

### **decorators.py**
Decorators customizados e utilitários:
- `@pipeline` / `@component` - Wrappers simplificados
- `log_metric()`, `log_artifact()` - Logging
- `ClearMLContext` - Context manager

### **task_manager.py**
Gerenciamento de tasks:
- `criar_task()` - Criar nova task
- `buscar_task_por_nome()` - Buscar task existente
- `registrar_metrica()` - Logar métricas
- `registrar_artefato()` - Upload de artefatos

### **dataset_manager.py**
Gerenciamento de datasets:
- `criar_dataset()` - Novo dataset
- `upload_dataset()` - Upload de arquivos
- `baixar_dataset()` - Download de dataset
- `criar_dataset_incremental()` - Versionamento

### **registrar_modelo_clearml.py**
Função standalone para registro de modelos no ClearML com metadados completos.

## 🚀 Uso Rápido

### 1. Pipeline Completo (Recomendado)

```python
from src.integracao_clearml.pipeline_completo_decorators import executar_pipeline

# Executar pipeline completo (local)
resultado = executar_pipeline(
    caminho_csv='dados/arquivo.csv',
    run_locally=True
)

# Resultado contém:
# - resultado['projeto']
# - resultado['datasets']['bruto']
# - resultado['datasets']['processado']
# - resultado['datasets']['features']
# - resultado['modelo']['id']
# - resultado['modelo']['nome']
# - resultado['modelo']['valor']  # Métrica principal (R²)
```

### 2. Criar Task Manual

```python
from src.integracao_clearml import criar_task, registrar_metrica

task = criar_task(
    project_name="meu_projeto",
    task_name="experimento_01",
    task_type="training"
)

registrar_metrica(task, "accuracy", 0.95, series="treino")
task.close()
```

### 3. Gerenciar Datasets

```python
from src.integracao_clearml import criar_e_publicar_dataset

dataset_id = criar_e_publicar_dataset(
    dataset_name="dados_v1",
    project_name="meu_projeto",
    arquivos=["dados/arquivo.csv"],
    tags=["treinamento", "v1"]
)
```

## 📊 Comparação de Abordagens

| Característica | Pipeline Completo (Decorators) | Utilitários Manuais |
|---------------|--------------------------------|---------------------|
| **Uso** | Pipeline end-to-end automático | Controle granular |
| **Datasets** | 3 versionados automaticamente | Manual |
| **Tasks** | 5 tasks criadas automaticamente | 1 task manual |
| **Componentes** | 5 componentes rastreáveis | Código customizado |
| **Execução** | Local ou remota (fila) | Local apenas |
| **Ideal para** | Produção, reprodutibilidade | Experimentos rápidos |

## 🎓 Exemplo Completo

```python
# ===================================================================
# PIPELINE COMPLETO - TODAS AS ETAPAS RASTREADAS
# ===================================================================
import sys
sys.path.append('..')

from src.integracao_clearml.pipeline_completo_decorators import executar_pipeline

# Executar pipeline
resultado = executar_pipeline(
    caminho_csv='dados/thermal_confort.csv',
    run_locally=True
)

# Acessar recursos criados
print(f"Projeto: {resultado['projeto']}")
print(f"Dataset bruto: {resultado['datasets']['bruto']}")
print(f"Modelo: {resultado['modelo']['nome']}")
print(f"R²: {resultado['modelo']['valor']:.4f}")

# Visualizar no ClearML UI:
# - http://localhost:8080 (local)
# - https://app.clear.ml (demo)
```

## 📌 Métrica Principal

O pipeline usa **R²** como métrica principal para decisão de modelo vigente.

**Configurar métrica (no arquivo pipeline_completo_decorators.py):**
```python
METRICA_PRINCIPAL = "R2"  # Para regressão
# ou
METRICA_PRINCIPAL = "Accuracy"  # Para classificação
```

## 🗑️ Arquivos Removidos (Limpeza Realizada)

Os seguintes arquivos foram removidos por serem redundantes ou deprecados:

1. ❌ `clearml_project.py` - Deprecado (funcionalidade em task_manager/dataset_manager)
2. ❌ `pipeline_processamento_clearml.py` - Substituído por pipeline_completo_decorators.py
3. ❌ `pipeline_treinamento_clearml.py` - Substituído por pipeline_completo_decorators.py
4. ❌ `pipeline_completo_clearml.py` - Substituído por pipeline_completo_decorators.py

**Resultado:** Estrutura mais limpa e focada no arquivo principal `pipeline_completo_decorators.py`.

## 📚 Documentação Adicional

- **ClearML Docs**: https://clear.ml/docs
- **PipelineDecorator**: https://clear.ml/docs/latest/docs/pipelines/pipelines
- **Configuração**: `config/config_clearml.py`

## ✅ Status

- ✅ Módulo limpo e organizado (7 arquivos)
- ✅ Pipeline principal com decorators oficiais
- ✅ Utilitários para uso manual
- ✅ Documentação completa
- ✅ Pronto para produção
