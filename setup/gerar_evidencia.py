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
                "desc": "Extensão gh copilot instalada",
                "tipo": "presenca_saida_comando",
                "comando": ["gh", "extension", "list"],
                "pattern": r"copilot",
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
        r = subprocess.run(comando, capture_output=True, text=True, timeout=8)
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
        r = subprocess.run(comando, capture_output=True, text=True, timeout=8)
        saida = r.stdout + r.stderr
        if re.search(pattern, saida, re.IGNORECASE):
            return True, "encontrado na saída do comando"
        return False, "extensão não encontrada (execute: gh extension install github/gh-copilot)"
    except FileNotFoundError:
        return False, f"'{comando[0]}' não encontrado no PATH"
    except subprocess.TimeoutExpired:
        return False, "timeout ao executar comando"


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
    status_icon = "✓" if aprovado_geral else "✗"
    pct_color = "#2da44e" if aprovado_geral else "#f59e0b"

    cards_html = ""
    for p in pilares_resultado:
        ok = p["aprovado"]
        card_cls = "pilar-ok" if ok else "pilar-fail"
        badge_cls = "b-ok" if ok else "b-fail"
        badge_label = "Configurado" if ok else "Incompleto"
        checks_html = ""
        for r in p["resultados"]:
            ci = "✔" if r["passou"] else "✘"
            ci_cls = "ci-ok" if r["passou"] else "ci-fail"
            det = f' <span class="check-det">— {r["detalhe"]}</span>' if not r["passou"] else ""
            checks_html += (
                f'<div class="check-row">'
                f'<span class="{ci_cls}">{ci}</span>'
                f'<span class="check-desc">{r["desc"]}{det}</span>'
                f'</div>'
            )
        cards_html += f"""
        <div class="pilar-card {card_cls}">
          <div class="pilar-top">
            <span class="pilar-icone">{p["icone"]}</span>
            <div class="pilar-info">
              <div class="pilar-label">{p["label"]}</div>
              <div class="pilar-desc">{p["descricao"]}</div>
            </div>
            <span class="badge {badge_cls}">{badge_label}</span>
          </div>
          <div class="checks">{checks_html}</div>
        </div>"""

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
    body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
          background:#eef2f7;padding:2rem 1rem}}
    .page{{max-width:860px;margin:0 auto}}
    .hd{{background:linear-gradient(135deg,#0d1117 0%,#161b22 65%,#1a2332 100%);
         color:#fff;border-radius:16px 16px 0 0;padding:2rem 2.5rem 1.6rem;
         position:relative;overflow:hidden}}
    .hd::after{{content:"";position:absolute;right:-60px;top:-60px;width:220px;height:220px;
                border-radius:50%;background:rgba(88,166,255,.06)}}
    .hd-top{{display:flex;align-items:center;justify-content:space-between;margin-bottom:1.2rem}}
    .brand{{font-size:.68rem;font-weight:700;letter-spacing:.18em;
            text-transform:uppercase;color:#58a6ff}}
    .fase-badge{{font-size:.65rem;border:1px solid rgba(88,166,255,.4);
                 color:#58a6ff;padding:.25rem .9rem;border-radius:100px;
                 letter-spacing:.09em;text-transform:uppercase}}
    .hd-pretitulo{{font-size:.8rem;color:rgba(255,255,255,.4);margin-bottom:.3rem}}
    .hd-nome{{font-size:2rem;font-weight:900;letter-spacing:-.02em;margin-bottom:.25rem}}
    .hd-sub{{font-size:.85rem;color:rgba(255,255,255,.45)}}
    .hd-sub strong{{color:#fff}}
    .meta-strip{{display:flex;gap:1.5rem;margin-top:1.2rem;flex-wrap:wrap}}
    .meta-item{{font-size:.72rem;color:rgba(255,255,255,.35)}}
    .meta-item strong{{color:rgba(255,255,255,.65);font-weight:600}}
    .pillars-tagline{{margin-top:1rem;font-size:.73rem;color:rgba(88,166,255,.7);
                      letter-spacing:.04em}}
    .status-bar{{padding:1.1rem 2.5rem;display:flex;align-items:center;gap:1rem}}
    .status-bar.aprovado{{background:#e6ffed;border-bottom:3px solid #2da44e}}
    .status-bar.pendente{{background:#fff8e1;border-bottom:3px solid #f59e0b}}
    .s-icon{{width:42px;height:42px;border-radius:50%;display:flex;
             align-items:center;justify-content:center;font-size:1.3rem;
             font-weight:800;flex-shrink:0}}
    .aprovado .s-icon{{background:#2da44e;color:#fff}}
    .pendente .s-icon{{background:#f59e0b;color:#fff}}
    .s-texts{{flex:1}}
    .s-label{{font-size:1rem;font-weight:800}}
    .aprovado .s-label{{color:#1a7f37}}
    .pendente .s-label{{color:#b45309}}
    .s-sub{{font-size:.78rem;margin-top:.15rem}}
    .aprovado .s-sub{{color:#2da44e}}
    .pendente .s-sub{{color:#b45309}}
    .s-right{{text-align:right}}
    .s-pct{{font-size:1.8rem;font-weight:900;color:{pct_color}}}
    .s-codigo{{font-family:monospace;font-size:.7rem;color:#aaa;margin-top:.1rem}}
    .body{{background:#fff;padding:2rem 2.5rem;border-radius:0 0 16px 16px}}
    .section-title{{font-size:.7rem;font-weight:700;letter-spacing:.12em;
                    text-transform:uppercase;color:#57606a;margin-bottom:1.2rem;
                    display:flex;align-items:center;gap:.6rem}}
    .section-title::after{{content:"";flex:1;height:1px;background:#e8e8e8}}
    .pilares-grid{{display:grid;gap:.8rem}}
    .pilar-card{{border:1px solid #e8e8e8;border-radius:10px;padding:1rem 1.2rem}}
    .pilar-ok{{border-left:4px solid #2da44e}}
    .pilar-fail{{border-left:4px solid #cf222e}}
    .pilar-top{{display:flex;align-items:flex-start;gap:.9rem;margin-bottom:.7rem}}
    .pilar-icone{{font-size:1.25rem;flex-shrink:0;margin-top:.1rem}}
    .pilar-info{{flex:1;min-width:0}}
    .pilar-label{{font-weight:700;font-size:.95rem;color:#24292f;margin-bottom:.2rem}}
    .pilar-desc{{font-size:.77rem;color:#57606a;line-height:1.4}}
    .badge{{font-size:.7rem;font-weight:700;padding:.2rem .7rem;border-radius:100px;
            white-space:nowrap;flex-shrink:0}}
    .b-ok{{background:#e6ffed;color:#1a7f37}}
    .b-fail{{background:#ffebe9;color:#cf222e}}
    .checks{{display:flex;flex-direction:column;gap:.32rem;
             padding-top:.65rem;border-top:1px solid #f0f0f0}}
    .check-row{{display:flex;align-items:flex-start;gap:.55rem;font-size:.8rem;color:#444}}
    .ci-ok{{color:#2da44e;flex-shrink:0;margin-top:.05rem;font-weight:700}}
    .ci-fail{{color:#cf222e;flex-shrink:0;margin-top:.05rem;font-weight:700}}
    .check-desc{{line-height:1.4}}
    .check-det{{color:#cf222e;font-size:.75rem}}
    .footer{{text-align:center;font-size:.72rem;color:#aaa;
             margin-top:1.1rem;padding:.4rem 0}}
  </style>
</head>
<body>
<div class="page">
  <div class="hd">
    <div class="hd-top">
      <div class="brand">Farmácia Boa Vista · GitHub Copilot Workshop</div>
      <div class="fase-badge">Fase 2 — Avançado</div>
    </div>
    <div class="hd-pretitulo">Evidência de Conclusão — Platform Extensibility</div>
    <div class="hd-nome">{nome}</div>
    <div class="hd-sub">Time: <strong>{turma.capitalize()}</strong> &nbsp;·&nbsp; Branch: <strong>{branch}</strong></div>
    <div class="meta-strip">
      <div class="meta-item">Gerado em: <strong>{ts_display}</strong></div>
      <div class="meta-item">Último commit: <strong>{commit}</strong></div>
    </div>
    <div class="pillars-tagline">Instructions · Skills · Agents · MCP · Hooks · Knowledge Base · Coding Agent · CLI</div>
  </div>

  <div class="status-bar {status_cls}">
    <div class="s-icon">{status_icon}</div>
    <div class="s-texts">
      <div class="s-label">{status_label}</div>
      <div class="s-sub">{pilares_ok} de {total_pilares} pilares configurados &nbsp;·&nbsp; {checks_ok} de {total_checks} verificações aprovadas</div>
    </div>
    <div class="s-right">
      <div class="s-pct">{pct}%</div>
      <div class="s-codigo">{codigo}</div>
    </div>
  </div>

  <div class="body">
    <div class="section-title">Validação dos 8 Pilares</div>
    <div class="pilares-grid">{cards_html}</div>
  </div>

  <div class="footer">PDV API — Farmácia Boa Vista &nbsp;·&nbsp; GitHub Copilot Workshop Fase 2 &nbsp;·&nbsp; {codigo}</div>
</div>
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
