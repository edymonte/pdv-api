#!/usr/bin/env python3
"""
Verificação e Preparação de Ambiente — Workshop GitHub Copilot Fase 2
Farmácia Boa Vista · PDV API

Execute:
    Windows : setup.bat          (duplo clique ou terminal)
    Linux/Mac: bash setup.sh
    Direto  : python setup/verificar_ambiente.py
"""

import os
import re
import subprocess
import sys
from pathlib import Path

# ── Encoding seguro no Windows ────────────────────────────────────────────────
if sys.stdout.encoding and sys.stdout.encoding.upper() != "UTF-8":
    sys.stdout = open(sys.stdout.fileno(), mode="w", encoding="utf-8", buffering=1)
    sys.stderr = open(sys.stderr.fileno(), mode="w", encoding="utf-8", buffering=1)

VERDE   = "\033[92m"
VERMELHO = "\033[91m"
AMARELO  = "\033[93m"
AZUL    = "\033[94m"
RESET   = "\033[0m"
NEGRITO = "\033[1m"

ROOT = Path(__file__).resolve().parent.parent
IS_WIN = sys.platform == "win32"

resultados: list[tuple[str, str]] = []


# ── Helpers de output ─────────────────────────────────────────────────────────

def ok(msg: str):
    print(f"  {VERDE}✔{RESET}  {msg}")
    resultados.append(("ok", msg))


def erro(msg: str, dica: str = ""):
    texto = f"  {VERMELHO}✘{RESET}  {msg}"
    if dica:
        texto += f"\n     {AMARELO}→ {dica}{RESET}"
    print(texto)
    resultados.append(("erro", msg))


def aviso(msg: str, dica: str = ""):
    texto = f"  {AMARELO}⚠{RESET}  {msg}"
    if dica:
        texto += f"\n     {AMARELO}→ {dica}{RESET}"
    print(texto)
    resultados.append(("aviso", msg))


def titulo(msg: str):
    print(f"\n{NEGRITO}{msg}{RESET}")
    print("─" * 52)


def perguntar_instalar(nome: str) -> bool:
    """Pergunta se o usuário quer instalar automaticamente."""
    try:
        resp = input(f"     {AZUL}→ Instalar {nome} automaticamente? [S/n]: {RESET}").strip().lower()
        return resp in ("", "s", "sim", "y", "yes")
    except (EOFError, KeyboardInterrupt):
        return False


def run(*args, cwd=None, shell=False, timeout=30) -> subprocess.CompletedProcess:
    return subprocess.run(
        args,
        capture_output=True,
        text=True,
        cwd=cwd or ROOT,
        shell=shell,
        stdin=subprocess.DEVNULL,
        timeout=timeout,
    )


# ─────────────────────────────────────────────────────────────────────────────
print(f"\n{NEGRITO}{'═' * 52}{RESET}")
print(f"{NEGRITO}  GitHub Copilot Workshop Fase 2 — Preparar Ambiente{RESET}")
print(f"{NEGRITO}  Farmácia Boa Vista · PDV API{RESET}")
print(f"{NEGRITO}{'═' * 52}{RESET}")

# ─────────────────────────────────────────────────────────────────────────────
titulo("1. Python 3.11+")

major, minor, micro = sys.version_info[:3]
versao_py = f"{major}.{minor}.{micro}"
if major == 3 and minor >= 11:
    ok(f"Python {versao_py}")
elif major == 3 and minor >= 9:
    aviso(f"Python {versao_py} (recomendado: 3.11+)", "Funciona, mas prefira 3.11 ou superior")
else:
    erro(
        f"Python {versao_py} incompatível",
        "Instale Python 3.11+: https://python.org/downloads\n"
        "     IMPORTANTE: marque 'Add python.exe to PATH' na instalação",
    )

# ─────────────────────────────────────────────────────────────────────────────
titulo("2. .NET 8 SDK")

dotnet_ok = False
dotnet_exe = r"C:\Program Files\dotnet\dotnet.exe" if IS_WIN else "dotnet"

# Procura SDK instalado
sdks_path = Path(r"C:\Program Files\dotnet\sdk") if IS_WIN else Path("/usr/share/dotnet/sdk")
try:
    r = run(dotnet_exe, "--list-sdks", timeout=10)
    sdks = r.stdout.strip()
    sdk8 = [l for l in sdks.splitlines() if l.startswith("8.")]
    if sdk8:
        ok(f".NET SDK {sdk8[0].split()[0]} instalado")
        dotnet_ok = True
    elif sdks:
        # Tem SDK mas não é 8
        aviso(
            f".NET SDK instalado, mas não é versão 8 ({sdks.splitlines()[0].split()[0]})",
            "O workshop usa .NET 8 — funcionalidades podem variar",
        )
        dotnet_ok = True
    else:
        raise ValueError("sem SDK")
