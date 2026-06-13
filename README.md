# PDV API — Farmácia Boa Vista
## Repositório do Workshop GitHub Copilot — Fase 2

Sistema de ponto de venda (PDV) da Farmácia Boa Vista.
Usado como cenário do **GitHub Copilot Workshop — "Agente Autônomo"**.

---

## Prepare o ambiente em 3 passos

### Pré-requisitos (instale uma vez)

| # | O que instalar | Link |
|---|---|---|
| 1 | **.NET 8 SDK** | https://dotnet.microsoft.com/download/dotnet/8 |
| 2 | **VS Code** | https://code.visualstudio.com |
| 3 | **Node.js LTS** | https://nodejs.org |
| 4 | **SQLite3** | https://sqlite.org/download.html |

> **GitHub Copilot:** você precisa de uma licença ativa.

### Iniciar

```bash
git clone https://github.com/bvista-dev/pdv-api.git
cd pdv-api
dotnet restore && dotnet build && dotnet test
sqlite3 db/catalogo-produtos.db < db/setup-catalogo.sql
```

Consulte [setup/SETUP.md](setup/SETUP.md) para o checklist completo.

---

## Estrutura do projeto

```
pdv-api/
├── .github/
│   ├── copilot-instructions.md        ← padrões do time (Bloco 2)
│   ├── instructions/                  ← instructions específicas por contexto
│   ├── skills/gerar-testes-pdv/       ← skill de testes xUnit (Bloco 2)
│   ├── agents/qa-boa-vista.agent.md   ← custom agent revisor QA (Bloco 5)
│   ├── hooks/build-guard.json         ← hook de autocorreção (Bloco 4)
│   ├── prompts/                       ← prompts prontos para cada bloco
│   ├── workflows/ci.yml               ← CI build + test
│   └── WORKSHOP_CONTEXT.md            ← contexto completo para retomar sessão
├── .vscode/
│   └── mcp.json                       ← MCP catálogo de produtos (Bloco 3)
├── src/PdvApi/                        ← código da API (.NET 8)
├── tests/PdvApi.Tests/                ← testes xUnit
├── db/
│   └── setup-catalogo.sql             ← script do banco SQLite (MCP)
└── setup/
    ├── SETUP.md
    ├── reset-ambiente.sh
    └── reset-ambiente.ps1
```

---

## Dois estados do repositório

O demo tem dois estados distintos — a transição entre eles É o workshop.

### Estado 1 — Sem governança (Bloco 1)
Quando você abre o repo, o `.github/` tem **apenas** o CI e o WORKSHOP_CONTEXT.  
O Copilot não tem instructions, skills, agents nem hooks.  
Execute o Prompt do Bloco 1 e mostre o código gerado sem regras → branch `demo/sem-padrao`.

### Estado 2 — Com governança (Blocos 2–8)
Rode o script de ativação para copiar as regras para o `.github/`:

```bash
# Windows:
pwsh -File setup\ativar-governanca.ps1

# Linux/Mac:
bash setup/ativar-governanca.sh
```

Abra um **novo chat do Copilot** após ativar (para o contexto ser recarregado).  
Agora execute o mesmo Prompt do Bloco 1 — a diferença é a revelação central do workshop.

### Reset entre turmas

```bash
pwsh -File setup\reset-ambiente.ps1   # Windows
bash setup/reset-ambiente.sh          # Linux/Mac
```

Remove a governança ativada, recria o banco SQLite, verifica build e testes.

---

## Roteiro do Workshop (resumo)

| Bloco | O que acontece | Estado do repo | Primitiva |
|---|---|---|---|
| 0 | Abertura — comparação com Kiro | Sem governança | — |
| 1 | Agente gera código **sem** regras | Sem governança | Agent Mode puro |
| **→** | **`ativar-governanca.ps1`** | **Transição ao vivo** | — |
| 2 | Mesma tarefa **com** instructions + skill | Com governança | Instructions + Skills |
| 3 | Agente consulta catálogo externo | Com governança | MCP |
| 4 ⭐ | Código quebra → agente se autocorrige | Com governança | Hooks |
| 5 | `@qa-boa-vista` revisa tudo | Com governança | Custom Agents |
| 6 | PR aberto com Code Review | Com governança | Copilot Code Review |
| 7 | Time N2 usa diagnóstico no terminal | Com governança | Copilot CLI |
| 8 | Antes × Depois + gancho para Challenge | — | — |

> Prompts prontos: [`governanca/.github/prompts/`](governanca/.github/prompts/)  
> Contexto completo: [`../contexto-completo/`](../contexto-completo/)
