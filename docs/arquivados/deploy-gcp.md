# Deploy da API Thermal Comfort na Google Cloud Platform (GCP)

## Pré-requisitos

1. **Google Cloud CLI instalado**
   ```bash
   # Instalar gcloud CLI
   # https://cloud.google.com/sdk/docs/install
   ```

2. **Docker instalado e rodando**

3. **Conta GCP com projeto criado**

4. **Configurar autenticação**
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   gcloud auth configure-docker
   ```

## Métodos de Deploy

### Método 1: Deploy Manual (Recomendado para teste)

1. **Configurar variáveis**
   ```bash
   # Substitua pelo seu Project ID
   export PROJECT_ID="your-project-id"
   ```

2. **Executar script de deploy**
   ```bash
   # Linux/Mac
   chmod +x deploy.sh
   ./deploy.sh

   # Windows PowerShell
   .\deploy.ps1 -ProjectId "your-project-id"
   ```

### Método 2: Deploy usando comandos individuais

```bash
# 1. Build da imagem
docker build -t gcr.io/YOUR_PROJECT_ID/thermal-comfort-api ./api

# 2. Push para Container Registry
docker push gcr.io/YOUR_PROJECT_ID/thermal-comfort-api

# 3. Deploy no Cloud Run
gcloud run deploy thermal-comfort-api \
    --image gcr.io/YOUR_PROJECT_ID/thermal-comfort-api \
    --region us-central1 \
    --platform managed \
    --allow-unauthenticated \
    --port 8080 \
    --memory 2Gi \
    --cpu 1 \
    --max-instances 10
```

### Método 3: Deploy usando Cloud Build (CI/CD)

1. **Habilitar APIs necessárias**
   ```bash
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable run.googleapis.com
   ```

2. **Executar build**
   ```bash
   gcloud builds submit --config cloudbuild.yaml .
   ```

## Testando a API

Após o deploy, você receberá uma URL. Teste os endpoints:

```bash
# Health check
curl https://YOUR_API_URL/health

# Root endpoint
curl https://YOUR_API_URL/

# Prediction endpoint
curl -X POST https://YOUR_API_URL/predict \
  -H "Content-Type: application/json" \
  -d '{
    "idade_anos": 25,
    "peso_kg": 70,
    "altura_cm": 175,
    "sexo_biologico": "m",
    "temperatura_media_c": 30.5,
    "umidade_relativa_percent": 65.0,
    "radiacao_solar_media_wm2": 250.0
  }'
```

## Monitoramento

- **Logs**: `gcloud logs read --service thermal-comfort-api`
- **Métricas**: Acesse o Console GCP > Cloud Run > thermal-comfort-api

## Configurações Avançadas

### Variáveis de Ambiente
```bash
gcloud run services update thermal-comfort-api \
    --set-env-vars "ENV_VAR_NAME=value" \
    --region us-central1
```

### Autenticação
Para requerir autenticação, remova `--allow-unauthenticated` do comando de deploy.

### Scaling
```bash
gcloud run services update thermal-comfort-api \
    --min-instances 1 \
    --max-instances 20 \
    --region us-central1
```

## Troubleshooting

1. **Erro de autenticação**: `gcloud auth login`
2. **Erro de permissões**: Verificar IAM roles
3. **Erro de build**: Verificar Dockerfile e dependências
4. **Erro de memória**: Aumentar `--memory` para 4Gi ou mais

## Custos

O Cloud Run cobra por:
- Tempo de CPU (quando a aplicação está processando requests)
- Memória utilizada
- Requests recebidos

Com o tier gratuito, você tem:
- 2 milhões de requests por mês
- 400.000 GB-segundos de CPU
- 360.000 GB-segundos de memória