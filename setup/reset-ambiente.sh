#!/bin/bash
# reset-ambiente.sh — executar entre turmas para garantir ambiente limpo
# Uso: bash setup/reset-ambiente.sh

set -e

echo ""
echo "=========================================="
echo "  Reset de Ambiente — pdv-api Workshop"
echo "  Farmácia Boa Vista"
echo "=========================================="
echo ""

# 1. Volta para main e descarta todas as alterações
echo "[1/5] Resetando branch para origin/main..."
git checkout main
git reset --hard origin/main
git clean -fd

# 2. Remove governança ativada (volta ao estado SEM instructions para Bloco 1)
echo "[2/5] Removendo governança ativada do .github/..."
rm -rf .github/copilot-instructions.md
rm -rf .github/instructions
rm -rf .github/skills
rm -rf .github/agents
rm -rf .github/hooks
rm -rf .github/prompts/bloco2-com-instructions.prompt.md
rm -rf .github/prompts/bloco3-mcp-catalogo.prompt.md
rm -rf .github/prompts/bloco4-adicionar-status.prompt.md
rm -rf .github/prompts/bloco4-correcao-manual.prompt.md
rm -rf .github/prompts/bloco6-descricao-pr.prompt.md

# 3. Remove e recria o banco do MCP
echo "[3/5] Recriando banco de catálogo de produtos..."
rm -f db/catalogo-produtos.db
sqlite3 db/catalogo-produtos.db < db/setup-catalogo.sql

# 4. Confirma que o build está passando
echo "[4/5] Verificando build..."
dotnet build --configuration Release --verbosity quiet

# 5. Confirma que os testes estão passando
echo "[5/5] Verificando testes..."
dotnet test --configuration Release --verbosity quiet

echo ""
echo "✅ Ambiente resetado com sucesso."
echo "   Estado atual: SEM governança (pronto para o Bloco 1)."
echo "   Para ativar governança no Bloco 2: bash setup/ativar-governanca.sh"
echo ""
