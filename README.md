# TCC ClearML - Sistema de Pipeline de Conforto Térmico

Projeto completo de pipeline de machine learning para análise de conforto térmico usando PyCaret e ClearML. O sistema implementa processamento de dados, treinamento de modelos e versionamento de datasets com rastreabilidade completa.

✅ Sistema em produção no Google Cloud Platform com CI/CD automatizado
🔧 Permissões IAM configuradas para Container Registry gcr.io/streamlit-388123/conforto-api
📦 Docker Registry: gcr.io/streamlit-388123/conforto-api

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Configuração ClearML](#configuração-clearml)
- [Como Usar](#como-usar)
- [Pipelines Disponíveis](#pipelines-disponíveis)
- [API REST](#api-rest)
- [Configurações](#configurações)
- [Exemplos de Uso](#exemplos-de-uso)
- [Troubleshooting](#troubleshooting)
- [Contribuição](#contribuição)

## 🎯 Visão Geral

Este projeto implementa um sistema completo de machine learning para análise de dados de conforto térmico, com as seguintes características:

- **Pipeline de Processamento**: Limpeza, transformação e feature engineering automatizados
- **Pipeline de Treinamento**: Comparação automática de modelos com PyCaret
- **Versionamento de Datasets**: Controle de versão usando ClearML
- **API REST**: Endpoint para predições em tempo real
- **Geração de Dados Sintéticos**: Bootstrap cumulativo para testes
- **Rastreabilidade Completa**: Tracking de experimentos e métricas

## ✨ Funcionalidades

### 🔄 Pipeline de Processamento
- Limpeza automática de dados (valores ausentes, outliers)
- Conversão de tipos de dados
- Criação de features derivadas (IMC, Heat Index, Dew Point)
- Normalização e codificação de variáveis categóricas
- Imputação inteligente de valores faltantes
- Validação de integridade dos dados

### 🤖 Pipeline de Treinamento
- Comparação automática de múltiplos algoritmos
- Otimização de hiperparâmetros
- Validação cruzada estratificada
- Geração automática de gráficos e métricas
- Registro de modelos no ClearML
- Criação automática de API para predições

### 📊 Análise e Visualização
- Relatórios detalhados de performance
- Gráficos de importância de features
- Curvas ROC, Precision-Recall e Calibração
- Matriz de confusão e métricas detalhadas
- Dashboard interativo no ClearML

### 🌐 API REST
- Endpoint `/predict` para predições em tempo real
- Validação automática de entrada
- Documentação automática com FastAPI
- Modelo carregado em memória para alta performance

## 📁 Estrutura do Projeto (atual)

```
.
├── src/
│   ├── api/                # FastAPI + modelo
│   │   └── Dockerfile      # Build apenas da API
│   └── funcoes/            # Núcleo de processamento/treino (ClearML/PyCaret)
├── tests/                  # Unit e integration
├── documentacao/           # Guias e docs
├── legacy/                 # Arquivos legados/backup
├── pyproject.toml, uv.lock, README.md, pytest.ini
└── .github/workflows/      # CI/CD
```

## 🚀 Instalação



## 🚀 Instalação

### Pré-requisitos
- Python 3.11 (PyCaret 3.3.2 não suporta 3.12+)
- Git
- [uv](https://github.com/astral-sh/uv) instalado (recomendado)

### Instalação com uv (recomendado)

```bash
# Clone o repositório

cd tcc_clm

# Instala dependências conforme pyproject/uv.lock
uv sync

# Ativa o ambiente virtual gerenciado pelo uv
source .venv/bin/activate  # Linux/Mac
.\.venv\Scripts\Activate   # Windows PowerShell
```

### Instalação alternativa com pip

```bash
git clone https://github.com/seu-usuario/tcc_clm.git
cd tcc_clm
python -m venv .venv
source .venv/bin/activate  # ou .\.venv\Scripts\Activate no Windows
pip install -r requirements.txt  # Opcional; preferir uv
```
```
clearml>=1.11.0
pycaret>=3.0.0
pandas>=1.5.0
scikit-learn>=1.3.0
fastapi>=0.100.0
uvicorn>=0.23.0
numpy>=1.24.0
matplotlib>=3.6.0
seaborn>=0.12.0
```

## ⚙️ Configuração ClearML

### 1. Servidor ClearML

Você pode usar o servidor ClearML de duas formas:

#### Opção A: Servidor Local (Docker)
```bash
# Instalar ClearML Server com Docker
docker run -d --name clearml-server -p 8080:8080 -p 8008:8008 -p 8081:8081 allegroai/clearml-server
```

#### Opção B: ClearML Community Server (Gratuito)
1. Registre-se em [app.clear.ml](https://app.clear.ml)
2. Obtenha suas credenciais de API

### 2. Configuração de Credenciais

Crie o arquivo `credenciais.json` (este arquivo está no .gitignore):

```json
{
  "api_host": "SEU_API_HOST",
  "web_host": "SEU_WEB_HOST", 
  "files_host": "SEU_FILES_HOST",
  "access_key": "SEU_ACCESS_KEY",
  "secret_key": "SEU_SECRET_KEY"
}
```

### 3. Variáveis de Ambiente

Crie o arquivo `.env` na raiz do projeto:

```env
# ClearML Configuration
CLEARML_API_HOST=seu_api_host
CLEARML_WEB_HOST=seu_web_host
CLEARML_FILES_HOST=seu_files_host
CLEARML_API_ACCESS_KEY=seu_access_key
CLEARML_API_SECRET_KEY=seu_secret_key

# Project Settings
PROJECT_NAME=conforto_termico
DATASET_PROJECT=Datasets
```

### 4. Configuração Inicial

```python
# Execute uma vez para configurar
clearml-init
# Siga as instruções na tela
```

## 📖 Como Usar

### 1. Execução Completa via Notebook

O notebook principal `exec_pipelines_completo.ipynb` contém o pipeline completo:

```bash
# Inicie o Jupyter Notebook
jupyter notebook exec_pipelines_completo.ipynb
```

Execute as células em sequência:
1. Importações e configurações
2. Carregamento de dados
3. Pipeline de processamento
4. Pipeline de treinamento
5. Avaliação e registro de resultados

### 2. Execução Programática

```python
from funcoes.io_local import load_dataframe
from funcoes.processamento import processar_df, ProcCfg
from funcoes.treinar import treinar_classificacao

# 1. Carregar dados
df = load_dataframe('dados/meus_dados.csv')

# 2. Processar dados
cfg = ProcCfg()  # Configuração padrão
df_processado, artefatos = processar_df(df, cfg)

# 3. Treinar modelo
params = {
    "data": df_processado,
    "target": "sensacao_termica",
    "session_id": 42,
    "normalize": True,
    "fold": 5,
    "use_gpu": False  # Mude para True se tiver GPU
}

exp, modelo, resultado = treinar_classificacao(params)
```

## 🔧 Pipelines Disponíveis

### Pipeline de Processamento

**Arquivo**: `pipeline_processamento.py`

**Etapas**:
1. **Limpeza Básica**: Remoção de valores inválidos
2. **Conversão de Tipos**: Aplicação do dicionário de tipos
3. **Feature Engineering**: Criação de features derivadas
4. **Imputação**: Preenchimento inteligente de valores faltantes
5. **Normalização**: Padronização de variáveis numéricas
6. **Codificação**: Transformação de variáveis categóricas
7. **Validação**: Verificação de integridade final

### Pipeline de Treinamento

**Arquivo**: `pipeline_treinamento.py`

**Modelos Testados**:
- Logistic Regression
- Random Forest
- Gradient Boosting
- Extra Trees
- AdaBoost
- Naive Bayes
- K-Neighbors
- SVM
- LightGBM
- XGBoost

## 🌐 API REST

### Inicialização da API

```bash
# Execute a API
python api.py

# Ou com uvicorn diretamente
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### Endpoints Disponíveis

#### GET `/`
Verificação de saúde da API

#### POST `/predict`
Predição de conforto térmico

**Request Body**:
```json
{
  "idade_anos": 30,
  "peso_kg": 70.5,
  "altura_cm": 175.0,
  "sexo_biologico": "m",
  "temperatura_media_c": 25.5,
  "umidade_relativa_percent": 60.0,
  "radiacao_solar_media_wm2": 200.0
}
```

**Response**:
```json
{
  "prediction": "Neutro"
}
```

### Documentação Interativa

Acesse `http://localhost:8000/docs` para documentação automática Swagger UI.

## 💡 Exemplos de Uso

### Exemplo 1: Processamento Básico

```python
from funcoes.io_local import load_dataframe
from funcoes.processamento import processar_arquivo, ProcCfg

# Configuração customizada
cfg = ProcCfg(
    criar_derivadas=True,
    normalizar=True,
    codificar=True
)

# Processar arquivo
processar_arquivo(
    path_in="dados_brutos.csv",
    path_out="dados_processados.csv",
    cfg=cfg,
    salvar_mapas_em="artefatos/"
)
```

### Exemplo 2: Treinamento Customizado

```python
from funcoes.treinar import treinar_random_forest

resultado = treinar_random_forest(
    dados=df_processado,
    coluna_alvo="sensacao_termica",
    atributos=["idade_anos", "peso_kg", "temperatura_media_c"],
    test_size=0.2,
    random_state=42,
    registrar_clearml=True,
    nome_modelo="rf_conforto_termico"
)

print(f"Acurácia: {resultado['metrics']['accuracy']:.3f}")
```

### Exemplo 3: Geração de Dados Sintéticos

```python
from funcoes.gerar_dados import gerar_amostras_bootstrap_cumulativas

# Gerar amostras bootstrap
caminhos = gerar_amostras_bootstrap_cumulativas(
    df=df_original,
    tamanhos_cumulativos=[100, 500, 1000, 2000],
    diretorio_saida="dados_sinteticos/",
    prefixo="bootstrap_conforto",
    random_state=42
)
```

## 🔍 Troubleshooting

### Problemas Comuns

#### 1. Erro de Conexão ClearML
**Problema**: `ConnectionError: Could not connect to ClearML server`

**Solução**:
- Verifique se o servidor ClearML está rodando
- Confirme as credenciais em `credenciais.json`
- Teste a conectividade de rede

#### 2. Erro de GPU no PyCaret
**Problema**: `GPU device not found, falling back to CPU`

**Solução**:
```python
# Desabilite GPU se não disponível
params["use_gpu"] = False
```

#### 3. Módulo não encontrado
**Problema**: `ModuleNotFoundError: No module named 'clearml'`

**Solução**:
```bash
# Reinstale dependências
pip install -r requirements.txt --force-reinstall
```

### Verificação de Integridade

```bash
# Teste imports
python -c "from funcoes import *; print('Imports OK')"

# Teste ClearML
python -c "from clearml import Task; print('ClearML OK')"

# Teste PyCaret  
python -c "from pycaret.classification import *; print('PyCaret OK')"
```

## 📊 Métricas e Avaliação

### Métricas Calculadas

- **Accuracy**: Precisão geral do modelo
- **AUC**: Área sob a curva ROC
- **Recall**: Taxa de verdadeiros positivos
- **Precision**: Precisão por classe
- **F1-Score**: Média harmônica precision/recall
- **Kappa**: Concordância entre predito e real
- **MCC**: Coeficiente de correlação de Matthews

### Visualizações Geradas

- Curva ROC
- Precision-Recall Curve
- Matriz de Confusão
- Feature Importance
- Learning Curves
- Calibration Plots

## 🤝 Contribuição

### Como Contribuir

1. **Fork** o repositório
2. **Clone** seu fork
3. **Crie** uma branch para sua feature: `git checkout -b feature/nova-feature`
4. **Implemente** suas mudanças
5. **Teste** thoroughly
6. **Commit** com mensagens claras: `git commit -m 'feat: adiciona nova feature'`
7. **Push** para seu fork: `git push origin feature/nova-feature`
8. **Abra** um Pull Request

### Padrões de Código

- **PEP 8**: Siga as convenções Python
- **Docstrings**: Documente todas as funções
- **Type Hints**: Use anotações de tipo
- **Logging**: Use logging ao invés de print
- **Testes**: Inclua testes para novas features

## 📝 Changelog

### v1.0.0 (2024-01-15)
- ✨ Pipeline completo de processamento implementado
- ✨ Pipeline de treinamento com PyCaret
- ✨ Integração completa com ClearML
- ✨ API REST funcional
- ✨ Geração de dados sintéticos
- 📚 Documentação completa

### Próximas Features
- 🔄 Pipeline de retreinamento automático
- 📊 Dashboard web interativo
- 🔔 Sistema de alertas e monitoramento
- 🚀 Deploy automatizado

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- [PyCaret](https://pycaret.org/) - Framework de ML
- [ClearML](https://clear.ml/) - MLOps platform
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [Pandas](https://pandas.pydata.org/) - Data manipulation

---

⭐ **Se este projeto foi útil para você, considere dar uma estrela!** ⭐

## 📧 Contato

Para dúvidas ou sugestões, abra uma [issue](https://github.com/seu-usuario/tcc_clm/issues) ou entre em contato através do GitHub.

