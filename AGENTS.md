# PDV API — Instruções para Agentes de IA

> Este arquivo orienta o comportamento do GitHub Copilot (Chat, Inline e Agent Mode).
> Complementa `.github/copilot-instructions.md` com contexto específico do workshop.

---

## Contexto do projeto

Sistema de PDV fictício da **Farmácia Boa Vista**, usado no **GitHub Copilot Workshop**.
Os participantes praticam geração de código, testes e autocorreção com suporte de IA.

---

## Regras de geração de código

- **Fix mínimo sempre:** corrija apenas o que o prompt pede. Não refatore código adjacente.
- **Preserve assinaturas públicas:** nunca altere assinaturas de métodos em interfaces sem instrução explícita.
- **Português nos outputs:** comentários, mensagens de erro e validações em pt-BR.
- **Sem dependências novas:** não adicione pacotes NuGet que não estejam no `.csproj`.
- **Segurança:** nunca use `FromSqlRaw` com interpolação de string.

---

## Arquivos-chave

| Arquivo | Papel |
|---|---|
| `src/PdvApi/Models/StatusVenda.cs` | Enum de status — alterado no Bloco 4 |
| `src/PdvApi/Services/IVendaService.cs` | Interface — `CancelarVendaAsync` gerado nos Blocos 1-4 |
| `src/PdvApi/Services/VendaService.cs` | Implementação do Service |
| `src/PdvApi/Validators/` | Validators FluentValidation — gerado no Bloco 2 |
| `tests/PdvApi.Tests/Services/` | Testes xUnit — expandidos nos Blocos 2-4 |
| `db/catalogo-produtos.db` | Banco SQLite do MCP — produto id=5 inativo de propósito |

---

## Ferramentas disponíveis no Agent Mode

- **MCP sqlite-catalogo:** consulte a tabela `produtos` para verificar se produtos estão ativos
- **Testes:** após alterações `.cs`, rode `dotnet test` para verificar se build passou

---

## Estado esperado antes da demo

- Build passando: `dotnet build` sem erros
- Testes passando: `dotnet test` — 3 testes green
- Sem endpoint `/cancelar` implementado (gerado ao vivo)
- Sem `CancelarVendaAsync` no Service (gerado ao vivo)
- Sem `EmAnalise` no enum (adicionado no Bloco 4)
