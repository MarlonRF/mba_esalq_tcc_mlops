# 🚀 Configuração de Deploy no Google Cloud Platform

## 📋 **Pré-requisitos**

Para habilitar o deploy automático no Google Cloud Run, você precisa configurar:

### 1. **Projeto no Google Cloud Platform**
- Crie um projeto no [Google Cloud Console](https://console.cloud.google.com/)
- Anote o **Project ID** (ex: `meu-projeto-123456`)
- Habilite as APIs necessárias:
  - Cloud Run API
  - Container Registry API
  - Cloud Build API

### 2. **Service Account (Conta de Serviço)**
- Acesse IAM & Admin > Service Accounts
- Crie uma nova service account com as permissões:
  - `Cloud Run Admin`
  - `Storage Admin`
  - `Cloud Build Editor`
- Baixe a chave JSON da service account

## 🔧 **Configuração dos Secrets no GitHub**

### Passo 1: Acessar Configurações do Repositório
1. Vá para o seu repositório no GitHub
2. Clique em **Settings** (Configurações)
3. No menu lateral, clique em **Secrets and variables** > **Actions**

### Passo 2: Adicionar os Secrets
Clique em **New repository secret** para cada um:

#### **Secret 1: GCP_CREDENTIALS**
- **Nome**: `GCP_CREDENTIALS`
- **Valor**: Cole todo o conteúdo do arquivo JSON da service account
```json
{
  "type": "service_account",
  "project_id": "seu-projeto-id",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\\n...\\n-----END PRIVATE KEY-----\\n",
  "client_email": "nome@seu-projeto.iam.gserviceaccount.com",
  ...
}
```

#### **Secret 2: GCP_PROJECT_ID**
- **Nome**: `GCP_PROJECT_ID`
- **Valor**: ID do seu projeto (ex: `meu-projeto-123456`)

## 🧪 **Testando a Configuração**

Após configurar os secrets:

1. **Fazer um push** para a branch `main` ou `test-clearml-script`
2. **Verificar execução** no GitHub Actions
3. **Acompanhar logs** do job `deploy`

### 📋 **Checklist de Verificação**
- [ ] Projeto GCP criado
- [ ] APIs habilitadas (Cloud Run, Container Registry, Cloud Build)
- [ ] Service Account criada com permissões corretas
- [ ] Chave JSON baixada
- [ ] Secret `GCP_CREDENTIALS` configurado
- [ ] Secret `GCP_PROJECT_ID` configurado

## 🐳 **Estrutura do Deploy**

O workflow fará automaticamente:

1. **Setup**: Instala dependências e gera modelo
2. **Build**: Constrói imagem Docker da API
3. **Push**: Envia para Google Container Registry
4. **Deploy**: Implanta no Cloud Run com configurações:
   - **Região**: us-central1
   - **Memória**: 512Mi
   - **CPU**: 1
   - **Instâncias**: 0-5 (auto-scaling)
   - **Porta**: 8080
   - **Acesso**: Público (não autenticado)

## 🌐 **Após o Deploy**

A API estará disponível em uma URL como:
```
https://conforto-termico-api-[hash]-uc.a.run.app
```

### Endpoints disponíveis:
- **GET /**: Health check
- **POST /predict**: Predição de conforto térmico

### Exemplo de uso:
```bash
curl -X POST https://sua-url.run.app/predict \\
  -H "Content-Type: application/json" \\
  -d '{
    "idade_anos": 30,
    "peso_kg": 70.0,
    "altura_cm": 175,
    "sexo_biologico": "m",
    "temperatura_media_c": 25.0,
    "umidade_relativa_percent": 60.0,
    "radiacao_solar_media_wm2": 400.0
  }'
```

## ⚠️ **Importante**

- Os secrets são **sensíveis** - nunca os compartilhe
- O deploy só executa se **todos os testes passarem**
- Custos do GCP são de **sua responsabilidade**
- Configure **alertas de billing** no GCP

## 🔍 **Troubleshooting**

### Deploy falha com "Permission denied"
- Verifique se a service account tem as permissões corretas
- Confirme se os secrets estão configurados corretamente

### Build falha
- Verifique se as APIs do GCP estão habilitadas
- Confirme se o projeto GCP está ativo

### API não responde
- Verifique logs no Cloud Run Console
- Confirme se o modelo foi gerado corretamente