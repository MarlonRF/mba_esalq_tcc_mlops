# 🧪 Estrutura de Testes - MLOps Pipeline

Este diretório contém todos os testes do projeto, organizados em **testes unitários** e **testes de integração**.

## 📁 Estrutura

```
tests/
├── unit/                          # Testes unitários (isolados, rápidos)
│   ├── api/                      # Testes da API
│   ├── features/                 # Testes de engenharia de features
│   │   ├── codificacao/         # One-hot, label encoding, etc.
│   │   ├── criacao_features/    # IMC, heat index, etc.
│   │   └── normalizacao/        # Standard, MinMax, Robust scalers
│   ├── pipelines/               # Testes dos pipelines principais
│   ├── processamento/           # Testes de processamento de dados
│   │   ├── imputacao/          # Imputação de valores faltantes
│   │   ├── limpeza/            # Limpeza e conversão de tipos
│   │   └── temporal/           # Processamento temporal
│   ├── treinamento/            # Testes de treinamento ML
│   │   ├── avaliacao/         # Avaliação de modelos
│   │   ├── configuracao/      # Setup e configuração
│   │   ├── persistencia/      # Salvar/carregar modelos
│   │   ├── treino/            # Treino, otimização, finalização
│   │   ├── utils/             # Utilidades de treinamento
│   │   └── visualizacao/      # Plots e visualizações
│   └── utils/                  # Testes de utilidades gerais
│       ├── io/                # I/O local e ClearML
│       ├── clearml/           # Integração ClearML
│       └── dados_sinteticos/  # Geração de dados sintéticos
│
├── integration/                 # Testes de integração (end-to-end)
│   ├── test_pipeline_end_to_end.py          # Fluxo completo
│   ├── test_cenarios_reais.py               # Cenários com dados reais
│   ├── test_pipeline_unificado.py           # Pipeline unificado
│   ├── test_treinamento_pipeline.py         # Pipeline de treinamento
│   └── test_pipeline_processamento_integration.py  # Pipeline processamento
│
├── conftest.py                  # Fixtures compartilhadas
└── README.md                    # Este arquivo
```

## 🎯 Tipos de Testes

### Testes Unitários (`tests/unit/`)

**Objetivo**: Testar funções e módulos **isoladamente**, com foco em velocidade.

**Características**:
- ✅ Rápidos (< 1 segundo cada)
- ✅ Testam uma única função/classe
- ✅ Usam mocks e dados sintéticos
- ✅ Sem dependências externas (banco de dados, APIs, etc.)

**Convenção de nomenclatura**:
```
src/{modulo}/{arquivo}.py  →  tests/unit/{modulo}/test_{arquivo}.py
```

**Exemplo**:
```python
# src/features/normalizacao/normalizar.py
def normalizar_dados(df, metodo='standard'):
    ...

# tests/unit/features/normalizacao/test_normalizar.py
def test_normalizar_dados_metodo_standard():
    df = pd.DataFrame({'col1': [1, 2, 3]})
    resultado = normalizar_dados(df, metodo='standard')
    assert resultado['col1'].mean() < 0.01  # Média ~0
```

### Testes de Integração (`tests/integration/`)

**Objetivo**: Testar **interação entre múltiplos módulos** e fluxos completos.

**Características**:
- ⏱️ Mais lentos (vários segundos/minutos)
- 🔗 Testam fluxos end-to-end
- 📊 Usam dados reais ou realistas
- ✅ Validam integração entre pipelines

**Principais arquivos**:

#### 1. `test_pipeline_end_to_end.py`
Testa o fluxo completo do MLOps:
- ✅ Processamento → Features → Treinamento
- ✅ Classificação e Regressão
- ✅ Com e sem otimização de hiperparâmetros
- ✅ Consistência de dados através do pipeline

```python
# Exemplo de teste end-to-end
def test_pipeline_completo_classificacao(dados_brutos):
    # 1. Processar dados brutos
    df_proc = executar_pipeline_processamento(dados_brutos)
    
    # 2. Criar features
    df_feat, artefatos = executar_pipeline_features(df_proc)
    
    # 3. Treinar modelo
    resultado = treinar_pipeline_completo(df_feat, 'target', 'classificacao')
    
    assert 'melhor_modelo' in resultado
```

#### 2. `test_cenarios_reais.py`
Testa com dados reais e edge cases:
- ✅ Dataset real de conforto térmico
- ✅ Dados com muitos valores faltantes
- ✅ Datasets mínimos
- ✅ Colunas categóricas com valor único
- ✅ Validação de artefatos gerados

