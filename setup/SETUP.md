# Setup do Ambiente — pdv-api Workshop

## Pré-requisitos (instale uma vez)

| # | O que instalar | Link | Observação |
|---|---|---|---|
| 1 | **.NET 8 SDK** | https://dotnet.microsoft.com/download/dotnet/8 | Verifique com `dotnet --version` |
| 2 | **VS Code** | https://code.visualstudio.com | Aceite instalar as extensões recomendadas ao abrir |
| 3 | **Node.js LTS** | https://nodejs.org | Necessário para o servidor MCP SQLite |
| 4 | **SQLite3** | https://sqlite.org/download.html | Para criar o banco do catálogo |
| 5 | **Git** | https://git-scm.com | Para clonar e gerenciar branches |

## Branches por time

O workshop usa 3 branches — uma por time. O apresentador cria antes de começar:

```bash
git checkout main
git checkout -b feature/dev
git push -u origin feature/dev

git checkout main
git checkout -b feature/qa
git push -u origin feature/qa

git checkout main
git checkout -b feature/suporte
git push -u origin feature/suporte

git checkout main   # volta para main para a demo
```

Cada time trabalha na sua branch. No final, o apresentador (ou cada time) gera a evidência:

```bash
# Na branch do time (ex: feature/dev)
git checkout feature/dev
python setup/gerar_evidencia.py --turma dev

# Repita para os demais:
git checkout feature/qa    && python setup/gerar_evidencia.py --turma qa
git checkout feature/suporte && python setup/gerar_evidencia.py --turma suporte

# Dashboard consolidado (pode rodar de qualquer branch)
python setup/gerar_index.py
```

Os HTMLs são gerados em `evidencias/` e abertos automaticamente no navegador.

---

## Inicializar o ambiente (fazer uma vez antes da primeira turma)

```bash
# 1. Clone o repositório
git clone https://github.com/bvista-dev/pdv-api.git
cd pdv-api

# 2. Restaure os pacotes .NET
dotnet restore

# 3. Verifique que o build passa
dotnet build

# 4. Verifique que os testes passam
dotnet test

# 5. Crie o banco de catálogo de produtos (MCP — Bloco 3)
sqlite3 db/catalogo-produtos.db < db/setup-catalogo.sql

# 6. Crie a branch demo/sem-padrao (Bloco 1 — gerar uma vez, reutilizar nas 6 turmas)
git checkout -b demo/sem-padrao
# → execute o Prompt do Bloco 1 aqui, dê commit, volte para main
git checkout main
```

## Reset entre turmas

```bash
# Windows:
pwsh -File setup\reset-ambiente.ps1

# Linux/Mac:
bash setup/reset-ambiente.sh
```

O script reseta para `origin/main`, recria o banco SQLite, verifica build e testes.

## Checklist pré-workshop

- [ ] Branches `feature/dev`, `feature/qa`, `feature/suporte` criadas e pushed
- [ ] `dotnet build` passa sem erros
- [ ] `dotnet test` — todos os testes passando
- [ ] Banco `db/catalogo-produtos.db` criado (produto id=5 está inativo)
- [ ] Branch `demo/sem-padrao` criada com o código do Bloco 1 sem instructions
- [ ] MCP server SQLite testado no Agent Mode: "liste os produtos do catálogo"
- [ ] Hook `build-guard.json` configurado no Copilot
- [ ] Prompts dos blocos abertos em abas no VS Code para fácil acesso
- [ ] Script `gerar_evidencia.py` testado em pelo menos uma branch (`python setup/gerar_evidencia.py --turma dev`)