except Exception:
    msg = ".NET 8 SDK não encontrado"
    if perguntar_instalar(".NET 8 SDK"):
        print(f"     {AZUL}instalando .NET 8 SDK via winget...{RESET}")
        try:
            r_inst = subprocess.run(
                ["winget", "install", "--id", "Microsoft.DotNet.SDK.8",
                 "--silent", "--accept-source-agreements", "--accept-package-agreements"],
                timeout=300,
            )
            if r_inst.returncode == 0:
                ok(".NET 8 SDK instalado com sucesso  (reabra o terminal para usar 'dotnet')")
                dotnet_ok = True
            else:
                erro(msg, "Falha no winget — baixe manualmente: https://dot.net/download?cid=eshttps://aka.ms/dotnet/download")
        except FileNotFoundError:
            erro(msg, "winget não disponível — baixe em: https://aka.ms/dotnet/download")
        except subprocess.TimeoutExpired:
            erro(msg, "Timeout na instalação — tente manualmente: https://aka.ms/dotnet/download")
    else:
        erro(msg, "Baixe em: https://aka.ms/dotnet/download")

# ─────────────────────────────────────────────────────────────────────────────
titulo("3. Node.js / npx  (MCP sqlite)")

node_ok = False
for cmd in ["node", "npx"]:
    try:
        shell_win = IS_WIN
        r = subprocess.run(
            [cmd, "--version"],
            capture_output=True, text=True,
            stdin=subprocess.DEVNULL,
            shell=shell_win, timeout=8,
        )
        if r.returncode == 0:
            versao_node = r.stdout.strip() or r.stderr.strip()
            ok(f"{cmd} {versao_node}")
            node_ok = True
        else:
            raise ValueError(f"{cmd} exit {r.returncode}")
    except (FileNotFoundError, ValueError, subprocess.TimeoutExpired):
        if cmd == "node":
            msg = "Node.js não encontrado (necessário para MCP sqlite)"
            if perguntar_instalar("Node.js LTS"):
                print(f"     {AZUL}instalando Node.js LTS via winget...{RESET}")
                try:
                    r_inst = subprocess.run(
                        ["winget", "install", "--id", "OpenJS.NodeJS.LTS",
                         "--silent", "--accept-source-agreements", "--accept-package-agreements"],
                        timeout=300,
                    )
                    if r_inst.returncode == 0:
                        ok("Node.js instalado (reabra o terminal)")
                        node_ok = True
                    else:
                        erro(msg, "Falha no winget — baixe em: https://nodejs.org")
                except (FileNotFoundError, subprocess.TimeoutExpired):
                    erro(msg, "Baixe em: https://nodejs.org/en/download/")
            else:
                erro(msg, "Baixe em: https://nodejs.org/en/download/")
        else:
            aviso("npx não respondeu", "Normalmente instalado junto com Node.js")

# ─────────────────────────────────────────────────────────────────────────────
titulo("4. GitHub CLI + Copilot")

# gh
try:
    r = run("gh", "--version", timeout=8)
    if r.returncode == 0:
        versao_gh = r.stdout.strip().splitlines()[0]
        ok(f"{versao_gh}")
    else:
        raise ValueError()
except (FileNotFoundError, ValueError):
    msg = "GitHub CLI (gh) não encontrado"
    if perguntar_instalar("GitHub CLI"):
        print(f"     {AZUL}instalando GitHub CLI via winget...{RESET}")
        try:
            r_inst = subprocess.run(
                ["winget", "install", "--id", "GitHub.cli",
                 "--silent", "--accept-source-agreements", "--accept-package-agreements"],
                timeout=180,
            )
            if r_inst.returncode == 0:
                ok("GitHub CLI instalado (reabra o terminal e faça 'gh auth login')")
            else:
                erro(msg, "Falha no winget — baixe em: https://cli.github.com")
        except (FileNotFoundError, subprocess.TimeoutExpired):
            erro(msg, "Baixe em: https://cli.github.com")
    else:
        erro(msg, "Baixe em: https://cli.github.com")

