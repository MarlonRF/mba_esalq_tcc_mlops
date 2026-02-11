# Guia MLOps (Padrao Atual)

Este documento descreve o fluxo operacional atual do projeto.

## Arquitetura

Componentes principais:
- processamento e treino: `src/processamento`, `src/treinamento`, `src/features`, `src/pipelines`, `src/utils`
- API independente: `src/api`
- integracao opcional com ClearML: `src/integracao_clearml`

Diretorios de apoio:
- `config/`: configuracoes e dicionarios
- `relatorios/`: resultados de testes e cobertura
- `legacy/`: codigo antigo temporario
- `notebooks/`: prototipagem local

## Testes

Executar suite critica (sem ClearML):

```bash
uv sync --extra test
uv run python -m pytest tests/unit -m "not clearml" --disable-warnings
```

Executar testes da API:

```bash
uv run python -m pytest tests/unit/api -q --disable-warnings
```

## CI

Workflow: `.github/workflows/ci.yml`

Fluxo:
- job `unit-critical`
- job `api-smoke` (contrato legado ativo/inativo e modo corte)
- upload de relatorios em `relatorios/`

## CD

Workflow: `.github/workflows/deploy.yml`

Fluxo:
- pre-deploy checks (testes criticos + build)
- deploy Cloud Run
- health check + smoke de contrato

Regras:
- push em `main`: staging
- production: manual com confirmacao explicita

## Fluxo de trabalho recomendado

1. Trabalhar em branch de feature.
2. Abrir PR para `main`.
3. Aguardar CI verde.
4. Merge em `main`.
5. Validar deploy de staging.
6. Rodar deploy manual de production quando necessario.

## Rollback

Opcoes praticas:
- reexecutar deploy com commit anterior (SHA anterior);
- no Cloud Run, direcionar trafego para revisao anterior.

## ClearML (opcional)

- Instale com `uv sync --extra clearml`
- Configure conforme `docs/clearml-configuracao.md`
- Mantenha CI critico independente de ClearML para estabilidade.

## Monitoramento basico

- acompanhar jobs no GitHub Actions;
- acompanhar logs e revisoes no Cloud Run;
- validar `/health` e `/predict` apos cada deploy.
