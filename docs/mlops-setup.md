# Guia de Configuração MLOps - Conforto Térmico

Este documento descreve como configurar e usar o sistema de MLOps implementado para o projeto de análise de conforto térmico.

## 🏗️ Arquitetura MLOps

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GitHub Repo   │    │  GitHub Actions  │    │   Google Cloud  │
│                 │──▶│                   │───▶│     Run         │
│ • Código        │    │ • Testes         │    │ • API Deploy    │
│ • Testes        │    │ • Build          │    │ • Auto-scale    │
│ • Workflows     │    │ • Deploy         │    │ • Health Check  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       ▼                       │
         │              ┌──────────────────┐             │
         │              │    ClearML       │             │
         └─────────────▶│                  │◀────────────┘
                        │ • Experiment     │
                        │   Tracking       │
                        │ • Model Registry │
                        │ • Data Versioning│
                        └──────────────────┘
```

## 🧪 Sistema de Testes

### Estrutura dos Testes

```
tests/
├── unit/                   # Testes unitários (rápidos)
│   ├── test_processamento_utils.py
│   └── test_api.py
├── integration/            # Testes de integração (lentos)
│   └── test_pipeline_processamento.py
├── conftest.py            # Fixtures compartilhadas
└── __init__.py
```

### Tipos de Testes

1. **Testes Unitários** (`pytest -m unit`)
   - Funções de cálculo (IMC, índice de calor, etc.)
   - Conversões de dados
   - Validações individuais
   - **Tempo**: < 5 segundos

2. **Testes de Integração** (`pytest -m integration`) 
   - Pipeline completo de processamento
   - Integração entre módulos
   - **Tempo**: < 30 segundos

3. **Testes de API** (`pytest -m api`)
   - Endpoints FastAPI
   - Validação de entrada/saída
   - **Tempo**: < 10 segundos

### Executando Testes Localmente

```bash
# Todos os testes
python -m pytest

# Apenas testes unitários (rápidos)
python -m pytest -m unit

# Testes com cobertura
python -m pytest --cov=funcoes --cov=api

# Testes específicos
python -m pytest tests/unit/test_processamento_utils.py -v
```

## 🚀 Pipeline CI/CD

### Workflow de CI (`.github/workflows/ci.yml`)

**Triggers:**
- Push para `main` ou `develop`
- Pull Requests

**Jobs:**
1. **Testes Unitários**
   - Instala dependências
   - Executa testes rápidos
   - Gera relatório de cobertura

2. **Testes de Integração**
   - Executa após testes unitários
   - Testes mais complexos
   - Validação end-to-end

3. **Qualidade de Código**
   - Formatação (Black)
   - Imports (isort)
   - Análise estática (flake8)

4. **Segurança**
   - Análise com Bandit
   - Vulnerabilidades de dependências

### Workflow de CD (`.github/workflows/deploy.yml`)

**Triggers:**
- Push para `main` (deploy automático)
- Dispatch manual (com seleção de ambiente)

**Proteções:**
- ✅ Todos os testes devem passar
- ✅ Build Docker deve ser bem-sucedido
- ✅ Health check pós-deploy
- 🔄 Rollback automático em falha

## ⚙️ Configuração do Ambiente

### 1. Secrets do GitHub

Configure os seguintes secrets no repositório:

```yaml
# Google Cloud Platform
GCP_PROJECT_ID: "seu-projeto-gcp"
GCP_SA_KEY: "chave-da-conta-de-servico"

# ClearML (opcional)
CLEARML_API_ACCESS_KEY: "sua-chave-clearml"
CLEARML_API_SECRET_KEY: "sua-chave-secreta-clearml"
CLEARML_API_HOST: "https://app.clear.ml"
```

### 2. Configuração Local

```bash
# Instalar dependências de desenvolvimento
pip install -r requirements-test.txt

# Configurar pre-commit hooks
pip install pre-commit
pre-commit install

# Configurar ClearML (opcional)
clearml-init
```

### 3. Variáveis de Ambiente

Crie arquivo `.env` (não commitar):

```env
# Desenvolvimento
ENVIRONMENT=development
DEBUG=true

