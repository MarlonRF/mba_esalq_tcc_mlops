# Resumo da Sessão de Refatoração do Projeto MLOps

## Contexto Geral
Esta sessão focou na **refatoração completa** do projeto de conforto térmico, transformando um código monolítico em uma arquitetura modular e testável, seguindo as melhores práticas de MLOps.

## Objetivo Principal
Modularizar todas as funções do projeto, separando cada função em seu próprio arquivo, organizando por módulos temáticos e criando testes unitários para cada uma.
A pasta de teste deve refletir essa estrutura de src, com um arquivo teste para cada função/arquivo.
---

## Modificações Realizadas

### 1. Estrutura de Diretórios Criada

```
src/
├── processamento/
│   ├── limpeza/
│   │   ├── remover_duplicados.py
│   │   ├── substituir_valores.py
│   │   ├── remover_linhas_nulas.py
│   │   └── __init__.py
│   ├── imputacao/
│   │   ├── imputar_numericos.py
│   │   ├── imputar_categoricos.py
│   │   └── __init__.py
│   ├── temporal/
│   │   ├── criar_datetime.py
│   │   ├── agrupar_mes_ano.py
│   │   └── __init__.py
│   ├── codificacao/
│   │   ├── codificar_label.py
│   │   ├── aplicar_codificacao_rotulos.py
│   │   ├── aplicar_dummy.py
│   │   └── __init__.py
│   └── __init__.py
│
├── features/
│   ├── criacao_features/
│   │   ├── calcular_valor_imc.py
│   │   ├── imc_classe.py
│   │   ├── calcular_heat_index.py
│   │   ├── calcular_dew_point.py
│   │   ├── calcular_t_x_u.py
│   │   ├── adicionar_features_derivadas.py
│   │   └── __init__.py
│   ├── normalizacao/
│   │   ├── pick_scaler.py
│   │   ├── normalizar.py
│   │   └── __init__.py
│   ├── codificacao/
│   │   ├── codificar_label.py
│   │   ├── aplicar_codificacao_rotulos.py
│   │   ├── aplicar_dummy.py
│   │   └── __init__.py
│   └── __init__.py
│
├── treinamento_ml/ # Ainda pensando na melhor divisão
│   ├── ...
│   └── __init__.py
│
├── utils/
│   ├── io/
│   │   ├── io_local.py
│   │   ├── io_clearml.py
│   │   └── __init__.py
│   ├── dados_sinteticos/
│   │   ├── fatiar_dataframe.py
│   │   ├── gerar_bootstrap_df.py
│   │   ├── gerar_amostras_bootstrap_cumulativas.py
│   │   └── __init__.py
│   └── __init__.py
│
├── pipelines/
│   ├── pipeline_processamento.py
│   ├── pipeline_features.py
│   ├── pipeline_completo.py
│   └── __init__.py
│
├── config_projeto/
│   ├── config.py
│   └── __init__.py
│
tests/
├── unit/
│   ├── processamento/
│   │   ├── limpeza/
│   │   ├── imputacao/
│   │   ├── temporal/
│   │   └── codificacao/
│   ├── features/
│   │   ├── criacao_features/
│   │   ├── normalizacao/
│   │   └── codificacao/
│   └── treinamento/
├── integration/
│   ├── test_pipeline_processamento.py
│   ├── test_pipeline_features.py
│   └── test_pipeline_completo.py
└── conftest.py
```

---

### 2. Pipelines Criados

#### **Pipeline de Processamento** (`pipeline_processamento.py`)
Executa:
1. Limpeza de dados (remoção de duplicados, substituição de valores, remoção de nulos)
2. Conversão de tipos de dados
3. Criação de colunas datetime
4. Imputação de valores (numéricos e categóricos) com suporte a configuração personalizada por coluna
5. Agrupamento temporal (opcional)

**Principais parâmetros:**
- `config_imputacao_customizada`: Dict com método de imputação específico por coluna carregado de config_projeto/config.py
- `criar_agrupamento_temporal`: Boolean para criar coluna de agrupamento
- `nome_coluna_agrupamento`: Nome da coluna de agrupamento temporal

#### **Pipeline de Features** (`pipeline_features.py`)
Executa:
1. Criação de features derivadas (IMC, heat index, dew point, etc.)
2. Codificação de variáveis categóricas (label ou one-hot)
3. Normalização de dados numéricos (com suporte a normalização por grupo e por coluna)

**Principais parâmetros:**
- `aplicar_codificacao`: Boolean
- `metodo_codificacao`: 'label' ou 'onehot'
- `criar_features_derivadas`: Boolean
- `tipos_features_derivadas`: Lista de features a criar
- `aplicar_normalizacao`: Boolean
- `metodo_normalizacao`: 'standard', 'minmax', ou 'robust'
- `config_normalizacao_customizada`: Dict com método de normalização específico por coluna ( estes estão em config_gerais)
- `agrupamento_normalizacao`: Nome da coluna para normalização por grupo

#### **Pipeline de Treinamento** (`pipeline_features.py`)



#### **Pipeline Completo** (`pipeline_completo.py`)
Executa processamento + features + treinamento em uma única chamada.

---

### 3. Configurações Centralizadas (`config.py`)

Todos os dicionários, listas e constantes foram movidos para `config/config_custom.py`:

