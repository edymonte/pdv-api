using FluentAssertions;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging.Abstractions;
using PdvApi.Data;
using PdvApi.Models;
using PdvApi.Services;
using Xunit;

namespace PdvApi.Tests.Services;

public class VendaServiceTests
{
    private static PdvContext CriarContexto()
    {
        var options = new DbContextOptionsBuilder<PdvContext>()
            .UseInMemoryDatabase(databaseName: Guid.NewGuid().ToString())
            .Options;
        return new PdvContext(options);
    }

    [Fact]
    public async Task ObterPorIdAsync_Should_ReturnVenda_When_VendaExiste()
    {
        // Arrange
        await using var context = CriarContexto();
        var venda = new Venda { ClienteId = "CLI-001", Status = StatusVenda.Concluida };
        context.Vendas.Add(venda);
        await context.SaveChangesAsync();

        var service = new VendaService(context, NullLogger<VendaService>.Instance);

        // Act
        var resultado = await service.ObterPorIdAsync(venda.Id);

        // Assert
        resultado.Should().NotBeNull();
        resultado!.ClienteId.Should().Be("CLI-001");
    }

    [Fact]
    public async Task ObterPorIdAsync_Should_ReturnNull_When_VendaNaoExiste()
    {
        // Arrange
        await using var context = CriarContexto();
        var service = new VendaService(context, NullLogger<VendaService>.Instance);

        // Act
        var resultado = await service.ObterPorIdAsync(999);

        // Assert
        resultado.Should().BeNull();
    }

    [Fact]
    public async Task CriarVendaAsync_Should_PersistirVenda_When_DadosValidos()
    {
        // Arrange
        await using var context = CriarContexto();
        var service = new VendaService(context, NullLogger<VendaService>.Instance);
        var venda = new Venda { ClienteId = "CLI-999", Status = StatusVenda.Pendente };

        // Act
        var criada = await service.CriarVendaAsync(venda);

        // Assert
        criada.Id.Should().BeGreaterThan(0);
        context.Vendas.Count().Should().Be(1);
    }

    [Fact]
    public async Task Should_ReturnDictionaryWithAllStatusCounts_When_VendasExistemEmTodosOsStatus()
    {
        // Arrange
        await using var context = CriarContexto();
        context.Vendas.AddRange(
            new Venda { ClienteId = "CLI-001", Status = StatusVenda.Pendente },
            new Venda { ClienteId = "CLI-002", Status = StatusVenda.Concluida },
            new Venda { ClienteId = "CLI-003", Status = StatusVenda.Concluida },
            new Venda { ClienteId = "CLI-004", Status = StatusVenda.Cancelada },
            new Venda { ClienteId = "CLI-005", Status = StatusVenda.EmAnalise });
        await context.SaveChangesAsync();

        var service = new VendaService(context, NullLogger<VendaService>.Instance);

        // Act
        var relatorio = await service.ObterRelatorioPorStatusAsync();

        // Assert
        relatorio.Should().BeEquivalentTo(new Dictionary<string, int>
        {
            ["Pendente"] = 1,
            ["Concluida"] = 2,
            ["Cancelada"] = 1,
            ["EmAnalise"] = 1
        });
    }

    // ⚠️ WORKSHOP — testes de CancelarVendaAsync são gerados pelo agente no Bloco 2.
    // Padrão esperado de nomenclatura:
    //   Should_CancelarVenda_When_StatusConcluida
    //   Should_ThrowValidationError_When_VendaJaCancelada
    //   Should_ThrowValidationError_When_VendaNaoEncontrada
}
