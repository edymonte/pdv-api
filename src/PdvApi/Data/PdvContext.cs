using Microsoft.EntityFrameworkCore;
using PdvApi.Models;

namespace PdvApi.Data;

public class PdvContext : DbContext
{
    public PdvContext(DbContextOptions<PdvContext> options) : base(options) { }

    public DbSet<Venda> Vendas => Set<Venda>();
    public DbSet<ItemVenda> Itens => Set<ItemVenda>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Venda>()
            .HasMany(v => v.Itens)
            .WithOne(i => i.Venda)
            .HasForeignKey(i => i.VendaId);

        // Dados de seed para o workshop
        modelBuilder.Entity<Venda>().HasData(
            new Venda { Id = 1, ClienteId = "CLI-001", Status = StatusVenda.Concluida, DataVenda = DateTime.UtcNow.AddHours(-2) },
            new Venda { Id = 2, ClienteId = "CLI-002", Status = StatusVenda.Pendente, DataVenda = DateTime.UtcNow.AddHours(-1) },
            new Venda { Id = 3, ClienteId = "CLI-003", Status = StatusVenda.Cancelada, DataVenda = DateTime.UtcNow.AddHours(-3) }
        );

        modelBuilder.Entity<ItemVenda>().HasData(
            new ItemVenda { Id = 1, VendaId = 1, ProdutoId = 1, NomeProduto = "Dipirona 500mg", Quantidade = 2, PrecoUnitario = 8.50m },
            new ItemVenda { Id = 2, VendaId = 1, ProdutoId = 3, NomeProduto = "Soro Fisiológico 250ml", Quantidade = 1, PrecoUnitario = 4.90m },
            new ItemVenda { Id = 3, VendaId = 2, ProdutoId = 5, NomeProduto = "Protetor Solar FPS 60", Quantidade = 1, PrecoUnitario = 45.00m }
        );
    }
}
