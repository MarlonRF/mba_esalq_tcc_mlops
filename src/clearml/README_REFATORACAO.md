# Refatoração da Estrutura ClearML

## 📁 Nova Estrutura Modular

```
src/clearml/
├── utils/                              # Funções auxiliares modulares
│   ├── __init__.py                    # Exports principais
│   ├── verificador_clearml.py         # Verifica disponibilidade ClearML
│   ├── operacoes_task.py              # Criar e gerenciar tasks
│   ├── operacoes_dataset.py           # Criar e gerenciar datasets
│   └── integracao_artefatos.py        # Registrar artefatos (DataFrames, métricas)
│
└── pipelines_clearml/                  # Pipelines integrados com ClearML
    ├── __init__.py
    └── pipeline_processamento_clearml.py  # Pipeline de processamento
```

## 🎯 Princípios da Refatoração

### 1. **Modularização**
- Cada função auxiliar em seu próprio módulo
- Separação clara de responsabilidades
- Facilita manutenção e testes

### 2. **Nomenclatura em Português**
- Todas as funções, variáveis e módulos em português
- Consistência com domínio do projeto
- Facilita compreensão do código

### 3. **Reutilização de Pipelines Locais**
- Pipelines ClearML são wrappers
- Lógica de negócio permanece em `src/pipelines/`
- ClearML adiciona apenas rastreamento e versionamento

### 4. **Simplicidade Incremental**
- Começar simples e adicionar funcionalidades gradualmente
- Pipeline de processamento como primeiro exemplo
- Base sólida para features e treinamento

## 📦 Módulos Utils

### `verificador_clearml.py`
Verifica se ClearML está disponível e instalado.

**Funções:**
- `obter_clearml_disponivel()` - Retorna True se ClearML disponível
- `garantir_clearml_disponivel()` - Decorator para funções que usam ClearML

### `operacoes_task.py`
Operações básicas com Tasks ClearML.

**Funções:**
- `criar_task()` - Cria nova task
- `obter_task_atual()` - Retorna task em execução

### `operacoes_dataset.py`
Operações básicas com Datasets ClearML.

**Funções:**
- `criar_dataset()` - Cria novo dataset versionado
- `buscar_dataset()` - Busca dataset por nome ou ID

### `integracao_artefatos.py`
Registra artefatos no ClearML.

**Funções:**
- `registrar_dataframe()` - Registra DataFrame
- `registrar_metricas()` - Registra métricas (dict)
- `registrar_arquivo()` - Registra arquivo qualquer

## 🔄 Pipeline de Processamento

### Arquitetura

```python
executar_pipeline_processamento_clearml()
    │
    ├─> [ClearML] criar_task()
    │   └─> Rastrear configurações
    │
    ├─> [Pipeline Local] executar_pipeline_processamento()
    │   └─> src/pipelines/pipeline_processamento.py
    │       ├─> Carregar dados
    │       ├─> Limpeza
    │       ├─> Transformações
    │       └─> Retorna DataFrame
    │
    └─> [ClearML] Registrar Resultados
        ├─> registrar_dataframe()
        ├─> registrar_metricas()
        └─> criar_dataset() versionado
```

### Uso

```python
from src.clearml.pipelines_clearml import executar_pipeline_processamento_clearml

# Modo online (com ClearML)
resultado = executar_pipeline_processamento_clearml(
    caminho_csv="dados/arquivo.csv",
    offline_mode=False
)

# Modo offline (sem ClearML)
resultado = executar_pipeline_processamento_clearml(
    caminho_csv="dados/arquivo.csv",
    offline_mode=True
)

# Acessar resultados
df = resultado["dados_processados"]
shape = resultado["shape"]
dataset_id = resultado["dataset_id"]  # None se offline
```

### Execução Direta

```bash
# Com ClearML
python src/clearml/pipelines_clearml/pipeline_processamento_clearml.py

# Sem ClearML
python src/clearml/pipelines_clearml/pipeline_processamento_clearml.py --offline

# Arquivo customizado
python src/clearml/pipelines_clearml/pipeline_processamento_clearml.py dados/meu_arquivo.csv
```

## 📝 Arquivos Legados

Arquivos antigos foram renomeados com extensão `.py_old`:
- `pipeline_01_processamento.py_old` - Versão antiga do pipeline de processamento
- `pipeline_02_features.py_old` - Versão antiga do pipeline de features

**Ação recomendada:** Manter por período de transição, depois remover.

## 🎨 Pipeline de Features

### Arquitetura

```python
executar_pipeline_features_clearml()
    │
    ├─> [ClearML] criar_task()
    │   └─> Rastrear configurações e dataset pai
    │
    ├─> [Pipeline Local] executar_pipeline_features()
    │   └─> src/pipelines/pipeline_features.py
    │       ├─> Features derivadas (IMC, heat index, etc)
    │       ├─> Codificação categórica (label/onehot)
    │       ├─> Normalização (standard/minmax/robust)
    │       └─> Retorna DataFrame + artefatos
    │
    └─> [ClearML] Registrar Resultados
        ├─> registrar_dataframe()
        ├─> registrar_arquivo() para artefatos (mapeamentos)
        ├─> registrar_metricas()
        └─> criar_dataset() versionado com parent_id
```

### Uso

```python
from src.clearml.pipelines_clearml import executar_pipeline_features_clearml

# Modo online (com ClearML)
resultado = executar_pipeline_features_clearml(
    df_processado=df,
    dataset_processado_id="abc123",  # ID do dataset anterior
    offline_mode=False,
    criar_features_derivadas=True,
    aplicar_codificacao=True,
    aplicar_normalizacao=True
)

# Modo offline (sem ClearML)
resultado = executar_pipeline_features_clearml(
    df_processado=df,
    offline_mode=True
)

# Acessar resultados
df_features = resultado["dados_features"]
artefatos = resultado["artefatos"]  # Mapeamentos, colunas criadas
dataset_id = resultado["dataset_id"]  # None se offline
```

### Execução Direta

```bash
# Com ClearML
python src/clearml/pipelines_clearml/pipeline_features_clearml.py

# Sem ClearML
python src/clearml/pipelines_clearml/pipeline_features_clearml.py --offline
```

## 🚀 Próximos Passos

1. **Pipeline de Features** ✅ **CONCLUÍDO**
   - `pipeline_features_clearml.py` ✅
   - Reutiliza `src/pipelines/pipeline_features.py` ✅
   - Registra features derivadas, encoders e mapeamentos ✅

2. **Pipeline de Treinamento** 📋 Planejado
   - `pipeline_treinamento_clearml.py`
   - Reutilizar `src/pipelines/pipeline_treinamento.py`
   - Registrar modelos e métricas

3. **Pipeline Completo** 📋 Planejado
   - Orquestrar os 3 pipelines
   - Usar PipelineDecorator para componentes
   - Versionamento automático entre etapas

## 💡 Benefícios

✅ **Manutenibilidade**: Cada função em seu próprio arquivo  
✅ **Testabilidade**: Módulos independentes fáceis de testar  
✅ **Clareza**: Nomenclatura em português consistente  
✅ **Flexibilidade**: Modo online/offline configurável  
✅ **Reutilização**: Lógica de negócio separada de rastreamento  
✅ **Escalabilidade**: Base sólida para adicionar mais pipelines  

## 📖 Referências

- **Configurações**: `config/config_custom.py`, `config/config_clearml.py`
- **Pipeline Local**: `src/pipelines/pipeline_processamento.py`
- **Documentação ClearML**: https://clear.ml/docs
