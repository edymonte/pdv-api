#!/bin/bash
# build-guard.sh — roda após cada alteração de arquivo .cs
# Se dotnet test falhar, retorna mensagem estruturada para o Copilot Agent Mode

# Só executa se houver arquivos .cs modificados
if ! git diff --name-only 2>/dev/null | grep -q "\.cs$"; then
  exit 0
fi

OUTPUT=$(dotnet test --no-build --verbosity quiet 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
  echo "{\"message\": \"[Boa Vista CI] ⚠️ Testes falharam após a última alteração. Analise os erros abaixo e corrija o código sem alterar o comportamento das regras de negócio existentes.\n\nSaída do dotnet test:\n$OUTPUT\"}"
fi

exit 0
