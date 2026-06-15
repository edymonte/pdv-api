using PdvApi.Models;

namespace PdvApi.Services;

public interface IVendaService
{
    Task<Venda?> ObterPorIdAsync(int id);
    Task<IEnumerable<Venda>> ListarTodasAsync();
    Task<IDictionary<string, int>> ObterRelatorioPorStatusAsync();
    Task<Venda> CriarVendaAsync(Venda venda);
    // CancelarVendaAsync será implementado durante o workshop (Blocos 1-4)
}
