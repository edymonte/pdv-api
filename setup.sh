#!/usr/bin/env bash
# GitHub Copilot Workshop Fase 2 — Preparar Ambiente
# Farmácia Boa Vista · PDV API

cd "$(dirname "$0")"

echo ""
echo " GitHub Copilot Workshop Fase 2 -- Preparar Ambiente"
echo " ===================================================="
echo ""

if command -v python3 &>/dev/null; then
    python3 setup/verificar_ambiente.py
elif command -v python &>/dev/null; then
    python setup/verificar_ambiente.py
else
    echo " Python não encontrado."
    echo " Instale Python 3.11+: https://python.org/downloads"
fi
