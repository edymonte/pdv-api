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
IS_WIN   = sys.platform == "win32"
IS_MAC   = sys.platform == "darwin"
IS_LINUX = sys.platform.startswith("linux")

resultados: list[tuple[str, str]] = []


# ── Detecção de gerenciadores de pacotes ──────────────────────────────────────

def _cmd_existe(cmd: str) -> bool:
    try:
        subprocess.run([cmd, "--version"], capture_output=True, stdin=subprocess.DEVNULL, timeout=5)
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False

def _has_brew()  -> bool: return IS_MAC   and _cmd_existe("brew")
def _has_winget()-> bool: return IS_WIN   and _cmd_existe("winget")
def _has_apt()   -> bool: return IS_LINUX and _cmd_existe("apt-get")


def _instalar_winget(package_id: str, timeout: int = 300) -> bool:
    r = subprocess.run(
        ["winget", "install", "--id", package_id,
         "--silent", "--accept-source-agreements", "--accept-package-agreements"],
        timeout=timeout,
    )
    return r.returncode == 0


def _instalar_brew(formula: str, cask: bool = False, timeout: int = 300) -> bool:
    cmd = ["brew", "install"] + (["--cask"] if cask else []) + [formula]
    r = subprocess.run(cmd, timeout=timeout)
    return r.returncode == 0


def _instalar_apt(pacote: str, timeout: int = 300) -> bool:
    # atualiza índice silenciosamente antes de instalar
    subprocess.run(["sudo", "apt-get", "update", "-qq"],
                   timeout=60, stdin=subprocess.DEVNULL)
    r = subprocess.run(["sudo", "apt-get", "install", "-y", pacote], timeout=timeout)
    return r.returncode == 0


def _instalar_snap(pacote: str, classic: bool = False, timeout: int = 300) -> bool:
    cmd = ["sudo", "snap", "install", pacote] + (["--classic"] if classic else [])
    r = subprocess.run(cmd, timeout=timeout)
    return r.returncode == 0


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
        "     Windows: marque 'Add python.exe to PATH' na instalação\n"
        "     macOS  : brew install python@3.11\n"
        "     Linux  : sudo apt install python3.11",
    )

# ─────────────────────────────────────────────────────────────────────────────
titulo("2. .NET 8 SDK")

dotnet_ok = False
dotnet_exe = r"C:\Program Files\dotnet\dotnet.exe" if IS_WIN else "dotnet"
try:
    r = run(dotnet_exe, "--list-sdks", timeout=10)
    sdks = r.stdout.strip()
    sdk8 = [l for l in sdks.splitlines() if l.startswith("8.")]
    if sdk8:
        ok(f".NET SDK {sdk8[0].split()[0]} instalado")
        dotnet_ok = True
    elif sdks:
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
        instalado = False
        try:
            if _has_winget():
                print(f"     {AZUL}instalando via winget (Windows)...{RESET}")
                instalado = _instalar_winget("Microsoft.DotNet.SDK.8")
            elif _has_brew():
                print(f"     {AZUL}instalando via Homebrew (macOS)...{RESET}")
                instalado = _instalar_brew("dotnet@8")
            elif _has_apt():
                # Adiciona repositório Microsoft e instala
                print(f"     {AZUL}instalando via apt (Linux)...{RESET}")
                subprocess.run(
                    ["bash", "-c",
                     "wget -q https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb "
                     "-O /tmp/packages-microsoft-prod.deb && sudo dpkg -i /tmp/packages-microsoft-prod.deb"],
                    timeout=60,
                )
                instalado = _instalar_apt("dotnet-sdk-8.0")
            else:
                raise FileNotFoundError("nenhum gerenciador disponível")
        except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
            instalado = False
            aviso(f"Auto-install falhou: {exc}")

        if instalado:
            ok(".NET 8 SDK instalado  (reabra o terminal para usar 'dotnet')")
            dotnet_ok = True
        else:
            erro(msg, "Baixe manualmente em: https://aka.ms/dotnet/download")
    else:
        erro(msg, "Baixe em: https://aka.ms/dotnet/download")

# ─────────────────────────────────────────────────────────────────────────────
titulo("3. Node.js / npx  (MCP sqlite)")

node_ok = False
for cmd in ["node", "npx"]:
    try:
        r = subprocess.run(
            [cmd, "--version"],
            capture_output=True, text=True,
            stdin=subprocess.DEVNULL,
            shell=IS_WIN, timeout=8,
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
                instalado = False
                try:
                    if _has_winget():
                        print(f"     {AZUL}instalando via winget (Windows)...{RESET}")
                        instalado = _instalar_winget("OpenJS.NodeJS.LTS")
                    elif _has_brew():
                        print(f"     {AZUL}instalando via Homebrew (macOS)...{RESET}")
                        instalado = _instalar_brew("node")
                    elif _has_apt():
                        print(f"     {AZUL}instalando via apt (Linux)...{RESET}")
                        # NodeSource LTS
                        subprocess.run(
                            ["bash", "-c",
                             "curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -"],
                            timeout=60,
                        )
                        instalado = _instalar_apt("nodejs")
                    else:
                        raise FileNotFoundError("nenhum gerenciador disponível")
                except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
                    aviso(f"Auto-install falhou: {exc}")

                if instalado:
                    ok("Node.js instalado (reabra o terminal)")
                    node_ok = True
                else:
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
        instalado = False
        try:
            if _has_winget():
                print(f"     {AZUL}instalando via winget (Windows)...{RESET}")
                instalado = _instalar_winget("GitHub.cli", timeout=180)
            elif _has_brew():
                print(f"     {AZUL}instalando via Homebrew (macOS)...{RESET}")
                instalado = _instalar_brew("gh")
            elif _has_apt():
                print(f"     {AZUL}instalando via apt (Linux)...{RESET}")
                # Repositório oficial do GitHub CLI
                subprocess.run(
                    ["bash", "-c",
                     "(type -p wget >/dev/null || (sudo apt update && sudo apt install wget -y)) "
                     "&& sudo mkdir -p -m 755 /etc/apt/keyrings "
                     "&& out=$(mktemp) && wget -nv -O$out https://cli.github.com/packages/githubcli-archive-keyring.gpg "
                     "&& cat $out | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null "
                     "&& sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg "
                     "&& echo \"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] "
                     "https://cli.github.com/packages stable main\" "
                     "| sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null"],
                    timeout=60,
                )
                instalado = _instalar_apt("gh", timeout=180)
            else:
                raise FileNotFoundError("nenhum gerenciador disponível")
        except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
            aviso(f"Auto-install falhou: {exc}")

        if instalado:
            ok("GitHub CLI instalado (reabra o terminal e execute: gh auth login)")
        else:
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
