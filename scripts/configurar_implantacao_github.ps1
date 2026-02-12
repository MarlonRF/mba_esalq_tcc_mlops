[CmdletBinding()]
param(
    [string]$Repositorio = "MarlonRF/mba_esalq_tcc_mlops",
    [string]$ProjectId,
    [string]$CaminhoCredenciais,
    [ValidateSet("staging", "production")]
    [string]$Ambiente = "staging",
    [ValidateSet("0", "1")]
    [string]$CompatLegado = "1",
    [ValidateSet("0", "1")]
    [string]$ModoCorteLegado = "0",
    [ValidateSet("0", "1")]
    [string]$ModoTesteSemGcp = "0",
    [ValidateSet("nao", "sim")]
    [string]$ConfirmacaoProducao = "nao",
    [switch]$PularAtualizacaoSecrets,
    [switch]$SemAcompanhar
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Escrever-Etapa {
    param([string]$Mensagem)
    Write-Host ""
    Write-Host "=== $Mensagem ===" -ForegroundColor Cyan
}

function Garantir-Ferramentas {
    Escrever-Etapa "Validando pre-requisitos locais"

    if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
        throw "GitHub CLI (gh) nao encontrado no PATH."
    }

    gh auth status | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Voce precisa autenticar no GitHub CLI: gh auth login"
    }
}

function Validar-Parametros {
    Escrever-Etapa "Validando parametros"

    if ($Ambiente -eq "production" -and $ConfirmacaoProducao -ne "sim") {
        throw "Para deploy em production, use -ConfirmacaoProducao sim."
    }

    if (-not $PularAtualizacaoSecrets -and $ModoTesteSemGcp -eq "0") {
        if ([string]::IsNullOrWhiteSpace($ProjectId)) {
            throw "ProjectId e obrigatorio quando ModoTesteSemGcp=0."
        }
        if ([string]::IsNullOrWhiteSpace($CaminhoCredenciais)) {
            throw "CaminhoCredenciais e obrigatorio quando ModoTesteSemGcp=0."
        }
        if (-not (Test-Path -Path $CaminhoCredenciais -PathType Leaf)) {
            throw "Arquivo de credenciais nao encontrado: $CaminhoCredenciais"
        }
    }
}

function Configurar-Secrets {
    if ($PularAtualizacaoSecrets) {
        Escrever-Etapa "Pulando atualizacao de secrets (opcao solicitada)"
        return
    }

    if ($ModoTesteSemGcp -eq "1" -and [string]::IsNullOrWhiteSpace($ProjectId) -and [string]::IsNullOrWhiteSpace($CaminhoCredenciais)) {
        Escrever-Etapa "Modo teste sem GCP: secrets nao informados, seguindo sem atualizar"
        return
    }

    Escrever-Etapa "Atualizando secrets do repositrio"

    if (-not [string]::IsNullOrWhiteSpace($ProjectId)) {
        gh secret set GCP_PROJECT_ID -R $Repositorio -b $ProjectId
        if ($LASTEXITCODE -ne 0) { throw "Falha ao atualizar secret GCP_PROJECT_ID." }
    }

    if (-not [string]::IsNullOrWhiteSpace($CaminhoCredenciais)) {
        Get-Content -Raw -Path $CaminhoCredenciais | gh secret set GCP_CREDENTIALS -R $Repositorio
        if ($LASTEXITCODE -ne 0) { throw "Falha ao atualizar secret GCP_CREDENTIALS." }
    }

    $secrets = gh secret list -R $Repositorio
    if ($LASTEXITCODE -ne 0) { throw "Falha ao listar secrets no repositrio." }
    $secretsTexto = ($secrets | Out-String)

    if ($ModoTesteSemGcp -eq "0") {
        if ($secretsTexto -notmatch "(?m)^GCP_PROJECT_ID\s") { throw "Secret ausente apos atualizacao: GCP_PROJECT_ID" }
        if ($secretsTexto -notmatch "(?m)^GCP_CREDENTIALS\s") { throw "Secret ausente apos atualizacao: GCP_CREDENTIALS" }
    }
}

function Disparar-Deploy {
    Escrever-Etapa "Disparando workflow de deploy"

    gh workflow run deploy.yml -R $Repositorio `
        -f environment=$Ambiente `
        -f compat_legado=$CompatLegado `
        -f modo_corte_legado=$ModoCorteLegado `
        -f modo_teste_sem_gcp=$ModoTesteSemGcp `
        -f confirmacao_producao=$ConfirmacaoProducao
    if ($LASTEXITCODE -ne 0) { throw "Falha ao disparar workflow deploy.yml." }
}

function Acompanhar-Deploy {
    if ($SemAcompanhar) {
        Escrever-Etapa "Acompanhamento desativado (opcao solicitada)"
        return
    }

    Escrever-Etapa "Aguardando e acompanhando execucao"
    Start-Sleep -Seconds 4

    $runId = gh run list -R $Repositorio --workflow deploy.yml --limit 1 --json databaseId --jq '.[0].databaseId'
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($runId)) {
        throw "Nao foi possivel identificar o run id do deploy."
    }

    gh run watch -R $Repositorio $runId --exit-status
    if ($LASTEXITCODE -ne 0) {
        throw "Workflow de deploy concluiu com falha. Run id: $runId"
    }

    $runUrl = gh run view -R $Repositorio $runId --json url --jq .url
    if ($LASTEXITCODE -eq 0 -and -not [string]::IsNullOrWhiteSpace($runUrl)) {
        Write-Host "Deploy concluido com sucesso: $runUrl" -ForegroundColor Green
    }
}

try {
    Garantir-Ferramentas
    Validar-Parametros
    Configurar-Secrets
    Disparar-Deploy
    Acompanhar-Deploy
}
catch {
    Write-Error $_.Exception.Message
    exit 1
}
