# reset-ambiente.ps1 — versão Windows
# Uso: pwsh -File setup\reset-ambiente.ps1

Write-Host ""
Write-Host "=========================================="
Write-Host "  Reset de Ambiente — pdv-api Workshop"
Write-Host "  Farmácia Boa Vista"
Write-Host "=========================================="
Write-Host ""

# 1. Volta para main e descarta todas as alterações
Write-Host "[1/5] Resetando branch para origin/main..."
git checkout main
git reset --hard origin/main
git clean -fd

# 2. Remove governança ativada (volta ao estado SEM instructions para Bloco 1)
Write-Host "[2/5] Removendo governança ativada do .github\..."
$githubDir = Join-Path $PSScriptRoot ".." | Resolve-Path
$githubDir = Join-Path $githubDir ".github"
Remove-Item -ErrorAction SilentlyContinue -Force (Join-Path $githubDir "copilot-instructions.md")
Remove-Item -ErrorAction SilentlyContinue -Recurse -Force (Join-Path $githubDir "instructions")
Remove-Item -ErrorAction SilentlyContinue -Recurse -Force (Join-Path $githubDir "skills")
Remove-Item -ErrorAction SilentlyContinue -Recurse -Force (Join-Path $githubDir "agents")
Remove-Item -ErrorAction SilentlyContinue -Recurse -Force (Join-Path $githubDir "hooks")
@("bloco2-com-instructions.prompt.md","bloco3-mcp-catalogo.prompt.md","bloco4-adicionar-status.prompt.md","bloco4-correcao-manual.prompt.md","bloco6-descricao-pr.prompt.md") | ForEach-Object {
    Remove-Item -ErrorAction SilentlyContinue (Join-Path $githubDir "prompts" $_)
}

# 3. Remove e recria o banco do MCP
Write-Host "[3/5] Recriando banco de catálogo de produtos..."
Remove-Item -ErrorAction SilentlyContinue db\catalogo-produtos.db
sqlite3 db\catalogo-produtos.db ".read db\setup-catalogo.sql"

# 4. Confirma que o build está passando
Write-Host "[4/5] Verificando build..."
dotnet build --configuration Release --verbosity quiet
if ($LASTEXITCODE -ne 0) { Write-Host "❌ Build falhou!"; exit 1 }

# 5. Confirma que os testes estão passando
Write-Host "[5/5] Verificando testes..."
dotnet test --configuration Release --verbosity quiet
if ($LASTEXITCODE -ne 0) { Write-Host "❌ Testes falharam!"; exit 1 }

Write-Host ""
Write-Host "✅ Ambiente resetado com sucesso."
Write-Host "   Estado atual: SEM governança (pronto para o Bloco 1)."
Write-Host "   Para ativar governança no Bloco 2: pwsh -File setup\ativar-governanca.ps1"
Write-Host ""
