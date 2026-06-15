using FluentAssertions;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using Moq;
using PdvApi.Controllers;
using PdvApi.Services;
using Xunit;

namespace PdvApi.Tests.Controllers;

public class VendasControllerTests
{
    [Fact]
    public async Task Should_ReturnOkWithSalesCountByStatus_When_RelatorioIsRequested()
    {
        // Arrange
        var vendaServiceMock = new Mock<IVendaService>();
        var loggerMock = new Mock<ILogger<VendasController>>();
        var relatorioEsperado = new Dictionary<string, int>
        {
            ["Pendente"] = 5,
            ["Concluida"] = 12,
            ["Cancelada"] = 3,
            ["EmAnalise"] = 1
        };

        vendaServiceMock
            .Setup(service => service.ObterRelatorioPorStatusAsync())
            .ReturnsAsync(relatorioEsperado);

        var controller = new VendasController(vendaServiceMock.Object, loggerMock.Object);

        // Act
        var resultado = await controller.ObterRelatorio();

        // Assert
        var okResult = resultado.Should().BeOfType<OkObjectResult>().Subject;
        okResult.Value.Should().BeEquivalentTo(relatorioEsperado);
    }
}
