#!/usr/bin/env python3
"""
PDV API — Farmácia Boa Vista
Gerador de Evidências do Workshop GitHub Copilot (Fase 2)

Valida os 8 pilares da extensibilidade do Copilot para cada participante
e gera um HTML de evidência individual.

Uso:
    python setup/gerar_evidencia.py --nome "João Silva" --turma dev
    python setup/gerar_evidencia.py --nome "Ana Lima"   --turma qa
    python setup/gerar_evidencia.py --nome "Carlos Mota" --turma suporte
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import webbrowser
from datetime import datetime

# Força UTF-8 no terminal Windows para exibir emojis
if sys.stdout.encoding and sys.stdout.encoding.upper() != "UTF-8":
    sys.stdout = open(sys.stdout.fileno(), mode="w", encoding="utf-8", buffering=1)
    sys.stderr = open(sys.stderr.fileno(), mode="w", encoding="utf-8", buffering=1)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# ─────────────────────────────────────────────────────────────────────────────
# 8 Pilares — definição e critérios de validação
# ─────────────────────────────────────────────────────────────────────────────

PILARES = [
    {
        "id": "instructions",
        "label": "Instructions",
        "descricao": "Regras permanentes do time injetadas em todo contexto do Copilot",
        "icone": "📋",
        "checks": [
            {
                "desc": "copilot-instructions.md ativo no repositório",
                "tipo": "arquivo_existe",
                "arquivo": ".github/copilot-instructions.md",
            },
            {
                "desc": "Instructions específicas de testes configuradas",
                "tipo": "arquivo_existe",
                "arquivo": ".github/instructions/testes.instructions.md",
            },
            {
                "desc": "Instructions específicas de validação configuradas",
                "tipo": "arquivo_existe",
                "arquivo": ".github/instructions/validacao.instructions.md",
            },
            {
                "desc": "Instructions contêm regras de arquitetura (Services/Controllers)",
                "tipo": "presenca_texto",
                "arquivo": ".github/copilot-instructions.md",
                "pattern": r"Service|Controller",
            },
        ],
    },
    {
        "id": "skills",
        "label": "Skills",
        "descricao": "Conhecimento especializado injetado sob demanda no contexto",
        "icone": "🧠",
        "checks": [
            {
                "desc": "Skill gerar-testes-pdv presente",
                "tipo": "arquivo_existe",
                "arquivo": ".github/skills/gerar-testes-pdv/SKILL.md",
            },
            {
                "desc": "Skill contém padrão de nomenclatura Should_X_When_Y",
                "tipo": "presenca_texto",
                "arquivo": ".github/skills/gerar-testes-pdv/SKILL.md",
                "pattern": r"Should_",
            },
            {
                "desc": "Skill define cobertura mínima exigida",
                "tipo": "presenca_texto",
                "arquivo": ".github/skills/gerar-testes-pdv/SKILL.md",
                "pattern": r"cobertura|mínima|mínimo",
            },
        ],
    },
    {
        "id": "agents",
        "label": "Agents",
        "descricao": "Agentes especialistas com identidade, escopo e ferramentas próprias",
        "icone": "🤖",
        "checks": [
            {
                "desc": "Custom Agent @qa-boa-vista configurado",
                "tipo": "arquivo_existe",
                "arquivo": ".github/agents/qa-boa-vista.agent.md",
            },
            {
                "desc": "Agent define ferramentas (tools) ativas",
                "tipo": "presenca_texto",
                "arquivo": ".github/agents/qa-boa-vista.agent.md",
                "pattern": r"^tools:",
            },
            {
                "desc": "Agent contém critérios de revisão de segurança",
                "tipo": "presenca_texto",
                "arquivo": ".github/agents/qa-boa-vista.agent.md",
                "pattern": r"segurança|SQL|injection|OWASP",
            },
        ],
    },
    {
        "id": "mcp",
        "label": "MCP",
        "descricao": "Ferramentas externas conectadas ao Agent Mode via Model Context Protocol",
        "icone": "🔌",
        "checks": [
            {
                "desc": "mcp.json configurado no workspace",
                "tipo": "arquivo_existe",
                "arquivo": ".vscode/mcp.json",
            },
            {
                "desc": "Servidor MCP sqlite-catalogo registrado",
                "tipo": "presenca_texto",
                "arquivo": ".vscode/mcp.json",
                "pattern": r"sqlite-catalogo",
            },
            {
                "desc": "Banco de dados do catálogo de produtos criado",
                "tipo": "arquivo_existe",
                "arquivo": "db/catalogo-produtos.db",
            },
            {
                "desc": "Script de setup do banco presente",
                "tipo": "arquivo_existe",
                "arquivo": "db/setup-catalogo.sql",
            },
        ],
    },
    {
        "id": "hooks",
        "label": "Hooks",
        "descricao": "Controle de ações do agente — único primitivo que pode bloquear e auditar",
        "icone": "🪝",
        "checks": [
            {
                "desc": "Hook build-guard.json configurado",
                "tipo": "arquivo_existe",
                "arquivo": ".github/hooks/build-guard.json",
            },
            {
                "desc": "Hook usa evento postToolUse para detectar falhas",
                "tipo": "presenca_texto",
                "arquivo": ".github/hooks/build-guard.json",
                "pattern": r"postToolUse",
            },
            {
                "desc": "Script do hook presente para Windows (PowerShell)",
                "tipo": "arquivo_existe",
                "arquivo": ".github/hooks/scripts/build-guard.ps1",
            },
            {
                "desc": "Script do hook presente para Linux/Mac (bash)",
                "tipo": "arquivo_existe",
                "arquivo": ".github/hooks/scripts/build-guard.sh",
            },
        ],
    },
    {
        "id": "knowledge_base",
        "label": "Knowledge Base",
        "descricao": "Prompts reutilizáveis que encapsulam o conhecimento do time para o agente",
        "icone": "📚",
        "checks": [
            {
                "desc": "Prompt Bloco 2 — instructions ativas",
                "tipo": "arquivo_existe",
                "arquivo": ".github/prompts/bloco2-com-instructions.prompt.md",
            },
            {
                "desc": "Prompt Bloco 3 — MCP catálogo de produtos",
                "tipo": "arquivo_existe",
                "arquivo": ".github/prompts/bloco3-mcp-catalogo.prompt.md",
            },
            {
                "desc": "Prompt Bloco 4 — gatilho de autocorreção",
                "tipo": "arquivo_existe",
                "arquivo": ".github/prompts/bloco4-adicionar-status.prompt.md",
            },
            {
                "desc": "Prompt Bloco 6 — descrição automática de PR",
                "tipo": "arquivo_existe",
                "arquivo": ".github/prompts/bloco6-descricao-pr.prompt.md",
            },
        ],
    },
    {
        "id": "coding_agent",
        "label": "Coding Agent",
        "descricao": "Agente autônomo que opera sobre o repositório com instruções estruturadas",
        "icone": "⚙️",
        "checks": [
            {
                "desc": "AGENTS.md presente (instrui o Coding Agent)",
                "tipo": "arquivo_existe",
                "arquivo": "AGENTS.md",
            },
            {
                "desc": "AGENTS.md define regras de geração de código",
                "tipo": "presenca_texto",
                "arquivo": "AGENTS.md",
                "pattern": r"fix mínimo|Preserve|nunca",
            },
            {
                "desc": "CI workflow configurado (build + test automático)",
                "tipo": "arquivo_existe",
                "arquivo": ".github/workflows/ci.yml",
            },
            {
                "desc": "Workflow CI executa dotnet test",
                "tipo": "presenca_texto",
                "arquivo": ".github/workflows/ci.yml",
                "pattern": r"dotnet test",
            },
        ],
    },
    {
        "id": "cli",
        "label": "CLI",
        "descricao": "GitHub Copilot CLI para diagnóstico e suporte direto no terminal",
        "icone": "💻",
        "checks": [
            {
                "desc": "GitHub CLI (gh) instalado",
                "tipo": "comando_disponivel",
                "comando": ["gh", "--version"],
            },
            {
                "desc": "gh copilot disponível (built-in ou extensão)",
                "tipo": "presenca_saida_comando",
                "comando": ["gh", "help", "copilot"],
                "pattern": r"Copilot|copilot",
            },
        ],
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# Executores de check
# ─────────────────────────────────────────────────────────────────────────────

def _arquivo_existe(arquivo: str) -> tuple[bool, str]:
    caminho = os.path.join(ROOT, arquivo.replace("/", os.sep))
    if os.path.exists(caminho):
        return True, arquivo
    return False, f"{arquivo} não encontrado"


def _presenca_texto(arquivo: str, pattern: str) -> tuple[bool, str]:
    caminho = os.path.join(ROOT, arquivo.replace("/", os.sep))
    if not os.path.exists(caminho):
        return False, f"{arquivo} não encontrado"
    with open(caminho, encoding="utf-8") as f:
        conteudo = f.read()
    if re.search(pattern, conteudo, re.IGNORECASE | re.MULTILINE):
        return True, f"padrão encontrado em {arquivo}"
    return False, f"padrão ausente em {arquivo}"


def _comando_disponivel(comando: list[str]) -> tuple[bool, str]:
    try:
        r = subprocess.run(comando, capture_output=True, text=True, timeout=8,
                           stdin=subprocess.DEVNULL)
        if r.returncode == 0:
            versao = (r.stdout + r.stderr).strip().splitlines()[0]
            return True, versao[:80]
        return False, f"exit code {r.returncode}"
    except FileNotFoundError:
        return False, f"'{comando[0]}' não encontrado no PATH"
    except subprocess.TimeoutExpired:
        return False, "timeout ao executar comando"


def _presenca_saida_comando(comando: list[str], pattern: str) -> tuple[bool, str]:
    try:
        r = subprocess.run(comando, capture_output=True, text=True, timeout=8,
                           stdin=subprocess.DEVNULL)
        saida = r.stdout + r.stderr
        if re.search(pattern, saida, re.IGNORECASE):
            linha = saida.strip().splitlines()[0][:80] if saida.strip() else "ok"
            return True, linha
        return False, f"comando executou mas saída não corresponde ao esperado"
    except FileNotFoundError:
        return False, f"'{comando[0]}' não encontrado no PATH"
    except subprocess.TimeoutExpired:
        return False, "timeout (execute: gh copilot --version para verificar)"


def executar_check(check: dict) -> dict:
    tipo = check["tipo"]
    if tipo == "arquivo_existe":
        passou, detalhe = _arquivo_existe(check["arquivo"])
    elif tipo == "presenca_texto":
        passou, detalhe = _presenca_texto(check["arquivo"], check["pattern"])
    elif tipo == "presenca_saida_comando":
        passou, detalhe = _presenca_saida_comando(check["comando"], check["pattern"])
    elif tipo == "comando_disponivel":
        passou, detalhe = _comando_disponivel(check["comando"])
    else:
        passou, detalhe = False, f"tipo desconhecido: {tipo}"
    return {"desc": check["desc"], "passou": passou, "detalhe": detalhe}


def executar_pilar(pilar: dict) -> dict:
    resultados = [executar_check(c) for c in pilar["checks"]]
    aprovado = all(r["passou"] for r in resultados)
    return {**pilar, "resultados": resultados, "aprovado": aprovado}

# ─────────────────────────────────────────────────────────────────────────────
# Geração do HTML
# ─────────────────────────────────────────────────────────────────────────────

def _codigo_unico(nome: str, turma: str, timestamp: str) -> str:
    raw = f"{nome}|{turma}|{timestamp}"
    return "BV-" + hashlib.sha256(raw.encode()).hexdigest()[:8].upper()


def _git_branch() -> str:
    try:
        r = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                           capture_output=True, text=True, cwd=ROOT)
        return r.stdout.strip()
    except Exception:
        return "—"


def _git_commit() -> str:
    try:
        r = subprocess.run(["git", "log", "-1", "--format=%h — %s"],
                           capture_output=True, text=True, cwd=ROOT)
        return r.stdout.strip()[:72]
    except Exception:
        return "—"


def gerar_html(nome: str, turma: str, pilares_resultado: list[dict],
               aprovado_geral: bool, timestamp: str) -> str:
    codigo = _codigo_unico(nome, turma, timestamp)
    ts_display = datetime.strptime(timestamp, "%Y%m%d_%H%M%S").strftime("%d/%m/%Y às %H:%M:%S")
    branch = _git_branch()
    commit = _git_commit()

    total_pilares = len(pilares_resultado)
    pilares_ok = sum(1 for p in pilares_resultado if p["aprovado"])
    total_checks = sum(len(p["resultados"]) for p in pilares_resultado)
    checks_ok = sum(sum(1 for r in p["resultados"] if r["passou"]) for p in pilares_resultado)
    pct = round(checks_ok / total_checks * 100) if total_checks else 0

    status_label = "GOVERNANÇA COMPLETA" if aprovado_geral else "GOVERNANÇA INCOMPLETA"
    status_cls = "aprovado" if aprovado_geral else "pendente"
    pct_color = "#2da44e" if aprovado_geral else "#f59e0b"

    # ── Grid compacto dos 8 pilares (para screenshot) ──────────────────────
    grid_html = ""
    for p in pilares_resultado:
        ok = p["aprovado"]
        n_ok = sum(1 for r in p["resultados"] if r["passou"])
        n_total = len(p["resultados"])
        cell_cls = "cell-ok" if ok else "cell-fail"
        tick = "✓" if ok else "✗"
        tick_cls = "tick-ok" if ok else "tick-fail"
        grid_html += (
            f'<div class="pcell {cell_cls}">'
            f'  <div class="pcell-top">'
            f'    <span class="picone">{p["icone"]}</span>'
            f'    <span class="{tick_cls}">{tick}</span>'
            f'  </div>'
            f'  <div class="pcell-label">{p["label"]}</div>'
            f'  <div class="pcell-checks">{n_ok}/{n_total} checks</div>'
            f'</div>'
        )

    # ── Detalhes expansíveis (abaixo da área de screenshot) ────────────────
    details_html = ""
    for p in pilares_resultado:
        ok = p["aprovado"]
        det_cls = "det-ok" if ok else "det-fail"
        rows = ""
        for r in p["resultados"]:
            ci = "✔" if r["passou"] else "✘"
            ci_cls = "dci-ok" if r["passou"] else "dci-fail"
            det = f' <span class="dci-det">→ {r["detalhe"]}</span>' if not r["passou"] else ""
            rows += (
                f'<div class="dcheck">'
                f'<span class="{ci_cls}">{ci}</span>'
                f'<span>{r["desc"]}{det}</span>'
                f'</div>'
            )
        details_html += f"""
      <details class="det-block {det_cls}">
        <summary>
          <span class="det-icone">{p["icone"]}</span>
          <strong>{p["label"]}</strong>
          <span class="det-sub">{p["descricao"]}</span>
          <span class="det-badge {'db-ok' if ok else 'db-fail'}">{'Configurado' if ok else 'Incompleto'}</span>
        </summary>
        <div class="det-rows">{rows}</div>
      </details>"""

    meta_json = json.dumps({
        "nome": nome, "turma": turma, "aprovado": aprovado_geral,
        "codigo": codigo, "timestamp": timestamp, "branch": branch,
    })

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Evidência · {nome} · Workshop Copilot Fase 2</title>
  <script id="evidencia-meta" type="application/json">{meta_json}</script>
  <style>
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
          background:#f0f2f5;padding:1.5rem 1rem}}

    /* ── CARD SCREENSHOT (tudo acima do fold) ─────────────────────── */
    .card{{width:820px;margin:0 auto;border-radius:14px;overflow:hidden;
           box-shadow:0 4px 24px rgba(0,0,0,.13)}}

    /* cabeçalho */
    .hd{{background:linear-gradient(135deg,#0d1117 0%,#161b22 55%,#1e2d3d 100%);
         color:#fff;padding:1.4rem 2rem 1.2rem;position:relative;overflow:hidden}}
    .hd::before{{content:"";position:absolute;right:-50px;top:-50px;
                 width:200px;height:200px;border-radius:50%;
                 background:radial-gradient(circle,rgba(88,166,255,.12) 0%,transparent 70%)}}
    .hd-row1{{display:flex;align-items:center;justify-content:space-between;margin-bottom:.9rem}}
    .brand{{font-size:.65rem;font-weight:700;letter-spacing:.16em;
            text-transform:uppercase;color:#58a6ff}}
    .fase-tag{{font-size:.62rem;border:1px solid rgba(88,166,255,.35);color:#58a6ff;
               padding:.2rem .75rem;border-radius:100px;letter-spacing:.08em;text-transform:uppercase}}
    .hd-row2{{display:flex;align-items:flex-end;justify-content:space-between;gap:1rem}}
    .hd-left{{flex:1;min-width:0}}
    .hd-pretitulo{{font-size:.72rem;color:rgba(255,255,255,.38);margin-bottom:.25rem}}
    .hd-nome{{font-size:1.7rem;font-weight:900;letter-spacing:-.025em;
              white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
    .hd-meta{{margin-top:.5rem;display:flex;flex-wrap:wrap;gap:.9rem}}
    .hd-meta span{{font-size:.7rem;color:rgba(255,255,255,.38)}}
    .hd-meta strong{{color:rgba(255,255,255,.7);font-weight:600}}
    .hd-right{{text-align:right;flex-shrink:0}}
    .pct-big{{font-size:3rem;font-weight:900;line-height:1;color:{pct_color}}}
    .pct-label{{font-size:.65rem;color:rgba(255,255,255,.35);margin-top:.15rem}}

    /* faixa de status */
    .sbar{{display:flex;align-items:center;gap:.75rem;padding:.8rem 2rem}}
    .sbar.aprovado{{background:#e6ffed;border-bottom:2px solid #2da44e}}
    .sbar.pendente{{background:#fff8e1;border-bottom:2px solid #f59e0b}}
    .sbar-dot{{width:10px;height:10px;border-radius:50%;flex-shrink:0}}
    .aprovado .sbar-dot{{background:#2da44e}}
    .pendente .sbar-dot{{background:#f59e0b}}
    .sbar-label{{font-size:.82rem;font-weight:800}}
    .aprovado .sbar-label{{color:#1a7f37}}
    .pendente .sbar-label{{color:#b45309}}
    .sbar-sep{{color:#ccc;font-size:.8rem}}
    .sbar-sub{{font-size:.78rem;color:#666}}
    .sbar-codigo{{margin-left:auto;font-family:monospace;font-size:.68rem;
                  color:#aaa;white-space:nowrap}}

    /* grid 4×2 dos pilares */
    .pgrid{{background:#fff;padding:1.1rem 2rem 1.3rem;
            display:grid;grid-template-columns:repeat(4,1fr);gap:.6rem}}
    .pcell{{border:1px solid #e8e8e8;border-radius:9px;padding:.7rem .8rem;
            display:flex;flex-direction:column;gap:.25rem}}
    .cell-ok{{border-top:3px solid #2da44e;background:#fafffe}}
    .cell-fail{{border-top:3px solid #cf222e;background:#fffafa}}
    .pcell-top{{display:flex;align-items:center;justify-content:space-between}}
    .picone{{font-size:1.1rem}}
    .tick-ok{{font-size:1rem;font-weight:900;color:#2da44e}}
    .tick-fail{{font-size:1rem;font-weight:900;color:#cf222e}}
    .pcell-label{{font-size:.82rem;font-weight:700;color:#24292f}}
    .pcell-checks{{font-size:.7rem;color:#888}}

    /* rodapé do card */
    .card-footer{{background:#f6f8fa;padding:.55rem 2rem;border-top:1px solid #e8e8e8;
                  display:flex;align-items:center;justify-content:space-between}}
    .cf-left{{font-size:.68rem;color:#aaa}}
    .cf-right{{font-size:.68rem;color:#aaa;font-style:italic}}

    /* ── DETALHES (abaixo do fold — não aparece no print) ─────────── */
    .details-section{{width:820px;margin:1.5rem auto 0}}
    .details-title{{font-size:.7rem;font-weight:700;letter-spacing:.1em;
                    text-transform:uppercase;color:#888;margin-bottom:.8rem;
                    padding-left:.2rem}}
    .det-block{{border:1px solid #e8e8e8;border-radius:9px;margin-bottom:.5rem;
                overflow:hidden}}
    .det-ok summary{{background:#f6fffe}}
    .det-fail summary{{background:#fff5f5}}
    .det-block summary{{padding:.7rem 1rem;cursor:pointer;display:flex;
                        align-items:center;gap:.6rem;list-style:none;
                        font-size:.83rem}}
    .det-block summary::-webkit-details-marker{{display:none}}
    .det-block summary::before{{content:"▶";font-size:.6rem;color:#aaa;
                                transition:transform .15s;flex-shrink:0}}
    .det-block[open] summary::before{{transform:rotate(90deg)}}
    .det-icone{{font-size:1rem}}
    .det-sub{{flex:1;font-size:.75rem;color:#888;min-width:0;
              overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
    .det-badge{{font-size:.65rem;font-weight:700;padding:.15rem .6rem;
                border-radius:100px;flex-shrink:0}}
    .db-ok{{background:#e6ffed;color:#1a7f37}}
    .db-fail{{background:#ffebe9;color:#cf222e}}
    .det-rows{{padding:.5rem 1rem .8rem 2.5rem;display:flex;flex-direction:column;gap:.3rem;
               border-top:1px solid #f0f0f0}}
    .dcheck{{display:flex;gap:.5rem;font-size:.78rem;color:#444;line-height:1.4}}
    .dci-ok{{color:#2da44e;font-weight:700;flex-shrink:0}}
    .dci-fail{{color:#cf222e;font-weight:700;flex-shrink:0}}
    .dci-det{{color:#cf222e;font-size:.73rem}}

    @media print{{
      body{{background:#fff;padding:0}}
      .card{{box-shadow:none;width:100%}}
      .details-section{{display:none}}
    }}
  </style>
</head>
<body>

<!-- ═══════════════════════════════════════════════════════════════════
     CARD — tire o screenshot desta área (acima da linha de detalhes)
     ═══════════════════════════════════════════════════════════════════ -->
<div class="card">
  <div class="hd">
    <div class="hd-row1">
      <div class="brand">Farmácia Boa Vista · GitHub Copilot Workshop</div>
      <div class="fase-tag">Fase 2 — Avançado</div>
    </div>
    <div class="hd-row2">
      <div class="hd-left">
        <div class="hd-pretitulo">Evidência de Conclusão — Platform Extensibility</div>
        <div class="hd-nome">{nome}</div>
        <div class="hd-meta">
          <span>Time: <strong>{turma.capitalize()}</strong></span>
          <span>Branch: <strong>{branch}</strong></span>
          <span>Gerado em: <strong>{ts_display}</strong></span>
          <span>Commit: <strong>{commit}</strong></span>
        </div>
      </div>
      <div class="hd-right">
        <div class="pct-big">{pct}%</div>
        <div class="pct-label">{checks_ok}/{total_checks} checks</div>
      </div>
    </div>
  </div>

  <div class="sbar {status_cls}">
    <div class="sbar-dot"></div>
    <div class="sbar-label">{status_label}</div>
    <div class="sbar-sep">·</div>
    <div class="sbar-sub">{pilares_ok} de {total_pilares} pilares configurados</div>
    <div class="sbar-codigo">{codigo}</div>
  </div>

  <div class="pgrid">{grid_html}</div>

  <div class="card-footer">
    <span class="cf-left">PDV API — Farmácia Boa Vista · GitHub Copilot Workshop Fase 2</span>
    <span class="cf-right">Clique nos pilares abaixo para ver detalhes</span>
  </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════════
     DETALHES — abaixo do fold, não precisa entrar no screenshot
     ═══════════════════════════════════════════════════════════════════ -->
<div class="details-section">
  <div class="details-title">Detalhes das verificações</div>
  {details_html}
</div>

<script id="evidencia-meta" type="application/json">{meta_json}</script>
</body>
</html>"""

# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Gera evidência individual de governança do workshop."
    )
    parser.add_argument("--nome", required=True,
                        help='Nome completo do participante (ex: "João Silva")')
    parser.add_argument("--turma", required=True, choices=["dev", "qa", "suporte"],
                        help="Turma: dev | qa | suporte")
    args = parser.parse_args()

    nome = args.nome.strip()
    turma = args.turma

    print(f"\n{'='*58}")
    print(f"  GitHub Copilot Platform Extensibility")
    print(f"  Participante : {nome}")
    print(f"  Turma        : feature/{turma}")
    print(f"{'='*58}\n")

    pilares_resultado = []
    for pilar in PILARES:
        print(f"  {pilar['icone']}  {pilar['label']}")
        resultado = executar_pilar(pilar)
        for r in resultado["resultados"]:
            icon = "  ✔" if r["passou"] else "  ✘"
            print(f"    {icon}  {r['desc']}")
            if not r["passou"]:
                print(f"         → {r['detalhe']}")
        print(f"  └─ {'CONFIGURADO ✅' if resultado['aprovado'] else 'INCOMPLETO ⚠️'}\n")
        pilares_resultado.append(resultado)

    aprovado_geral = all(p["aprovado"] for p in pilares_resultado)
    pilares_ok = sum(1 for p in pilares_resultado if p["aprovado"])
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    os.makedirs(os.path.join(ROOT, "evidencias"), exist_ok=True)
    nome_slug = re.sub(r"[^a-z0-9]", "-", nome.lower()).strip("-")
    nome_arquivo = f"turma-{turma}-{nome_slug}.html"
    caminho = os.path.join(ROOT, "evidencias", nome_arquivo)

    html = gerar_html(nome, turma, pilares_resultado, aprovado_geral, timestamp)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"{'='*58}")
    print(f"  {'✅ GOVERNANÇA COMPLETA' if aprovado_geral else '⚠️  GOVERNANÇA INCOMPLETA'}")
    print(f"  Pilares OK: {pilares_ok}/{len(pilares_resultado)}")
    print(f"  Arquivo   : evidencias/{nome_arquivo}")
    print(f"{'='*58}\n")

    webbrowser.open(f"file:///{caminho.replace(os.sep, '/')}")


if __name__ == "__main__":
    main()
