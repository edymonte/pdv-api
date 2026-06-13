@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"

echo.
echo  GitHub Copilot Workshop Fase 2 -- Preparar Ambiente
echo  ====================================================
echo.

python setup\verificar_ambiente.py
if errorlevel 9009 (
    echo.
    echo  Python nao encontrado.
    echo  Baixe em: https://python.org/downloads/
    echo  IMPORTANTE: marque "Add python.exe to PATH" na instalacao.
    echo.
)

echo.
pause
