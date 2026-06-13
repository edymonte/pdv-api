# Workshop Context — GitHub Copilot Extensibility
# pdv-api — Farmácia Boa Vista

> Use `@file:.github/WORKSHOP_CONTEXT.md` no início de uma nova sessão
> para retomar exatamente de onde o workshop parou.

---

## Fluxo de dois estados (FUNDAMENTAL para o demo)

O repo tem dois estados intencionais — a troca entre eles É o workshop:

| Estado | O que o `.github/` contém | Quando usar |
|---|---|---|
| **Sem governança** | Apenas `ci.yml` + `WORKSHOP_CONTEXT.md` | Blocos 0 e 1 |
| **Com governança** | Tudo do `governanca/.github/` copiado | Blocos 2 a 8 |

**Transição ao vivo (entre Bloco 1 e Bloco 2):**
```
pwsh -File setup\ativar-governanca.ps1
```
Depois, abra um **novo chat do Copilot** para as instructions serem recarregadas.

**Reset entre turmas:**
```
pwsh -File setup\reset-ambiente.ps1
```
Volta para o estado sem governança, recria o banco SQLite e verifica os testes.

---

## Primitivas ativas (após ativar-governanca)

### Instructions — sempre no contexto

| Arquivo | Escopo | O que define |
|---|---|---|
| `.github/copilot-instructions.md` | Todo o repositório | Arquitetura, segurança, padrão de commits |
| `.github/instructions/testes.instructions.md` | `tests/**/*.cs` | Nomenclatura AAA, uma assertion por teste |
| `.github/instructions/validacao.instructions.md` | `src/**/Validators/*.cs` | FluentValidation, mensagens em português |

### Skills — injetadas sob demanda

| Pasta | Quando usar |
|---|---|
| `.github/skills/gerar-testes-pdv/` | Gerar ou revisar testes xUnit do pdv-api |

### Custom Agents — chamados via @nome

| Arquivo | Como chamar | Especialidade |
|---|---|---|
| `.github/agents/qa-boa-vista.agent.md` | `@qa-boa-vista` | Revisão de código: aderência às instructions, cobertura, segurança |

### Hook de Build — dispara autocorreção

| Arquivo | Evento | O que faz |
|---|---|---|
| `.github/hooks/build-guard.json` | `postToolUse` | Roda `dotnet test` após alterações `.cs`; se falhar, notifica o agente |

### Knowledge Base — wiki consultada pelo agente

| Arquivo | Conteúdo |
|---|---|
| `docs/wiki/regras-de-negocio.md` | Regras de cancelamento, desconto, estoque, fluxo de status |
| `docs/wiki/regulatorio-anvisa.md` | LGPD, medicamentos controlados, NF-e |
| `docs/wiki/arquitetura-decisoes.md` | ADRs — padrões de código, testes, commits |

Demo: `@workspace Qual é o limite de desconto sem aprovação gerencial?` — Copilot encontra em `docs/wiki/`.  
Prompt: `.github/prompts/bloco6-knowledge-base.prompt.md` — agente lê a wiki e implementa a validação.

### MCP — ferramentas externas no Agent Mode

| Servidor | O que acessa | Como testar |
|---|---|---|
| `sqlite-catalogo` | `db/catalogo-produtos.db` | "liste todos os produtos do catálogo" |
| `fetch` | Qualquer URL pública em tempo real | `bloco3b-mcp-fetch.prompt.md` — busca ANVISA/CMED |

---

## Roteiro dos Blocos (referência rápida)

| Bloco | Conteúdo | Como executar | Tempo |
|---|---|---|---|
| 0 | Abertura — contexto e objetivo | — | 10min |
| 1 | Agente sem regras | `.github/prompts/bloco1-sem-padrao.prompt.md` | 20min |
| 2 | Com instructions + skill | `.github/prompts/bloco2-com-instructions.prompt.md` | 25min |
| 3 | MCP — catálogo SQLite + fetch externo | `bloco3-mcp-catalogo.prompt.md` / `bloco3b-mcp-fetch.prompt.md` | 15min |
| 4 ⭐ | Autocorreção via hook | `.github/prompts/bloco4-adicionar-status.prompt.md` | 30min |
| 5 | `@qa-boa-vista` revisa | prompt inline: `@qa-boa-vista revise as alterações feitas até agora` | 15min |
| 6 ⭐ | Knowledge Base — wiki → código | `.github/prompts/bloco6-knowledge-base.prompt.md` | 15min |
| 7 ⭐ | Coding Agent — Issue → PR no GitHub.com | Atribuir issue ao Copilot em github.com/edymonte/pdv-api/issues | 15min |
| 8 | CLI + Encerramento | `gh copilot suggest` / `copilot` CLI · Comparar `demo/sem-padrao` vs PR final | 15min |

---

## Estado inicial do repo (antes da demo)

- `VendasController`: endpoints GET e POST funcionando; **sem** `/cancelar`
- `VendaService`: `ObterPorIdAsync`, `ListarTodasAsync`, `CriarVendaAsync`; **sem** `CancelarVendaAsync`
- `StatusVenda`: apenas `Pendente`, `Concluida`, `Cancelada`; **sem** `EmAnalise`
- 3 testes passando (cobertura básica do Service)
- Branch `demo/sem-padrao`: gerada uma vez, reutilizada nas 6 turmas
