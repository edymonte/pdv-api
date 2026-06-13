---
description: >
  Gera testes xUnit para o pdv-api seguindo o padrão do time Boa Vista:
  nomenclatura Should_X_When_Y, estrutura AAA, Moq para dependências e
  FluentAssertions para assertions. Use quando precisar criar ou revisar
  testes de Services ou Controllers.
---

# Skill — gerar-testes-pdv

## Quando usar esta skill

Use `@workspace` + esta skill sempre que precisar:
- Criar testes para um novo método de Service
- Completar cobertura de testes existente
- Revisar se um teste segue o padrão do projeto

## Padrão de nomenclatura

```
Should_[ResultadoEsperado]_When_[Condição]
```

| Cenário | Nome do teste |
|---|---|
| Operação bem-sucedida | `Should_CancelarVenda_When_StatusConcluida` |
| Entidade não encontrada | `Should_ThrowValidationError_When_VendaNaoEncontrada` |
| Estado inválido | `Should_ThrowValidationError_When_VendaJaCancelada` |
| Dado ausente/inválido | `Should_ThrowValidationError_When_IdInvalido` |

## Template completo de teste de Service

```csharp
[Fact]
public async Task Should_[Resultado]_When_[Condicao]()
{
    // Arrange
    var options = new DbContextOptionsBuilder<PdvContext>()
        .UseInMemoryDatabase(Guid.NewGuid().ToString())
        .Options;
    await using var context = new PdvContext(options);

    // (seed de dados necessários)
    var venda = new Venda { ClienteId = "CLI-001", Status = StatusVenda.Concluida };
    context.Vendas.Add(venda);
    await context.SaveChangesAsync();

    var service = new VendaService(context, NullLogger<VendaService>.Instance);

    // Act
    var resultado = await service.CancelarVendaAsync(venda.Id);

    // Assert
    resultado.Should().NotBeNull();
    resultado.Status.Should().Be(StatusVenda.Cancelada);
}
```

## Cobertura mínima exigida para CancelarVendaAsync

Todo PR que adicionar `CancelarVendaAsync` deve cobrir:

1. `Should_CancelarVenda_When_StatusConcluida` — caminho feliz
2. `Should_ThrowValidationError_When_VendaJaCancelada` — status já cancelada
3. `Should_ThrowValidationError_When_VendaNaoEncontrada` — ID inexistente
4. `Should_ThrowValidationError_When_StatusPendente` — status não permite cancelamento

## Checklist antes do PR

- [ ] Todos os testes acima implementados
- [ ] Nenhum teste com múltiplos `Assert` (um cenário por `[Fact]`)
- [ ] DB in-memory com nome único por teste (`Guid.NewGuid().ToString()`)
- [ ] `dotnet test` passando localmente
