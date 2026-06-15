namespace PdvApi.Models;

/// <summary>
/// Possíveis estados de uma venda no PDV.
/// </summary>
public enum StatusVenda
{
    Pendente = 0,
    Concluida = 1,
    Cancelada = 2,
    EmAnalise = 3
}
