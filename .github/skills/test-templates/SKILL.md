# Test Templates — Farmácia Boa Vista (bvista-qa)

> Skill de templates de testes xUnit para o time de QA do pdv-api.
> Use esta skill ao criar testes para Services, Controllers e Validators.

---

## Template: Teste de Service (padrão completo)

```csharp
using FluentAssertions;
using Moq;
using PdvApi.Models;
using PdvApi.Services;
using Xunit;

namespace PdvApi.Tests.Services;

public class [NomeDoService]Tests
{
    private readonly Mock<I[NomeDoRepository]> _mockRepository;
    private readonly [NomeDoService] _service;

    public [NomeDoService]Tests()
    {
        _mockRepository = new Mock<I[NomeDoRepository]>();
        _service = new [NomeDoService](_mockRepository.Object);
    }

    [Fact]
    public async Task Should_[Resultado]_When_[CondicaoSucesso]()
    {
        // Arrange
        var entidade = new [Modelo] { Id = 1, /* propriedades */ };
        _mockRepository
            .Setup(r => r.GetByIdAsync(1))
            .ReturnsAsync(entidade);

        // Act
        var result = await _service.[Metodo]Async(1);

        // Assert
        result.Should().NotBeNull();
        result.Id.Should().Be(1);
    }

    [Fact]
    public async Task Should_ThrowValidationError_When_EntidadeNaoEncontrada()
    {
        // Arrange
        _mockRepository
            .Setup(r => r.GetByIdAsync(99))
            .ReturnsAsync((Venda?)null);

        // Act
        var act = async () => await _service.[Metodo]Async(99);

        // Assert
        await act.Should()
            .ThrowAsync<ValidationException>()
            .WithMessage("[Entidade] não encontrada.");
    }

    [Fact]
    public async Task Should_ThrowValidationError_When_EntradaInvalida()
    {
        // Arrange
        var idInvalido = 0;

        // Act
        var act = async () => await _service.[Metodo]Async(idInvalido);

        // Assert
        await act.Should()
            .ThrowAsync<ValidationException>();
    }
}
```

---

## Template: Teste de Validator (FluentValidation)

```csharp
using FluentValidation.TestHelper;
using PdvApi.Models;
using PdvApi.Validators;
using Xunit;

namespace PdvApi.Tests.Validators;

public class [NomeDoValidator]Tests
{
    private readonly [NomeDoValidator] _validator = new();

    [Fact]
    public void Should_HaveNoErrors_When_ModeloValido()
    {
        // Arrange
        var modelo = new [Modelo]
        {
            // propriedades válidas
        };

        // Act
        var result = _validator.TestValidate(modelo);

        // Assert
        result.ShouldNotHaveAnyValidationErrors();
    }

    [Theory]
    [InlineData(0)]
    [InlineData(-1)]
    public void Should_HaveError_When_[Campo]Invalido(int valorInvalido)
    {
        // Arrange
        var modelo = new [Modelo] { [Campo] = valorInvalido };

        // Act
        var result = _validator.TestValidate(modelo);

        // Assert
        result.ShouldHaveValidationErrorFor(m => m.[Campo]);
    }
}
```

---

## Regras de nomenclatura

| Padrão | Exemplo |
|---|---|
| Sucesso | `Should_ReturnVenda_When_IdValido` |
| Entidade não encontrada | `Should_ThrowValidationError_When_VendaNaoEncontrada` |
| Entrada inválida | `Should_ThrowValidationError_When_ItensVazios` |
| Estado inválido | `Should_ThrowValidationError_When_VendaJaCancelada` |
| Verificar chamada | `Should_CallRepository_When_Sucesso` |

---

## Ferramentas obrigatórias

- **xUnit** — framework de testes
- **Moq** — mock de dependências (repositórios, services externos)
- **FluentAssertions** — assertions legíveis (`result.Should().Be(...)`)
- **FluentValidation.TestHelper** — testes de validators

---

## O que NUNCA fazer em testes

- ❌ `Assert.Equal` — use `result.Should().Be()`
- ❌ Lógica complexa no `// Arrange` — extraia para métodos privados
- ❌ Testar detalhes de implementação — teste comportamento
- ❌ Testes sem `// Arrange / // Act / // Assert` comments
- ❌ Nome genérico como `Test1`, `TestarCancelar`