# gh auth
try:
    r = run("gh", "auth", "status", timeout=8)
    saida = r.stdout + r.stderr
    if "Logged in" in saida or "Active account" in saida:
        usuario = re.search(r"account (\S+)", saida)
        ok(f"gh autenticado{f' como {usuario.group(1)}' if usuario else ''}")
    else:
        aviso("gh não autenticado", "Execute: gh auth login")
except Exception:
    aviso("Não foi possível verificar autenticação do gh", "Execute: gh auth login")

# gh copilot
try:
    r = run("gh", "help", "copilot", timeout=8)
    if r.returncode == 0 and re.search(r"copilot", r.stdout, re.I):
        ok("gh copilot disponível")
    else:
        raise ValueError()
except (FileNotFoundError, ValueError, subprocess.TimeoutExpired):
    aviso(
        "gh copilot não disponível",
        "Execute: gh extension install github/gh-copilot",
    )

# ─────────────────────────────────────────────────────────────────────────────
titulo("5. Banco de dados SQLite (catálogo de produtos)")

db_path = ROOT / "db" / "catalogo-produtos.db"
sql_path = ROOT / "db" / "setup-catalogo.sql"

if db_path.exists():
    ok(f"db/catalogo-produtos.db encontrado")
elif sql_path.exists():
    print(f"     {AZUL}criando banco de dados...{RESET}")
    try:
        import sqlite3 as _sqlite3
        with open(sql_path, encoding="utf-8") as f:
            sql = f.read()
        conn = _sqlite3.connect(db_path)
        for stmt in re.split(r";", sql):
            s = re.sub(r"--[^\n]*", "", stmt).strip()
            if s:
                conn.execute(s)
        conn.commit()
        conn.close()
        ok("db/catalogo-produtos.db criado com sucesso")
    except Exception as exc:
        erro(f"Falha ao criar banco: {exc}", "Execute manualmente: python -c \"import sqlite3; ...\"")
else:
    erro("db/setup-catalogo.sql não encontrado", "Repositório pode estar incompleto — clone novamente")

# ─────────────────────────────────────────────────────────────────────────────
titulo("6. Extensões VS Code recomendadas")

vscode_ext = ROOT / ".vscode" / "extensions.json"
try:
    import json as _json
    with open(vscode_ext) as f:
        recs = _json.load(f).get("recommendations", [])
    ok(f"{len(recs)} extensão(ões) recomendadas em .vscode/extensions.json")
    print(f"     {AZUL}→ Aceite as sugestões quando o VS Code perguntar{RESET}")
except Exception:
    aviso(".vscode/extensions.json não encontrado")

# ─────────────────────────────────────────────────────────────────────────────
titulo("7. Verificação rápida do repositório")

# .github/copilot-instructions.md
gov_ok = (ROOT / ".github" / "copilot-instructions.md").exists()
if gov_ok:
    ok("Governança ativa (.github/copilot-instructions.md presente)")
else:
    aviso(
        "Governança não ativada (Bloco 1 — esperado)",
        "Execute 'bash setup/ativar-governanca.sh' antes do Bloco 2",
    )

# branches
try:
    r = run("git", "branch", "-a", timeout=5)
    branches = r.stdout
    turmas = [t for t in ["feature/dev", "feature/qa", "feature/suporte"] if t in branches]
    if turmas:
        ok(f"Branches de turma: {', '.join(turmas)}")
    else:
        aviso("Branches feature/dev, feature/qa, feature/suporte não encontradas",
              "Execute: git fetch origin")
except Exception:
    aviso("Não foi possível verificar branches")

# ─────────────────────────────────────────────────────────────────────────────
print(f"\n{NEGRITO}{'═' * 52}{RESET}")

total_ok    = sum(1 for r in resultados if r[0] == "ok")
total_erro  = sum(1 for r in resultados if r[0] == "erro")
total_aviso = sum(1 for r in resultados if r[0] == "aviso")

print(f"  {VERDE}✔ {total_ok} ok{RESET}   "
      f"{VERMELHO}✘ {total_erro} erro(s){RESET}   "
      f"{AMARELO}⚠ {total_aviso} aviso(s){RESET}")

if total_erro == 0:
    print(f"\n  {VERDE}{NEGRITO}Ambiente pronto para o workshop! 🚀{RESET}")
    print(f"  Próximo passo: abra o VS Code nesta pasta e comece pelo Bloco 1.")
else:
    print(f"\n  {VERMELHO}{NEGRITO}Corrija os erros acima antes de começar.{RESET}")
    print(f"  Dúvidas? Chame o instrutor ou execute: python setup/verificar_ambiente.py")

print()