```python
# Substituições na limpeza
SUBSTITUICOES_LIMPEZA = {99: 0, 'x': 0, 'F': 'f'}

# Colunas
COLUNA_DATA = 'data'
COLUNA_HORA = 'hora'
COLUNAS_CATEGORICAS = ['sexo', 'vestimenta']
COLUNAS_FLOAT = ['altura', 'tev', 'utci', 'sst', ...]
COLUNAS_INT = ['idade', 'peso', 'p1', 'p2', ...]

# Configuração de imputação personalizada
CONFIG_IMPUTACAO_CUSTOMIZADA = {
    'altura': 'median',
    'peso': 'median',
    'tev': 'mean',
    'ur': 'forward_fill',
    'sexo': 'mode',
    'vestimenta': 'constant:desconhecido',
}

# Mapeamentos de features derivadas
MAPA_SENSACAO_TERMICA = {
    (-99, -40): 'Extremamente frio',
    (-40, -10): 'Muito frio',
    ...
}

# Agrupamento para normalização
AGRUPAMENTO_NORMALIZAR = 'mes-ano'
```

---

### 4. Funcionalidades Implementadas

#### **Imputação Personalizada**
- Suporte a diferentes métodos por coluna via dicionário
- Métodos disponíveis: 'mean', 'median', 'mode', 'forward_fill', 'backward_fill', 'constant:valor'
- Fallback para métodos padrão se não especificado

#### **Normalização Flexível**
- Normalização global ou por grupos (ex: mes-ano)
- Normalização personalizada por coluna
- Suporte a múltiplos scalers: StandardScaler, MinMaxScaler, RobustScaler
- Retorna artefatos (scalers) para uso posterior

#### **Features Derivadas**
- IMC e classificação de IMC
- Heat Index
- Dew Point
- Temperatura × Umidade
- Sistema extensível para adicionar novas features

#### **I/O Robusto**
- `load_dataframe()`: Carrega CSV/Excel com detecção automática de delimitadores
- Suporte para caminhos absolutos e relativos
- Tratamento de erros de encoding

---

### 5. Testes Unitários

Estrutura criada para testes espelhando a estrutura de `src/`:
- Um arquivo de teste para cada função
- Fixtures em `conftest.py` para dados de teste reutilizáveis
- Testes de integração para pipelines completos
- Script de verificação de cobertura criado

**Arquivos de teste criados:**
- `tests/unit/processamento/limpeza/test_*.py`
- `tests/unit/processamento/imputacao/test_*.py`
- `tests/unit/features/criacao_features/test_*.py`
- `tests/unit/features/normalizacao/test_*.py`
- `tests/integration/test_pipeline_*.py`

---

### 6. Correções e Ajustes Realizados

1. **Imports corrigidos** em todos os módulos
2. **Estrutura de pastas limpa** (removidas subpastas desnecessárias)
3. **Arquivos `.old` deletados** do repositório
4. **Git worktrees removidas** para evitar confusão
5. **`__init__.py` atualizados** em todos os módulos com exports corretos
6. **Lazy loading** implementado em `pipelines/__init__.py` para otimização

---

### 7. Como Usar os Pipelines

```python
from src.pipelines import (
    executar_pipeline_processamento,
    executar_pipeline_features
)
from src.config_projeto import config
from src.utils.io import load_dataframe

# 1. Carregar dados
df = load_dataframe('../dados/arquivo.csv')

# 2. Processamento
df_proc = executar_pipeline_processamento(
    df,
    config_imputacao_customizada=config.CONFIG_IMPUTACAO_CUSTOMIZADA,
    criar_agrupamento_temporal=True,
    nome_coluna_agrupamento='mes-ano'
)

# 3. Features
df_feat, artefatos = executar_pipeline_features(
    df_proc,
    aplicar_codificacao=True,
    metodo_codificacao='label',
    criar_features_derivadas=True,
    tipos_features_derivadas=['imc', 'heat_index', 'dew_point'],
    aplicar_normalizacao=True,
    metodo_normalizacao='standard',
    agrupamento_normalizacao='mes-ano'
)
```

---

## Arquivos Principais Modificados

1. **`src/pipelines/pipeline_processamento.py`** - Pipeline de processamento completo
2. **`src/pipelines/pipeline_features.py`** - Pipeline de features
3. **`src/config_projeto/config.py`** - Configurações centralizadas
4. **`src/utils/io/io_local.py`** - Funções de I/O robustas
5. **`src/processamento/__init__.py`** - Exports do módulo de processamento
6. **`src/features/__init__.py`** - Exports do módulo de features

---

## Próximos Passos Sugeridos

1. **Completar testes unitários** para todas as funções
2. **Executar testes com pytest** e verificar cobertura
3. **Criar pipeline de treinamento** modular
4. **Documentar** funções com docstrings detalhadas
5. **Integrar com ClearML** para tracking de experimentos
6. **Criar CI/CD pipeline** para testes automáticos

---

## Problemas Resolvidos

1. ✅ Estrutura modular implementada
2. ✅ Imports corrigidos em todos os módulos
3. ✅ Configurações centralizadas
4. ✅ Pipelines funcionando com dados reais
5. ✅ Git worktrees removidas
6. ✅ Arquivos duplicados/antigos limpos
7. ✅ Testes unitários estruturados

---

## Comandos Úteis

```bash
# Executar todos os testes
pytest tests/ -v

# Executar testes com cobertura
pytest tests/ --cov=src --cov-report=html

# Executar apenas testes unitários
pytest tests/unit/ -v

# Executar apenas testes de integração
pytest tests/integration/ -v
```

---

**Data da sessão:** 27/01/2026 - 02/02/2026
**Status:** ✅ Refatoração completa finalizada, pronto para próxima fase (testes e treinamento)
