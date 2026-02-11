# Estrutura CI/CD (Atual)

Este documento padroniza a estrutura de CI/CD usada no repositorio.

## Workflows

### CI

Arquivo: `.github/workflows/ci.yml`

Responsabilidades:
- instalar dependencias com `uv`;
- validar qualidade minima (compilacao/build);
- executar testes criticos sem ClearML;
- executar smoke da API em multiplos modos de contrato;
- publicar relatorios de execucao.

### CD

Arquivo: `.github/workflows/deploy.yml`

Responsabilidades:
- executar pre-checks antes de deploy;
- build/push da imagem;
- deploy no Cloud Run;
- health check e smoke de contrato pos-deploy.

## Estrutura recomendada de diretorios

```text
.
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
├── config/
├── docs/
├── relatorios/
├── src/
│   ├── api/
│   ├── integracao_clearml/
│   ├── pipelines/
│   ├── processamento/
│   ├── treinamento/
│   ├── features/
│   └── utils/
└── tests/
```

## Artefatos e saidas

- Relatorios de teste: `relatorios/`
- Cobertura: `relatorios/coverage.xml`
- Artefatos de smoke API: upload no CI

## Variaveis e secrets

Secrets GitHub (deploy real):
- `GCP_PROJECT_ID`
- `GCP_CREDENTIALS`

Flags importantes no deploy:
- `compat_legado`
- `modo_corte_legado`
- `modo_teste_sem_gcp`
- `confirmacao_producao`

## Politica de deploy

- staging via push em `main`;
- production via `workflow_dispatch`;
- production bloqueada fora de `main` e sem confirmacao explicita.

## Validacao minima apos deploy

- `GET /health` com status `200`
- `POST /predict` com status `200`
- cabecalhos de transicao de contrato presentes
