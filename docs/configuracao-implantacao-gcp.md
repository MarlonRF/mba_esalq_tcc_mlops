# Setup de Deploy GCP (Cloud Run)

Este guia padroniza a configuracao para o workflow `deploy.yml`.

## Objetivo

Permitir deploy de staging e production pelo GitHub Actions, com:
- pre-checks de teste;
- build/push de imagem;
- health check e smoke de contrato.

## Pre-requisitos

- Projeto GCP ativo
- APIs habilitadas (Cloud Run, Artifact Registry/Container Registry, Cloud Build)
- Service Account para deploy

## Permissoes recomendadas para a Service Account de deploy

No projeto GCP:
- `roles/run.admin`
- `roles/iam.serviceAccountUser`
- `roles/artifactregistry.writer` (ou permissoes equivalentes no registry usado)
- `roles/storage.objectAdmin` (se necessario no fluxo atual)

## Secrets no GitHub

No repositorio, configure:
- `GCP_PROJECT_ID`
- `GCP_CREDENTIALS` (JSON da chave da service account)

## Workflows e modos

Arquivo:
- `.github/workflows/deploy.yml`

Entradas de `workflow_dispatch`:
- `environment`: `staging` ou `production`
- `compat_legado`: `1`/`0`
- `modo_corte_legado`: `1`/`0`
- `modo_teste_sem_gcp`: `1`/`0`
- `confirmacao_producao`: `sim`/`nao`

## Regras atuais de seguranca no deploy

- Push em `main` dispara deploy de staging.
- Deploy de production e manual (`workflow_dispatch`).
- Production so permite execucao quando:
  - branch de execucao e `main`;
  - `confirmacao_producao=sim`.

## Teste rapido

### 1. Teste sem GCP (pipeline de CD)

Use:
- `modo_teste_sem_gcp=1`

Resultado esperado:
- valida pipeline de deploy local (build + health + predict) sem autenticar no GCP.

### 2. Teste real em staging

Use:
- `environment=staging`
- `modo_teste_sem_gcp=0`

Resultado esperado:
- deploy no servico `conforto-termico-api-staging`
- health check e smoke de contrato com sucesso.

### 3. Teste real em production

Use:
- `environment=production`
- `confirmacao_producao=sim`
- `modo_teste_sem_gcp=0`

## Verificacoes pos-deploy

- `GET /health` retorna `200`
- `POST /predict` retorna `200`
- cabecalhos de compatibilidade presentes

## Problemas comuns

### Falha em autenticacao GCP

- conferir secret `GCP_CREDENTIALS`
- conferir formato JSON valido
- conferir role da service account

### Health check falha com 403

- revisar IAM de invoker no servico Cloud Run;
- confirmar comportamento esperado de acesso publico.

### Build/push falha

- revisar permissoes de registry;
- revisar projeto GCP no secret `GCP_PROJECT_ID`.