# ClearML (opcional)
CLEARML_API_ACCESS_KEY=sua_chave
CLEARML_API_SECRET_KEY=sua_chave_secreta
CLEARML_API_HOST=https://app.clear.ml
```

## 🎯 Fluxo de Desenvolvimento

### 1. Desenvolvimento de Features

```bash
# 1. Criar branch da feature
git checkout -b feature/nova-funcionalidade

# 2. Desenvolver código
# ... fazer alterações ...

# 3. Executar testes localmente
python -m pytest -x  # Para no primeiro erro

# 4. Verificar qualidade
black .
isort .
flake8 .

# 5. Commit e push
git add .
git commit -m "feat: adicionar nova funcionalidade"
git push origin feature/nova-funcionalidade

# 6. Criar Pull Request
# - Testes automatizados serão executados
# - Code review necessário
# - Merge após aprovação
```

### 2. Processo de Deploy

```bash
# Deploy automático após merge para main:
git checkout main
git merge feature/nova-funcionalidade
git push origin main
# → GitHub Actions executa testes + deploy

# Deploy manual (emergência):
# → Ir no GitHub Actions
# → "Run workflow" no deploy.yml
# → Escolher ambiente (staging/production)
```

### 3. Monitoramento e Rollback

```bash
# Verificar saúde do serviço
curl https://conforto-termico-api-204511535856.us-central1.run.app/

# Logs do Cloud Run
gcloud logs read --service=conforto-termico-api --region=us-central1

# Rollback manual (se necessário)
gcloud run services update-traffic conforto-termico-api \\
  --to-revisions=PREVIOUS=100 \\
  --platform managed \\
  --region us-central1
```

## 📊 Integração com ClearML

### Tracking de Experimentos

```python
# Exemplo de uso no código
from funcoes.treinar import treinar_modelo_com_tracking

# Automaticamente logga:
# - Hiperparâmetros
# - Métricas de performance
# - Artefatos (modelo, gráficos)
# - Dados de entrada/saída

resultado = treinar_modelo_com_tracking(
    dados=df,
    parametros=config,
    nome_experimento="conforto_termico_v1.0"
)
```

### Versionamento de Dados

```python
# Upload de dataset
from funcoes.io_clearml import upload_dataset

dataset_id = upload_dataset(
    dataframe=df_processado,
    nome="dados_conforto_termico_processados",
    versao="1.0",
    tags=["processado", "limpo", "features_derivadas"]
)

# Download de dataset
df = download_dataset(dataset_id)
```

## 🔧 Resolução de Problemas

### Testes Falhando

```bash
# Ver detalhes do erro
python -m pytest -vvv --tb=long

# Executar teste específico
python -m pytest tests/unit/test_processamento_utils.py::TestIMC -v

# Debug interativo
python -m pytest --pdb
```

### Deploy Falhando

1. **Verificar logs do GitHub Actions**
2. **Verificar secrets estão configurados**
3. **Testar build local**:
   ```bash
   cd api
   docker build -t test-local .
   docker run -p 8080:8080 test-local
   ```

### ClearML Não Conecta

1. **Verificar credenciais**
2. **Testar conexão**:
   ```python
   from clearml import Task
   task = Task.init(project_name="test", task_name="test")
   ```

## 📈 Métricas e KPIs

### Qualidade do Código
- **Cobertura de Testes**: > 70%
- **Testes Passando**: 100%
- **Análise Estática**: 0 issues críticos

### Performance de Deploy
- **Tempo de Build**: < 5 minutos
- **Tempo de Deploy**: < 2 minutos  
- **Uptime da API**: > 99.5%

### Qualidade dos Modelos
- **Acurácia**: > 85%
- **Tempo de Resposta**: < 200ms
- **Throughput**: > 100 req/min

## 📚 Recursos Adicionais

- [Documentação do pytest](https://docs.pytest.org/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Google Cloud Run](https://cloud.google.com/run/docs)
- [ClearML Documentation](https://clear.ml/docs/)
- [MLOps Best Practices](https://ml-ops.org/)

---

## 🚨 IMPORTANTE - Segurança

- ❌ **NUNCA** commitar secrets ou credenciais
- ✅ Usar GitHub Secrets para informações sensíveis
- ✅ Validar entrada de dados na API
- ✅ Manter dependências atualizadas
- ✅ Revisar code antes de merge