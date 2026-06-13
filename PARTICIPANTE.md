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
**Instructions vs. Skills — quando usar cada um:**

| | Instructions | Skills |
|---|---|---|
| **Quando ativa** | Sempre — em todo chat do repo | Sob demanda — quando o contexto é relevante |
| **O que define** | Regras que sempre se aplicam (stack, segurança, nomenclatura) | Procedimentos específicos (como gerar testes, como escalar incidente) |
| **Exemplo** | “Nunca usar `FromSqlRaw` com interpolação” | “Ao gerar testes, use o template xUnit com AAA e `Should_X_When_Y`” |
**✅ Valide:** abra um novo chat no Copilot e pergunte _"Qual é o padrão de nomenclatura de testes do time?"_ — ele deve responder com `Should_X_When_Y`.

---

### Pilar 2 — Skills 🧠

**O que é:** conhecimento especializado injetado **sob demanda**. Diferente das instructions (sempre ativas), a skill entra quando o Copilot detecta que o contexto é relevante (ex: ao gerar testes).

**Faça:**

```bash
mkdir -p .github/skills/gerar-testes-pdv
cp governanca/.github/skills/gerar-testes-pdv/SKILL.md .github/skills/gerar-testes-pdv/
```

**Leia o `SKILL.md`:** o arquivo tem uma estrutura específica que o Copilot interpreta:

```markdown
# Skill: Gerar Testes PDV
## Quando usar: testes, xunit, cobertura, Should_, AAA
## Template
...
```

Os campos `# Skill:` e `## Quando usar:` são o que determina **quando** a skill é injetada. O Copilot lê o `description` e decide se o contexto da pergunta é relevante para ativá-la.

> 💡 **Por que importa:** skills empacotam o "como fazer" do time. Um dev novo recebe automaticamente o template correto de testes xUnit ao pedir para o Copilot gerar testes.

---

### Pilar 3 — Agents 🤖

**O que é:** agente especializado com identidade, escopo e ferramentas próprias. Você o invoca explicitamente com `@nome-do-agente`.

**Faça:**

```bash
mkdir -p .github/agents
cp governanca/.github/agents/qa-boa-vista.agent.md .github/agents/
```

**Leia o arquivo:** veja a estrutura que todo agente deve ter:

```yaml
---
description: >  # o que o agente faz e quando invocar
tools:          # ferramentas que ele pode usar
  - read_file
  - grep
  - list_directory
---
# Nome do Agente
Você é ...
## O que verificar
...
## Formato de resposta
## [Nome do arquivo ou feature]
### 🔴 Bloqueante | 🟡 Atenção | 🟢 Sugestão
```

O formato de classificação 🔴/🟡/🟢 é definido dentro do arquivo do agente — você controla os critérios de aceite da empresa.

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

**Leia `.vscode/mcp.json`:** o arquivo tem dois servidores configurados:

| Servidor | O que faz |
|---|---|
| `sqlite-catalogo` | Consulta o banco local de produtos (SQLite) |
| `fetch` | Busca qualquer URL pública em tempo real |

> 💡 **Por que importa:** o agente não está limitado ao que existe no repositório. Com o `fetch`, ele pode ler documentação técnica externa, regulatórios, APIs públicas — e usar o conteúdo diretamente no código que está escrevendo.

**Isolamento por repositório:** o `mcp.json` fica dentro do `.vscode/` de cada repo. O Time Dev acessa o banco de produtos; o Time QA acessa issues; o Suporte N2 acessa logs de incidentes. **Sem vazamento de contexto entre times.**

**✅ Valide — dois experimentos:**

1. Bloco 3 (SQLite): no Agent Mode, pergunte _"Quais produtos estão inativos no catálogo?"_
2. Bloco 3b (fetch): execute o prompt `bloco3b-mcp-fetch.prompt.md` — o agente vai buscar a página da ANVISA/CMED e usar o conteúdo para documentar o código

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

**Leia `build-guard.json`:** note o evento `postToolUse`. Hooks são o único primitivo com eventos — cada um tem uma finalidade diferente:

| Evento | Quando dispara | O que pode fazer |
|---|---|---|
| `sessionStart` | Início de cada sessão do agente | Log de início, aviso de políticas ativas |
| `preToolUse` ⭐ | **Antes** de o agente executar qualquer ferramenta | Único que pode **BLOQUEAR** a ação antes de acontecer |
| `postToolUse` | Após o agente executar uma ferramenta | Validar resultado, notificar, disparar testes |
| `userPromptSubmitted` | Quando o usuário envia um prompt | Filtrar dados sensíveis (CPF, senha) antes de processar |
| `errorOccurred` | Quando ocorre um erro | Alerta automático + sugestão de rollback |

> ⚠️ `preToolUse` é o único evento que pode BLOQUEAR uma ação antes de acontecer. O nosso `build-guard.json` usa `postToolUse` (mais comum) — em produção, um `preToolUse` poderia impedir que o agente deletasse arquivos em `/prod/` sem PR aprovado.

