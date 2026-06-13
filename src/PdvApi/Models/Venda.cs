namespace PdvApi.Models;

public class Venda
{
    public int Id { get; set; }
    public string ClienteId { get; set; } = string.Empty;
    public StatusVenda Status { get; set; }
    public DateTime DataVenda { get; set; } = DateTime.UtcNow;
    public List<ItemVenda> Itens { get; set; } = new();
}
