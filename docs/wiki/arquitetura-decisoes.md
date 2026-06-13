# Decisões de Arquitetura — pdv-api

> ADRs (Architecture Decision Records) do sistema PDV da Farmácia Boa Vista.
> Consulte antes de propor mudanças estruturais.

---

## ADR-001: Lógica de negócio em Services, não em Controllers

**Status:** Aceito

**Contexto:** Controllers ASP.NET Core tendem a acumular lógica quando não há separação explícita.

**Decisão:** Controllers são responsáveis exclusivamente por:
1. Receber e validar a entrada HTTP
2. Delegar ao Service correspondente
3. Mapear o resultado para a resposta HTTP

Toda regra de negócio (cancelamento, desconto, estoque) vive no Service — testável sem contexto HTTP.

**Consequência:** Nunca injetar `DbContext` diretamente em Controllers. Usar sempre a interface do Service.

---

## ADR-002: FluentValidation para validações de domínio

**Status:** Aceito

**Contexto:** DataAnnotations são suficientes para validações simples mas limitados para regras complexas.

**Decisão:** Usar `FluentValidation.AspNetCore` para todas as validações de request.
- Mensagens de erro em **português**
- Um `AbstractValidator<T>` por comando/request
- Validators ficam em `src/PdvApi/Validators/`

**Consequência:** Nunca usar `[Required]` ou `[Range]` para regras de negócio. DataAnnotations permitidas apenas para mapeamento de modelo.

---

## ADR-003: EF Core InMemory no ambiente de workshop

**Status:** Aceito (ambiente de desenvolvimento/workshop)

**Contexto:** O setup de um banco SQL completo aumenta o tempo de configuração sem agregar ao aprendizado.

**Decisão:** Usar `Microsoft.EntityFrameworkCore.InMemory` durante o workshop.

**Em produção:** Azure SQL com migrations EF Core. A mudança é apenas na string de conexão e pacote.

**Restrição crítica:** **Nunca usar `FromSqlRaw` com interpolação de string** — risco de SQL Injection mesmo em InMemory (o padrão vaza para produção). Use sempre `FromSqlRaw` com parâmetros ou LINQ.

---

## ADR-004: Conventional Commits obrigatório

**Status:** Aceito

**Formato:** `<tipo>(<escopo>): <descrição em português>`

Tipos permitidos:
- `feat`: nova funcionalidade
- `fix`: correção de bug
- `refactor`: refatoração sem mudança de comportamento
- `test`: adição ou correção de testes
- `docs`: documentação
- `chore`: tarefas de manutenção (deps, config)

**Exemplos:**
```
feat(vendas): adiciona endpoint de cancelamento com validação FluentValidation
fix(estoque): corrige devolução dupla em cancelamento concorrente
test(vendas): adiciona cobertura para cancelamento fora do prazo
```

Mensagem do commit deve ser em português. Sem emoji no título.

---

## ADR-005: Padrão de testes xUnit

**Status:** Aceito

- Nomenclatura: `Should_<resultado>_When_<condição>`
- Estrutura: Arrange / Act / Assert com comentários explícitos
- Uma assertion por teste (usar FluentAssertions)
- Mocks com Moq; nunca testar infraestrutura diretamente em testes unitários
- Cobertura mínima aceitável: **80%** para código novo
