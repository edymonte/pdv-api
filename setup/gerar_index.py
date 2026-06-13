#!/usr/bin/env python3
"""
PDV API — Farmácia Boa Vista
Gerador do Dashboard de Evidências (GitHub Pages / visualização local)

Varre evidencias/turma-*.html, extrai metadados e gera evidencias/index.html
com o painel consolidado das 3 turmas.

Uso:
    python setup/gerar_index.py
"""

import glob
import json
import os
import re
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVIDENCIAS_DIR = os.path.join(ROOT, "evidencias")

TURMAS_INFO = {
    "dev":     {"label": "Time Dev",     "branch": "feature/dev"},
    "qa":      {"label": "Time QA",      "branch": "feature/qa"},
    "suporte": {"label": "Time Suporte", "branch": "feature/suporte"},
}

# ─────────────────────────────────────────────────────────────────────────────
# Extração de metadados
# ─────────────────────────────────────────────────────────────────────────────

def extrair_meta(caminho: str) -> dict | None:
    try:
        with open(caminho, encoding="utf-8") as f:
            conteudo = f.read()
        match = re.search(
            r'<script id="evidencia-meta" type="application/json">([^<]+)</script>',
            conteudo,
        )
        if not match:
            return None
        return json.loads(match.group(1))
    except (OSError, json.JSONDecodeError):
        return None


def coletar_evidencias() -> list[dict]:
    # Ignora index.html, coleta turma-*.html individuais
    pattern = os.path.join(EVIDENCIAS_DIR, "turma-*.html")
    arquivos = sorted(glob.glob(pattern))
    resultado = []
    for caminho in arquivos:
        if os.path.basename(caminho) == "index.html":
            continue
        meta = extrair_meta(caminho)
        if meta is None:
            continue
        meta["arquivo"] = os.path.basename(caminho)
        try:
            meta["ts_formatado"] = datetime.strptime(
                meta["timestamp"], "%Y%m%d_%H%M%S"
            ).strftime("%d/%m/%Y %H:%M")
        except (KeyError, ValueError):
            meta["ts_formatado"] = "—"
        resultado.append(meta)
    # Ordena por turma e depois nome
    return sorted(resultado, key=lambda e: (e.get("turma", ""), e.get("nome", "").lower()))

# ─────────────────────────────────────────────────────────────────────────────
# Geração do HTML do dashboard
# ─────────────────────────────────────────────────────────────────────────────

