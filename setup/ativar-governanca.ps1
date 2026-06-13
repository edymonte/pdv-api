# ativar-governanca.ps1 — versão Windows, executar no início do Bloco 2
# Uso: pwsh -File setup\ativar-governanca.ps1

$repoRoot = Split-Path $PSScriptRoot -Parent
$origem   = Join-Path $repoRoot "governanca\.github"
$destino  = Join-Path $repoRoot ".github"

Write-Host ""
Write-Host "=========================================="
Write-Host "  Ativando Governança — pdv-api"
Write-Host "  Farmácia Boa Vista"
Write-Host "=========================================="
Write-Host ""

if (-not (Test-Path $origem)) {
    Write-Host "❌ Pasta governanca\.github não encontrada."
    exit 1
}

Write-Host "[1/3] Copiando arquivos de governança para .github/..."
Copy-Item -Path "$origem\*" -Destination $destino -Recurse -Force

Write-Host "[2/3] Arquivos ativados:"
Write-Host "  ✔ copilot-instructions.md"
Write-Host "  ✔ instructions\ (testes + validação)"
Write-Host "  ✔ skills\gerar-testes-pdv\"
Write-Host "  ✔ agents\qa-boa-vista.agent.md"
Write-Host "  ✔ hooks\build-guard.json"
Write-Host "  ✔ prompts\ (blocos 2-6)"

Write-Host "[3/3] Recarregue o VS Code ou abra um novo chat do Copilot."

Write-Host ""
Write-Host "✅ Governança ativada. O agente agora conhece as regras do time."
Write-Host "   Próximo passo: execute o Prompt do Bloco 2."
Write-Host ""
