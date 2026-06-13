# 🏆 Challenge — GitHub Copilot Platform Extensibility
## Farmácia Boa Vista · Workshop Fase 2

> **Objetivo:** configurar os 8 pilares de governança do Copilot manualmente,
> executar cada bloco do workshop e gerar sua evidência de conclusão.
>
> O challenge termina quando você rodar `gerar_evidencia.py` e ver **8/8 pilares** no HTML.

---

## Antes de começar

### 1. Clone e configure o ambiente

```bash
git clone https://github.com/edymonte/pdv-api.git
cd pdv-api

# Windows:
setup.bat

# Linux / Mac:
bash setup.sh
```

O script verifica e instala automaticamente o que estiver faltando.

### 2. Faça checkout da branch do seu time

```bash
# Escolha a branch do seu time:
git checkout feature/dev       # Time Dev
git checkout feature/qa        # Time QA
git checkout feature/suporte   # Time Suporte
```

Leia o arquivo `SQUAD.md` que aparece — ele confirma que você está na branch certa.

### 3. Confirme que o projeto compila

```bash
dotnet restore
dotnet build
dotnet test
```

Você deve ver **3 testes passando**. Esse é o estado inicial — sem nenhuma governança.

---

## Os 8 Pilares — configure um a um

A pasta `governanca/.github/` contém todos os arquivos prontos.
**Você vai copiar cada um manualmente** para `.github/` — e entender o que cada arquivo faz antes de copiar.

---

### Pilar 1 — Instructions 📋

**O que é:** regras permanentes que o Copilot lê em **todo** contexto, automaticamente.
É o "combinado do time" — padrões de código, segurança, nomenclatura.

**Faça:**

```bash
# Cria as pastas necessárias
mkdir -p .github/instructions

# Copia o arquivo principal de instructions
cp governanca/.github/copilot-instructions.md .github/copilot-instructions.md

# Copia as instructions específicas por contexto
cp governanca/.github/instructions/testes.instructions.md .github/instructions/
cp governanca/.github/instructions/validacao.instructions.md .github/instructions/
```

**Abra os arquivos copiados e leia:**
- `copilot-instructions.md` — regras de arquitetura, segurança e commits
- `testes.instructions.md` — padrão `Should_X_When_Y`, AAA, FluentAssertions
- `validacao.instructions.md` — FluentValidation, mensagens em pt-BR

> 💡 **Por que importa:** sem isso, dois devs do time recebem sugestões diferentes do Copilot para o mesmo problema. Com isso, o Copilot conhece os padrões do time desde o primeiro acesso.

**✅ Valide:** abra um novo chat no Copilot e pergunte _"Qual é o padrão de nomenclatura de testes do time?"_ — ele deve responder com `Should_X_When_Y`.

---

### Pilar 2 — Skills 🧠

**O que é:** conhecimento especializado injetado **sob demanda**. Diferente das instructions (sempre ativas), a skill entra quando o Copilot detecta que o contexto é relevante (ex: ao gerar testes).

**Faça:**

```bash
mkdir -p .github/skills/gerar-testes-pdv
cp governanca/.github/skills/gerar-testes-pdv/SKILL.md .github/skills/gerar-testes-pdv/
```

**Leia o `SKILL.md`:** note o campo `description` — é ele que determina quando a skill é ativada.

> 💡 **Por que importa:** skills empacotam o "como fazer" do time. Um dev novo recebe automaticamente o template correto de testes xUnit ao pedir para o Copilot gerar testes.

---

### Pilar 3 — Agents 🤖

**O que é:** agente especializado com identidade, escopo e ferramentas próprias. Você o invoca explicitamente com `@nome-do-agente`.

**Faça:**

```bash
mkdir -p .github/agents
cp governanca/.github/agents/qa-boa-vista.agent.md .github/agents/
```

**Leia o arquivo:** note os campos `tools:` (ferramentas que o agente pode usar) e como ele classifica issues.

> 💡 **Por que importa:** diferente das instructions (que orientam quem *gera*), o agent `@qa-boa-vista` é um *revisor* — você o chama para avaliar código já gerado. É o QA automatizado do time.

**✅ Valide:** no Copilot Chat, invoque `@qa-boa-vista` e peça para ele revisar o arquivo `VendasController.cs`.

---

### Pilar 4 — MCP 🔌

**O que é:** conexão do Agent Mode a ferramentas externas via Model Context Protocol. Com isso, o agente pode ler o banco de dados, consultar APIs internas ou qualquer fonte de dados — sem você precisar copiar e colar contexto.

**O arquivo `.vscode/mcp.json` já existe no repositório.** Mas o banco de dados precisa existir.

**Faça:**

```bash
# Cria o banco SQLite do catálogo de produtos
python -c "
import sqlite3, re
conn = sqlite3.connect('db/catalogo-produtos.db')
for stmt in re.split(r';', open('db/setup-catalogo.sql').read()):
    s = re.sub(r'--[^\n]*', '', stmt).strip()
    if s: conn.execute(s)
conn.commit(); conn.close()
print('Banco criado!')
"
```

**Leia `.vscode/mcp.json`:** veja como o servidor MCP sqlite é configurado em 3 linhas.

> 💡 **Por que importa:** o agente pode consultar o catálogo de produtos real durante a geração de código — sem você precisar descrever quais produtos existem. Experimente no Bloco 3.

**✅ Valide:** no VS Code, vá em `Copilot Chat → Agent Mode` e pergunte _"Quais produtos estão inativos no catálogo?"_

---

### Pilar 5 — Hooks 🪝

**O que é:** o único primitivo que **bloqueia e corrige** o agente. Hooks interceptam ações (antes ou depois) e podem injetar mensagens de volta para o agente.