> 💡 **Por que importa:** é a diferença entre "agente que faz e pronto" e "agente que faz, verifica e conserta". Em produção, o Copilot não vai commitar código quebrado.

**✅ Valide:** este pilar você vai ver em ação no Bloco 4 — é o momento mais impactante do workshop.

---

### Pilar 6 — Knowledge Base 📚

**O que é:** documentação versionada no repositório que o Copilot consulta e **aplica diretamente no código**. Regras de negócio, ADRs, runbooks — o agente encontra a resposta na wiki antes de escrever uma linha.

A diferença para as instructions: instructions são regras técnicas (sempre ativas). A Knowledge Base é o **domínio do negócio** — o agente a consulta quando precisa saber o que a empresa exige, não apenas como o código deve ser escrito.

**Skills vs. Knowledge Base — a distinção do slide:**

| | Skills | Knowledge Base |
|---|---|---|
| **Escopo** | Procedimento específico e pontual | Índice amplo de toda a documentação |
| **Ativação** | Injetada on-demand quando relevante | Pesquisada semanticamente em background |
| **Exemplo** | “Ao gerar testes, use este template” | “Qual é o limite de desconto? → busca em regras-de-negocio.md” |
| **Artefato** | `SKILL.md` em `.github/skills/` | `docs/wiki/*.md` (ou repos indexados no Enterprise) |

> 📎 Em produção, o GitHub Copilot Enterprise indexa documentação de vários repositórios, PDFs e wikis externas semanticamente. Aqui simulamos o mesmo conceito com `docs/wiki/` versionado no próprio repo.

**Faça:**

```bash
# A pasta docs/wiki/ já existe no repositório — explore os arquivos:
cat docs/wiki/regras-de-negocio.md       # regras de cancelamento, desconto, estoque
cat docs/wiki/regulatorio-anvisa.md      # LGPD, medicamentos controlados, NF-e
cat docs/wiki/arquitetura-decisoes.md    # ADRs do projeto

# Copia o prompt do Bloco 6
mkdir -p .github/prompts
cp governanca/.github/prompts/bloco6-knowledge-base.prompt.md .github/prompts/
```

**Leia `docs/wiki/regras-de-negocio.md`:** preste atenção na seção "Descontos" — tem os limites exatos (15% geral, 5% para controlados) e as mensagens de erro que o sistema deve retornar.

**Teste antes de executar o prompt:**

No Copilot Chat (modo chat normal), pergunte:
> `@workspace Qual é o limite de desconto permitido sem aprovação gerencial?`

O Copilot vai encontrar a resposta em `docs/wiki/regras-de-negocio.md` sem você precisar explicar. **Esse é o conceito de Knowledge Base** — a documentação se torna contexto automático.

**Execute o prompt do Bloco 6:**

Abra `bloco6-knowledge-base.prompt.md` no VS Code e execute (`/` para listar prompts).

O agente vai:
1. Ler `docs/wiki/regras-de-negocio.md` para encontrar os limites exatos
2. Ler `docs/wiki/arquitetura-decisoes.md` para seguir o padrão de testes
3. Implementar a validação com os valores **da documentação** — não inventados
4. Gerar os testes seguindo o padrão ADR-005

> 💡 **Por que importa:** um dev novo nunca precisa perguntar "qual é a regra de desconto?" — ele escreve o código e o Copilot aplica a regra correta da wiki automaticamente. Regra mudou? Atualiza o Markdown e o agente passa a usar a nova regra.

**✅ Valide:** o `gerar_evidencia.py` verifica que `docs/wiki/regras-de-negocio.md`, `regulatorio-anvisa.md` e `bloco6-knowledge-base.prompt.md` existem.

---

### Pilar 7 — Coding Agent ⚙️

**O que é:** o Copilot como agente autônomo no GitHub.com. Você atribui uma issue ao Copilot; ele lê as instructions, explora o codebase, escreve código, roda os testes e **abre o PR automaticamente** — sem intervenção humana até a revisão.

**O fluxo completo em 4 etapas:**

| Etapa | O que acontece |
|---|---|
| **1 → Atribuir issue** | Você cria a issue no GitHub e atribui ao Copilot |
| **2 → Copilot planeja** | Lê `AGENTS.md`, instructions e explora o codebase para definir a abordagem |
| **3 → Codifica + testa** | Escreve o código, itera nos erros, roda os testes automaticamente |
| **4 → Abre o PR** | Draft PR com código, testes e scan de segurança. Marca dev para revisão |

**Pré-requisito:** `AGENTS.md` na raiz do repositório instrui o Coding Agent sobre as regras do time. Leia-o agora.

**Leia também `.github/workflows/ci.yml`:** o Coding Agent sabe que há CI rodando `dotnet test` a cada push e não pode quebrar a build.