def gerar_html(evidencias: list[dict]) -> str:
    total = len(evidencias)
    aprovados = sum(1 for e in evidencias if e.get("aprovado"))
    pendentes = total - aprovados
    pct = round(aprovados / total * 100) if total > 0 else 0
    gerado_em = datetime.now().strftime("%d/%m/%Y %H:%M")

    # Cards por turma com lista de participantes
    cards_html = ""
    turmas_evidencias: dict[str, list] = {}
    for e in evidencias:
        turmas_evidencias.setdefault(e.get("turma", "?"), []).append(e)

    for key, info in TURMAS_INFO.items():
        participantes = turmas_evidencias.get(key, [])
        total_t = len(participantes)
        aprov_t = sum(1 for e in participantes if e.get("aprovado"))

        if participantes:
            badge_cls = "badge-ok" if aprov_t == total_t else "badge-pend"
            badge_label = f"{aprov_t}/{total_t} aprovados"
        else:
            badge_cls = "badge-none"
            badge_label = "Aguardando"

        partic_html = ""
        for e in participantes:
            ok = e.get("aprovado", False)
            p_cls = "p-ok" if ok else "p-pend"
            p_icon = "✔" if ok else "✘"
            partic_html += (
                f'<div class="partic {p_cls}">'
                f'<span class="p-icon">{p_icon}</span>'
                f'<a href="{e["arquivo"]}" target="_blank">{e.get("nome","—")}</a>'
                f'<span class="p-ts">{e.get("ts_formatado","—")}</span>'
                f'</div>'
            )
        if not partic_html:
            partic_html = '<div class="partic-none">Nenhuma evidência gerada</div>'

        cards_html += f"""
        <div class="tcard">
          <div class="tcard-top">
            <div class="tcard-label">{info["label"]}</div>
            <span class="badge {badge_cls}">{badge_label}</span>
          </div>
          <div class="tcard-branch">{info["branch"]}</div>
          <div class="partic-list">{partic_html}</div>
        </div>"""

    # Linhas da tabela detalhada
    linhas_html = ""
    for e in evidencias:
        aprovado = e.get("aprovado", False)
        sc = "badge-ok" if aprovado else "badge-pend"
        sl = "Aprovado" if aprovado else "Pendente"
        turma = e.get("turma", "—")
        info = TURMAS_INFO.get(turma, {"label": turma, "branch": "—"})
        linhas_html += f"""
        <tr>
          <td>{e.get("nome","—")}</td>
          <td>{info["label"]}</td>
          <td><code>{e.get("branch", info["branch"])}</code></td>
          <td><span class="badge {sc}">{sl}</span></td>
          <td>{e.get("ts_formatado", "—")}</td>
          <td><code>{e.get("codigo", "—")}</code></td>
          <td><a href="{e.get("arquivo","#")}" target="_blank">↗ abrir</a></td>
        </tr>"""

    if not linhas_html:
        linhas_html = '<tr><td colspan="7" style="text-align:center;color:#aaa;padding:2rem">Nenhuma evidência gerada ainda.</td></tr>'

    pct_color = "#2da44e" if pct >= 70 else "#f59e0b"

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dashboard de Evidências — Workshop Copilot · Fase 2</title>
  <style>
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
          background:#eef2f7;min-height:100vh;padding:2rem 1rem}}
    .container{{max-width:960px;margin:0 auto}}
    .hd{{background:linear-gradient(135deg,#0d1117 0%,#161b22 60%,#1a2332 100%);
         color:#fff;border-radius:16px 16px 0 0;padding:2rem 2.5rem 1.5rem}}
    .brand{{font-size:.7rem;font-weight:700;letter-spacing:.18em;
            text-transform:uppercase;color:#58a6ff;margin-bottom:.5rem}}
    .hd-titulo{{font-size:1.6rem;font-weight:800;margin-bottom:.3rem}}
    .hd-sub{{font-size:.85rem;color:rgba(255,255,255,.45)}}
    .stats-bar{{background:#161b22;padding:1.2rem 2.5rem;
                display:flex;gap:2.5rem;flex-wrap:wrap;
                border-bottom:1px solid rgba(255,255,255,.08)}}
    .stat{{display:flex;flex-direction:column;gap:.2rem}}
    .stat-val{{font-size:1.6rem;font-weight:800;color:#fff}}
    .stat-val.green{{color:#3fb950}}
    .stat-val.orange{{color:#f59e0b}}
    .stat-label{{font-size:.72rem;color:rgba(255,255,255,.35);text-transform:uppercase;letter-spacing:.1em}}
    .pct-bar{{margin-top:.4rem;height:4px;width:80px;background:rgba(255,255,255,.1);border-radius:2px}}
    .pct-fill{{height:100%;border-radius:2px;background:{pct_color};width:{pct}%}}
    .body{{background:#fff;padding:2rem 2.5rem;border-radius:0 0 16px 16px}}
    h3{{font-size:1rem;font-weight:700;color:#24292f;margin-bottom:1rem;
        padding-bottom:.5rem;border-bottom:1px solid #e8e8e8}}
    .cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));
             gap:1rem;margin-bottom:2rem}}
    .tcard{{border:1px solid #e8e8e8;border-radius:10px;padding:1rem 1.2rem}}
    .tcard-top{{display:flex;align-items:center;justify-content:space-between;margin-bottom:.4rem}}
    .tcard-label{{font-weight:700;font-size:.95rem;color:#24292f}}
    .tcard-branch{{font-family:monospace;font-size:.78rem;color:#57606a;margin-bottom:.6rem}}
    .partic-list{{display:flex;flex-direction:column;gap:.3rem}}
    .partic{{display:flex;align-items:center;gap:.5rem;font-size:.82rem}}
    .partic a{{color:#0969da;text-decoration:none;flex:1}}
    .partic a:hover{{text-decoration:underline}}
    .p-ok .p-icon{{color:#2da44e;font-weight:700}}
    .p-pend .p-icon{{color:#cf222e;font-weight:700}}
    .p-ts{{font-size:.72rem;color:#aaa;white-space:nowrap}}
    .partic-none{{font-size:.8rem;color:#aaa;font-style:italic}}
    .badge{{font-size:.72rem;font-weight:700;padding:.2rem .65rem;border-radius:100px}}
    .badge-ok{{background:#e6ffed;color:#1a7f37}}
    .badge-pend{{background:#fff8e1;color:#b45309}}
    .badge-none{{background:#f6f8fa;color:#888}}
    table{{width:100%;border-collapse:collapse;font-size:.85rem}}
    th{{text-align:left;padding:.6rem .5rem;border-bottom:2px solid #e8e8e8;
        font-size:.75rem;color:#57606a;text-transform:uppercase;letter-spacing:.05em}}
    td{{padding:.65rem .5rem;border-bottom:1px solid #f0f0f0;vertical-align:middle}}
    tr:last-child td{{border-bottom:none}}
    code{{font-size:.78rem;background:#f6f8fa;padding:.15rem .4rem;border-radius:4px}}
    a{{color:#0969da;text-decoration:none}}
    .footer{{text-align:center;font-size:.75rem;color:#aaa;margin-top:1.5rem}}
  </style>
</head>
<body>
<div class="container">
  <div class="hd">
    <div class="brand">Farmácia Boa Vista · Workshop GitHub Copilot</div>
    <div class="hd-titulo">Dashboard de Evidências — Fase 2</div>
    <div class="hd-sub">Gerado em {gerado_em}</div>
  </div>
  <div class="stats-bar">
    <div class="stat">
      <div class="stat-val">{total}</div>
      <div class="stat-label">Turmas</div>
    </div>
    <div class="stat">
      <div class="stat-val green">{aprovados}</div>
      <div class="stat-label">Aprovadas</div>
    </div>
    <div class="stat">
      <div class="stat-val orange">{pendentes}</div>
      <div class="stat-label">Pendentes</div>
    </div>
    <div class="stat">
      <div class="stat-val" style="color:{pct_color}">{pct}%</div>
      <div class="stat-label">Aprovação</div>
      <div class="pct-bar"><div class="pct-fill"></div></div>
    </div>
  </div>
  <div class="body">
    <h3>Situação por Time</h3>
    <div class="cards">{cards_html}</div>

    <h3>Histórico de Evidências</h3>
    <table>
      <thead>
        <tr>
          <th>Participante</th><th>Time</th><th>Branch</th><th>Status</th>
          <th>Gerado em</th><th>Código</th><th>Evidência</th>
        </tr>
      </thead>
      <tbody>{linhas_html}</tbody>
    </table>
  </div>
  <div class="footer">PDV API — Farmácia Boa Vista · GitHub Copilot Workshop Fase 2</div>
</div>
</body>
</html>"""

# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    import webbrowser
    evidencias = coletar_evidencias()
    os.makedirs(EVIDENCIAS_DIR, exist_ok=True)
    caminho = os.path.join(EVIDENCIAS_DIR, "index.html")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(gerar_html(evidencias))

    aprovados = sum(1 for e in evidencias if e.get("aprovado"))
    print(f"\nDashboard gerado: evidencias/index.html")
    print(f"Turmas com evidência: {len(evidencias)}/3 | Aprovadas: {aprovados}/{len(evidencias)}\n")
    webbrowser.open(f"file:///{caminho.replace(os.sep, '/')}")


if __name__ == "__main__":
    main()
