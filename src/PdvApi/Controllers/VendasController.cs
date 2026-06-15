using Microsoft.AspNetCore.Mvc;
using PdvApi.Models;
using PdvApi.Services;

namespace PdvApi.Controllers;

[ApiController]
[Route("api/vendas")]
public class VendasController : ControllerBase
{
    private readonly IVendaService _vendaService;
    private readonly ILogger<VendasController> _logger;

    public VendasController(IVendaService vendaService, ILogger<VendasController> logger)
    {
        _vendaService = vendaService;
        _logger = logger;
    }

    /// <summary>GET /api/vendas — lista todas as vendas.</summary>
    [HttpGet]
    public async Task<IActionResult> Listar()
    {
        var vendas = await _vendaService.ListarTodasAsync();
        return Ok(vendas);
    }

    /// <summary>GET /api/vendas/relatorio — retorna a contagem de vendas por status.</summary>
    [HttpGet("relatorio")]
    public async Task<IActionResult> ObterRelatorio()
    {
        var relatorio = await _vendaService.ObterRelatorioPorStatusAsync();
        return Ok(relatorio);
    }

    /// <summary>GET /api/vendas/{id} — retorna uma venda pelo ID.</summary>
    [HttpGet("{id:int}")]
    public async Task<IActionResult> ObterPorId(int id)
    {
        var venda = await _vendaService.ObterPorIdAsync(id);
        if (venda is null)
            return NotFound(new { mensagem = $"Venda {id} não encontrada." });

        return Ok(venda);
    }

    /// <summary>POST /api/vendas — cria uma nova venda.</summary>
    [HttpPost]
    public async Task<IActionResult> Criar([FromBody] Venda venda)
    {
        if (!ModelState.IsValid)
            return UnprocessableEntity(ModelState);

        var criada = await _vendaService.CriarVendaAsync(venda);
        return CreatedAtAction(nameof(ObterPorId), new { id = criada.Id }, criada);
    }

    // ⚠️ WORKSHOP — POST /api/vendas/{id}/cancelar é gerado nos Blocos 1-4.
}
