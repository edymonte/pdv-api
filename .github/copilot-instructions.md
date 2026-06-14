# Padrões do projeto pdv-api — Farmácia Boa Vista

> Estas instruções são injetadas automaticamente no contexto do Copilot.
> Toda geração de código neste repositório deve seguir as regras abaixo.

---

## Stack e contexto

- **Projeto:** PDV API — sistema de ponto de venda da Farmácia Boa Vista
- **Stack:** .NET 8, ASP.NET Core, Entity Framework Core, xUnit, Moq, FluentValidation
- **Editores:** VS Code e Visual Studio
- **Organização GitHub:** `bvista-dev`

---

## Arquitetura

- Toda lógica de negócio fica em **Services** — nunca em Controllers
- Controllers apenas delegam para o Service e retornam HTTP responses
- Validações de entrada usam **FluentValidation** (Validators em `/Validators`)
- Acesso a dados exclusivamente via **EF Core** — nunca `FromSqlRaw` com concatenação
- Métodos assíncronos sempre com sufixo **`Async`** (ex: `CancelarVendaAsync`)

---

## Segurança (CRÍTICO)

- **NUNCA** usar `FromSqlRaw` com interpolação de string — use `FromSqlInterpolated` ou parâmetros nomeados
- **NUNCA** expor detalhes de exceção interna no response HTTP
- **NUNCA** logar dados sensíveis de clientes (CPF, endereço, dados de pagamento)
- **NUNCA** inventar nomes de pacotes NuGet — sugerir apenas pacotes que existam oficialmente em nuget.org
- Validar todos os inputs no Validator antes de chegar ao Service
- Nunca confiar em IDs ou dados vindos do cliente sem validar existência e permissão

---

## Padrão de testes (xUnit)

Toda nova funcionalidade deve ter testes xUnit cobrindo:
1. Caso de sucesso (`Should_X_When_Y_Sucesso`)
2. Caso de erro de validação (`Should_ThrowValidationError_When_EntradaInvalida`)
3. Caso de entidade não encontrada (`Should_ThrowValidationError_When_VendaNaoEncontrada`)

**Nomenclatura obrigatória:** `Should_[Resultado]_When_[Condição]`

**Estrutura obrigatória (padrão AAA):**
```csharp
// Arrange
// Act
// Assert
```

Use **Moq** para mockar repositórios e dependências.
Use **FluentAssertions** para assertions mais legíveis.

---

## Commits e PRs

- Commits seguem **Conventional Commits**: `feat:`, `fix:`, `test:`, `refactor:`, `docs:`
- A descrição do PR deve explicar o que foi alterado e por quê em linguagem que um revisor não-técnico (liderança) consiga entender o impacto
- PRs devem listar riscos de segurança avaliados (ex: "validado contra SQL injection", "entrada de usuário validada")
- Nunca dar merge sem testes passando (`dotnet test`)

---

## Idioma

- Código em inglês (nomes de classes, métodos, variáveis)
- Comentários, mensagens de erro e logs em **português (pt-BR)**
- Mensagens de validação em português (ex: `"Venda não encontrada."`)
