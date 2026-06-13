using Microsoft.EntityFrameworkCore;
using PdvApi.Data;
using PdvApi.Models;

namespace PdvApi.Services;

public class VendaService : IVendaService
{
    private readonly PdvContext _context;
    private readonly ILogger<VendaService> _logger;

    public VendaService(PdvContext context, ILogger<VendaService> logger)
    {
        _context = context;
        _logger = logger;
    }

    public async Task<Venda?> ObterPorIdAsync(int id)
    {
        return await _context.Vendas
            .Include(v => v.Itens)
            .FirstOrDefaultAsync(v => v.Id == id);
    }

    public async Task<IEnumerable<Venda>> ListarTodasAsync()
    {
        return await _context.Vendas
            .Include(v => v.Itens)
            .ToListAsync();
    }

    public async Task<Venda> CriarVendaAsync(Venda venda)
    {
        _context.Vendas.Add(venda);
        await _context.SaveChangesAsync();
        _logger.LogInformation("Venda {VendaId} criada para cliente {ClienteId}", venda.Id, venda.ClienteId);
        return venda;
    }

    // ⚠️ WORKSHOP — CancelarVendaAsync é gerado pelo agente nos Blocos 1-4.
    // Não implemente aqui antes da demo.
}