**Faça:**

```bash
mkdir -p .github/hooks/scripts
cp governanca/.github/hooks/build-guard.json .github/hooks/
cp governanca/.github/hooks/scripts/build-guard.ps1 .github/hooks/scripts/
cp governanca/.github/hooks/scripts/build-guard.sh .github/hooks/scripts/
```

**Leia `build-guard.json`:** note o evento `postToolUse` — ele dispara **depois** que o agente edita um arquivo. Se arquivos `.cs` foram modificados, roda `dotnet test`. Se falhar, injeta a mensagem de erro de volta para o agente se corrigir.

> 💡 **Por que importa:** é a diferença entre "agente que faz e pronto" e "agente que faz, verifica e conserta". Em produção, o Copilot não vai commitar código quebrado.

**✅ Valide:** este pilar você vai ver em ação no Bloco 4 — é o momento mais impactante do workshop.

---

### Pilar 6 — Knowledge Base 📚

**O que é:** prompts reutilizáveis que encapsulam o conhecimento do time. São como "receitas" prontas — você executa com um clique em vez de descrever tudo do zero.

**Faça:**

```bash
mkdir -p .github/prompts
cp governanca/.github/prompts/bloco2-com-instructions.prompt.md .github/prompts/
cp governanca/.github/prompts/bloco3-mcp-catalogo.prompt.md .github/prompts/
cp governanca/.github/prompts/bloco4-adicionar-status.prompt.md .github/prompts/
cp governanca/.github/prompts/bloco4-correcao-manual.prompt.md .github/prompts/
cp governanca/.github/prompts/bloco6-descricao-pr.prompt.md .github/prompts/
```

**Leia os arquivos:** note o campo `mode:` — `agent` para tarefas que modificam código, `chat` para tarefas narrativas (como descrição de PR).

> 💡 **Por que importa:** sem prompts padronizados, cada dev descreve a tarefa de um jeito diferente e recebe resultados inconsistentes. Com prompts compartilhados, o time tem um vocabulário comum com o agente.

---

### Pilar 7 — Coding Agent ⚙️

**O que é:** o arquivo `AGENTS.md` instrui o Coding Agent (usado em CI/CD e automações) sobre as regras do repositório. Diferente das instructions do Copilot no VS Code, este arquivo é lido pelo agente autônomo que opera sem supervisão humana.

**O `AGENTS.md` já existe na raiz do repositório.** Leia-o agora.

**Leia também `.github/workflows/ci.yml`:** o workflow CI roda `dotnet test` a cada push. O Coding Agent sabe disso e não pode commitar código que quebre o build.

> 💡 **Por que importa:** quando o agente opera de forma autônoma (em pipelines, em PRs automáticos), o `AGENTS.md` é o contrato entre o time e o agente. Sem ele, o agente age sem restrições.

**✅ Valide:** já está configurado. O `gerar_evidencia.py` vai verificar que o arquivo existe e contém as regras corretas.

---

### Pilar 8 — CLI 💻

**O que é:** GitHub Copilot no terminal. Para quem vive no bash/PowerShell — sem precisar abrir o VS Code.

**Faça:**

```bash
# Verifica se gh está instalado (o setup.bat já fez isso)
gh --version

# Testa o Copilot CLI
gh copilot suggest "como ver todos os arquivos modificados no último commit"
gh copilot explain "git rebase -i HEAD~3"
```

> 💡 **Por que importa:** onboarding de devs que ainda não conhecem os comandos git avançados. E para automações — você pode usar `gh copilot suggest` em scripts de CI.

---

## Execute os Blocos

Agora que todos os pilares estão configurados, execute os blocos do workshop usando os prompts que você copiou:

| Bloco | Prompt | O que demonstra |
|-------|--------|-----------------|
| **Bloco 1** | `bloco1-sem-padrao` (na raiz) | Agente sem governança |
| **Bloco 2** | `bloco2-com-instructions` | Instructions + Skills |
| **Bloco 3** | `bloco3-mcp-catalogo` | MCP — consulta ao banco |
| **Bloco 4** | `bloco4-adicionar-status` | Hook de autocorreção |
| **Bloco 5** | `@qa-boa-vista` no chat | Custom Agent revisor |
| **Bloco 6** | `bloco6-descricao-pr` | Descrição automática de PR |
| **Bloco 7** | `gh copilot suggest` | CLI |

> Os prompts aparecem automaticamente no Copilot Chat (`/` para listar).

---

## 🏁 Gere sua evidência

Após executar todos os blocos:

```bash
# Substitua com seu nome e sua turma (dev / qa / suporte)
python setup/gerar_evidencia.py --nome "Seu Nome Completo" --turma dev
```

O HTML abrirá automaticamente no navegador. Você deve ver **8/8 pilares configurados**.

**Tire o screenshot do card** e envie como evidência de conclusão.

---

## Abra seu PR

```bash
# Garante que seus commits estão na branch do time
git push origin feature/dev    # ou qa / suporte

# Abre o PR via CLI
gh pr create \
  --base main \
  --head feature/dev \
  --title "feat: configuração completa de governança — Time Dev" \
  --body "Evidência gerada em evidencias/"
```

---

## Checklist final

- [ ] Clonei o repo e rodei `setup.bat` / `setup.sh`
- [ ] Fiz checkout da minha branch (`feature/dev|qa|suporte`)
- [ ] Copiei e li cada arquivo de governança de `governanca/.github/`
- [ ] Criei o banco SQLite do catálogo
- [ ] Executei os Blocos 1 a 7
- [ ] Rodei `gerar_evidencia.py` e obtive 8/8 pilares
- [ ] Tirei o screenshot do HTML
- [ ] Abri PR da minha branch → `main`
