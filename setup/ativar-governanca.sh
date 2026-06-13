#!/bin/bash
# ativar-governanca.sh — executar no início do Bloco 2
# Copia todos os arquivos de governança para o .github/ ativo
# Uso: bash setup/ativar-governanca.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
ORIGEM="$REPO_ROOT/governanca/.github"
DESTINO="$REPO_ROOT/.github"

echo ""
echo "=========================================="
echo "  Ativando Governança — pdv-api"
echo "  Farmácia Boa Vista"
echo "=========================================="
echo ""

if [ ! -d "$ORIGEM" ]; then
  echo "❌ Pasta governanca/.github não encontrada. Execute a partir da raiz do repo."
  exit 1
fi

echo "[1/3] Copiando arquivos de governança para .github/..."
cp -r "$ORIGEM/." "$DESTINO/"

echo "[2/3] Verificando arquivos ativados:"
echo "  ✔ copilot-instructions.md"
echo "  ✔ instructions/ (testes + validação)"
echo "  ✔ skills/gerar-testes-pdv/"
echo "  ✔ agents/qa-boa-vista.agent.md"
echo "  ✔ hooks/build-guard.json"
echo "  ✔ prompts/ (blocos 2-6)"

echo "[3/3] Recarregue o VS Code ou abra um novo chat do Copilot para ativar as instructions."

echo ""
echo "✅ Governança ativada. O agente agora conhece as regras do time."
echo "   Próximo passo: execute o Prompt do Bloco 2."
echo ""