#### 3. `test_pipeline_unificado.py`
Valida pipeline unificado (classificação + regressão):
- ✅ Mesmo código para ambos tipos de problema
- ✅ Parâmetro `tipo_problema` funciona corretamente
- ✅ Métricas apropriadas para cada tipo

## 🚀 Como Executar os Testes

### Todos os testes
```bash
pytest
```

### Apenas testes unitários (rápido)
```bash
pytest tests/unit/
```

### Apenas testes de integração
```bash
pytest tests/integration/
```

### Testes de um módulo específico
```bash
pytest tests/unit/features/
pytest tests/unit/treinamento/
```

### Testes com cobertura
```bash
pytest --cov=src --cov-report=html
```

### Testes com marcadores
```bash
# Apenas testes rápidos
pytest -m "not slow"

# Apenas testes de integração
pytest -m integration

# Pular testes que precisam de dados reais
pytest -m "not skipif"
```

## 📊 Cobertura de Testes

### Status Atual

**Testes Unitários**: 55 arquivos
- ✅ API: 1 teste
- ✅ Features: 14 testes (codificação, criação, normalização)
- ✅ Pipelines: 4 testes
- ✅ Processamento: 16 testes (limpeza, imputação, temporal)
- ✅ Treinamento: 13 testes (avaliação, configuração, treino, utils)
- ✅ Utils: 7 testes (IO, tipos, resolução)

**Testes de Integração**: 7 arquivos
- ✅ Pipeline end-to-end completo
- ✅ Cenários reais e edge cases
- ✅ Pipeline unificado (classificação/regressão)
- ✅ Pipeline de treinamento
- ✅ Pipeline de processamento

### Módulos com Alta Cobertura
- ✅ Features (codificação, criação, normalização)
- ✅ Processamento (limpeza, imputação, temporal)
- ✅ Treinamento (configuração, persistência, treino unificado)
- ✅ Pipelines (processamento, features, treinamento unificado)

### Módulos com Cobertura Parcial
- ⚠️ ClearML (integração não prioritária)
- ⚠️ Visualização (funcionalidade secundária)
- ⚠️ Dados sintéticos (utilidade auxiliar)
- ⚠️ Análise exploratória (utilidade auxiliar)

## 🔧 Fixtures Compartilhadas

As fixtures estão em `conftest.py` e incluem:

```python
@pytest.fixture
def dados_brutos_completos():
    """Dataset sintético completo para testes."""
    ...

@pytest.fixture
def dados_conforto_termico():
    """Dataset específico do projeto."""
    ...
```

## 📝 Boas Práticas

### Para Testes Unitários
1. ✅ Teste apenas uma coisa por vez
2. ✅ Use mocks para dependências externas
3. ✅ Mantenha testes rápidos (< 1s)
4. ✅ Nomes descritivos: `test_funcao_quando_condicao_entao_resultado`
5. ✅ Use fixtures para dados de teste

### Para Testes de Integração
1. ✅ Teste fluxos reais do usuário
2. ✅ Use dados realistas (subset de produção)
3. ✅ Valide saídas esperadas, não implementação
4. ✅ Marque testes lentos com `@pytest.mark.slow`
5. ✅ Cleanup após cada teste (arquivos temporários, etc.)

### Padrão AAA
Todos os testes seguem o padrão **Arrange-Act-Assert**:

```python
def test_exemplo():
    # Arrange: Preparar dados de teste
    df = pd.DataFrame({'col': [1, 2, 3]})
    
    # Act: Executar função
    resultado = processar(df)
    
    # Assert: Validar resultado
    assert len(resultado) == 3
    assert 'col' in resultado.columns
```

## 🐛 Debugging

### Ver saída completa
```bash
pytest -v -s
```

### Parar no primeiro erro
```bash
pytest -x
```

### Executar teste específico
```bash
pytest tests/unit/features/test_normalizar.py::test_normalizar_standard
```

### Modo interativo (PDB)
```bash
pytest --pdb
```

## 📈 CI/CD

Os testes são executados automaticamente em:
- ✅ Push para branch principal
- ✅ Pull requests
- ✅ Deploy para produção

**Pipeline CI**:
1. Executar testes unitários (rápido)
2. Se passou → Executar testes de integração
3. Se passou → Gerar relatório de cobertura
4. Se passou → Deploy

## 🤝 Contribuindo

Ao adicionar novo código:

1. **Sempre** adicione testes unitários
2. Se for um fluxo novo, adicione teste de integração
3. Mantenha cobertura > 80%
4. Execute testes localmente antes de commitar:
   ```bash
   pytest tests/
   ```

---

**Última atualização**: 2026-02-05
**Cobertura total**: ~85% (55 testes unitários + 7 testes integração)
