# 🚀 Quick Start - MLOps Setup

Este guia fornece instruções passo-a-passo para configurar rapidamente o pipeline MLOps.

## ⚡ Setup Rápido (5 minutos)

### 1. Pré-requisitos

```bash
# Verificar instalações necessárias
python --version        # Python 3.11+
docker --version       # Docker 20.10+
gcloud --version       # Google Cloud CLI
git --version          # Git 2.30+
```

### 2. Clonar e Instalar

```bash
# Clonar repositório
git clone https://github.com/MarlonRF/tcc_clm.git
cd tcc_clm

# Instalar dependências
pip install -r requirements.txt
pip install -r requirements-test.txt
```

### 3. Testes Locais

```bash
# Executar testes
pytest tests/ -v

# Verificar cobertura
pytest --cov=funcoes --cov=api --cov-report=html
```

### 4. Build e Teste da API

```bash
# Build local
cd api
docker build -t conforto-api:local .

# Testar localmente
docker run -p 8080:8080 conforto-api:local

# Teste da API (nova janela do terminal)
curl http://localhost:8080/health
```

## 🔑 Configurar Secrets no GitHub

### GitHub Repository Settings > Secrets and Variables > Actions

```bash
# Google Cloud Platform
GCP_PROJECT_ID: "seu-project-id"
GCP_SA_KEY: "{"type": "service_account", ...}"

# ClearML (opcional, mas recomendado)
CLEARML_WEB_HOST: "https://app.clear.ml"
CLEARML_API_HOST: "https://api.clear.ml"
CLEARML_FILES_HOST: "https://files.clear.ml"
CLEARML_ACCESS_KEY: "sua-access-key"
CLEARML_SECRET_KEY: "sua-secret-key"

# Slack (opcional)
SLACK_WEBHOOK_URL: "https://hooks.slack.com/services/..."
```

## ⚙️ Configuração Google Cloud (Uma vez)

```bash
# 1. Configurar projeto
export PROJECT_ID="seu-project-id"
gcloud config set project $PROJECT_ID

# 2. Habilitar APIs
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# 3. Criar service account
gcloud iam service-accounts create github-actions \
    --display-name="GitHub Actions"

# 4. Conceder permissões
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

# 5. Criar e baixar chave
gcloud iam service-accounts keys create key.json \
    --iam-account=github-actions@$PROJECT_ID.iam.gserviceaccount.com

# 6. Copiar conteúdo do key.json para o secret GCP_SA_KEY
cat key.json
```

## 🎯 Configuração ClearML (Opcional)

```bash
# 1. Criar conta em https://app.clear.ml
# 2. Obter credenciais em Settings > Workspace
# 3. Adicionar aos secrets do GitHub
# 4. Testar localmente:

clearml-init
python -c "from clearml import Task; print('ClearML OK!')"
```

## 🚀 Primeiro Deploy

### Via Push para Main

```bash
git add .
git commit -m "feat: setup MLOps pipeline"
git push origin main
```

### Via Manual Dispatch

1. Acesse GitHub > Actions
2. Selecione "MLOps CI/CD Pipeline"
3. Clique "Run workflow"
4. Escolha "staging" ou "production"

## ✅ Verificar Deploy

```bash
# Aguardar conclusão do workflow (~5-10 minutos)
# URLs serão mostradas nos logs do GitHub Actions

# Testar API deployada
curl https://sua-url-do-cloud-run/health
curl -X POST https://sua-url-do-cloud-run/predict \
  -H "Content-Type: application/json" \
  -d '{
    "idade_anos": 28,
    "peso_kg": 75.0,
    "altura_cm": 167,
    "sexo_biologico": "f",
    "temperatura_media_c": 29.8,
    "umidade_relativa_percent": 35.13,
    "radiacao_solar_media_wm2": 48.51
  }'
```

## 🔧 Comandos Úteis

### Desenvolvimento Local

```bash
# Executar testes específicos
pytest tests/unit/test_pipeline_utils.py -v
pytest tests/integration/test_api.py::TestThermalComfortAPI::test_predict_endpoint_success -v

# Executar API local para desenvolvimento
cd api
uvicorn app:app --reload --host 0.0.0.0 --port 8080

# Build e teste rápido
docker build -t test . && docker run -p 8080:8080 test
```

### Debugging CI/CD

```bash
# Verificar logs do Cloud Run
gcloud run logs tail conforto-termico-api --region=us-central1

# Verificar imagens no registry
gcloud container images list --repository=gcr.io/$PROJECT_ID

# Debug de permissões
gcloud auth list
gcloud projects get-iam-policy $PROJECT_ID
```

### Gerenciamento de Modelos

```bash
# Listar modelos no ClearML (local)
python -c "
from clearml import Model
models = Model.query_models(project_name='conforto_termico')
for m in models[:5]:
    print(f'{m.name}: {m.tags}')
"

# Forçar retreinamento
gh workflow run model-training.yml -f retrain_all=true
```

## 📋 Checklist de Verificação

### ✅ Setup Inicial
- [ ] Python 3.11+ instalado
- [ ] Docker funcionando
- [ ] Google Cloud CLI configurado
- [ ] Repositório clonado
- [ ] Dependências instaladas

### ✅ Testes Locais
- [ ] Testes unitários passando
- [ ] Testes de integração passando
- [ ] API funcionando localmente
- [ ] Docker build funciona

### ✅ Configuração GitHub
- [ ] Secrets do GCP configurados
- [ ] Secrets do ClearML configurados (opcional)
- [ ] Webhook do Slack configurado (opcional)
- [ ] Workflows habilitados

### ✅ Configuração GCP
- [ ] APIs habilitadas
- [ ] Service account criado
- [ ] Permissões concedidas
- [ ] Chave JSON gerada e adicionada aos secrets

### ✅ Deploy Funcional
- [ ] Pipeline CI/CD executado com sucesso
- [ ] Deploy para staging funciona
- [ ] Deploy para production funciona
- [ ] Health checks passando
- [ ] API respondendo corretamente

## 🆘 Problemas Comuns

### Erro: "gcloud command not found"
```bash
# Instalar Google Cloud CLI
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init
```

### Erro: "Permission denied" no GCP
```bash
# Verificar service account
gcloud iam service-accounts list
gcloud projects get-iam-policy $PROJECT_ID

# Re-criar permissões se necessário
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/run.admin"
```

### Erro: "Docker build failed"
```bash
# Verificar Dockerfile
cd api
cat Dockerfile

# Verificar arquivos necessários
ls -la

# Build com logs verbosos
docker build --no-cache --progress=plain -t debug-build .
```

### Erro: "Tests failing"
```bash
# Executar com output detalhado
pytest tests/ -v --tb=long --no-header

# Executar teste específico
pytest tests/unit/test_pipeline_utils.py::TestEnsureGroupColumn -v

# Verificar imports
python -c "from funcoes.pipeline_utils import ensure_group_column; print('OK')"
```

## 📞 Suporte

- **Documentação completa**: `docs/mlops-pipeline.md`
- **Issues**: https://github.com/MarlonRF/tcc_clm/issues
- **Logs**: GitHub Actions tabs
- **Monitoring**: Cloud Run logs no GCP Console

---

**⏰ Tempo estimado para setup completo**: 15-30 minutos  
**✨ Após configuração**: Deploys automáticos a cada push!