**Faça — demo do Issue → PR automático:**

1. Acesse **github.com/edymonte/pdv-api/issues** no navegador
2. Crie uma nova issue com o título:
   > `feat: endpoint GET /api/vendas/relatorio — contagem por status`
3. No corpo da issue, descreva:
   > Criar um endpoint que retorna a contagem de vendas agrupadas por `StatusVenda`. Seguir os padrões de arquitetura do repositório.
4. No campo **Assignees**, atribua ao **Copilot** (aparece como opção ao clicar)
5. Aguarde — o Copilot vai:
   - Explorar o codebase
   - Escrever o endpoint seguindo as instructions
   - Rodar os testes
   - Abrir um **draft PR** com o código, testes e scan de segurança
6. Revise o PR aberto pelo Copilot no GitHub

> 💡 **Por que importa:** o Coding Agent opera fora do VS Code — em pipelines, automações noturnas, PRs gerados por issue. O `AGENTS.md` é o contrato que garante que ele segue os mesmos padrões do time, mesmo sem supervisão humana direta.

**✅ Valide:** o `gerar_evidencia.py` verifica que `AGENTS.md` existe e contém as regras de governança. O PR aberto pelo Copilot é a evidência em tempo real.

---

### Pilar 8 — CLI 💻

**O que é:** GitHub Copilot no terminal — dois modos:

| Modo | Comando | Instalação | Quando usar |
|---|---|---|---|
| **gh copilot** | `gh copilot suggest` / `explain` | Via GitHub CLI (já instalado) | Comandos git e shell rápidos |
| **copilot CLI** | `copilot` | `npm install -g @github/copilot` | Agente completo no terminal — edita arquivos, roda testes, delega tarefas |

**Faça:**

```bash
# gh copilot (já instalado via setup.bat)
gh copilot suggest "como ver todos os arquivos modificados no último commit"
gh copilot explain "git rebase -i HEAD~3"

# copilot CLI (agente completo no terminal)
npm install -g @github/copilot   # instala uma vez
copilot                           # inicia sessão interativa
```

Dentro da sessão `copilot`:
```
> Revise todos os endpoints em src/ buscando SQL Injection
> &Crie testes para o módulo de estoque enquanto continuo trabalhando
> /model                          # lista modelos disponíveis
> /resume                         # retoma sessão delegada com &
```

O prefixo `&` delega a tarefa em background — o agente trabalha enquanto você continua no terminal.

> 💡 **Por que importa:** onboarding de devs que ainda não conhecem os comandos git avançados. E para automações — você pode usar `gh copilot suggest` em scripts de CI.

---

## Execute os Blocos

Agora que todos os pilares estão configurados, execute os blocos do workshop usando os prompts que você copiou:

| Bloco | Como executar | O que demonstra |
|-------|---------------|------------------|
| **Bloco 1** | prompt `bloco1-sem-padrao` (na raiz) | Agente sem governança |
| **Bloco 2** | prompt `bloco2-com-instructions` | Instructions + Skills |
| **Bloco 3** | prompt `bloco3-mcp-catalogo` + `bloco3b-mcp-fetch` | MCP — banco local + URL externa |
| **Bloco 4** | prompt `bloco4-adicionar-status` | Hook de autocorreção |
| **Bloco 5** | `@qa-boa-vista` no chat | Custom Agent revisor |
| **Bloco 6** | prompt `bloco6-knowledge-base` | Knowledge Base — wiki → código |
| **Bloco 7** | Atribuir issue ao Copilot em github.com | Coding Agent — Issue → PR automático |
| **Bloco 8** | `gh copilot suggest` / `copilot` CLI | CLI |

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

## Revise o PR aberto pelo Copilot

No **Bloco 7**, o Copilot abriu um draft PR automaticamente a partir da issue que você criou.

1. Acesse **github.com/edymonte/pdv-api/pulls** no navegador
2. Encontre o PR aberto pelo Copilot
3. Leia o código gerado — verifique se ele seguiu as instructions do time
4. Aprove e faça o merge (ou solicite ajustes deixando um comentário — o Copilot vai iterar)

> O PR aberto pelo Copilot é a evidência viva do Pilar 7. Guarde o link.

---

## Checklist final

- [ ] Clonei o repo e rodei `setup.bat` / `setup.sh`
- [ ] Fiz checkout da minha branch (`feature/dev|qa|suporte`)
- [ ] Copiei e li cada arquivo de governança de `governanca/.github/`
- [ ] Criei o banco SQLite do catálogo
- [ ] Executei os Blocos 1 a 8
- [ ] O Copilot abriu o PR automaticamente no Bloco 7 (Coding Agent)
- [ ] Rodei `gerar_evidencia.py` e obtive 8/8 pilares
- [ ] Tirei o screenshot do HTML
- [ ] Revisei e aprovei o PR aberto pelo Copilot
