# build-guard.ps1 — versão Windows do hook de build
# Roda após cada alteração de arquivo .cs

$changedFiles = git diff --name-only 2>$null
if (-not ($changedFiles -match "\.cs$")) {
    exit 0
}

$output = dotnet test --no-build --verbosity quiet 2>&1
$exitCode = $LASTEXITCODE

if ($exitCode -ne 0) {
    $msg = "[Boa Vista CI] ⚠️ Testes falharam após a última alteração. Analise os erros abaixo e corrija o código sem alterar o comportamento das regras de negócio existentes.`n`nSaída do dotnet test:`n$output"
    Write-Output "{`"message`": `"$msg`"}"
}

exit 0
