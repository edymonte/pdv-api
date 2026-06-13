---
applyTo: "tests/**/*.cs"
---

# Padrões de Testes — pdv-api

Ao gerar ou modificar testes neste projeto, siga rigorosamente:

## Nomenclatura

```
Should_[ResultadoEsperado]_When_[Condição]
```

Exemplos corretos:
- `Should_CancelarVenda_When_StatusConcluida`
- `Should_ThrowValidationError_When_VendaJaCancelada`
- `Should_ReturnNull_When_VendaNaoEncontrada`

## Estrutura (padrão AAA obrigatório)

```csharp
[Fact]
public async Task Should_X_When_Y()
{
    // Arrange
    var mockRepo = new Mock<IVendaService>();
    mockRepo.Setup(...).ReturnsAsync(...);

    // Act
    var resultado = await service.MetodoAsync(params);

    // Assert
    resultado.Should().NotBeNull();
    resultado.Status.Should().Be(StatusVenda.Cancelada);
}
```

## Regras

- Um `[Fact]` por cenário — nunca testar duas coisas no mesmo teste
- Banco de dados em memória: use `Guid.NewGuid().ToString()` como nome do DB para isolamento
- Mocke todas as dependências externas com **Moq**
- Use **FluentAssertions** (`.Should().Be()`, `.Should().Throw<>()`, etc.)
- Nunca altere testes para fazê-los passar — corrija o código de produção
