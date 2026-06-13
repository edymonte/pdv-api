using FluentValidation;
using PdvApi.Models;

namespace PdvApi.Validators;

public class CriarVendaValidator : AbstractValidator<Venda>
{
    public CriarVendaValidator()
    {
        RuleFor(v => v.ClienteId)
            .NotEmpty()
            .WithMessage("O identificador do cliente é obrigatório.");

        RuleFor(v => v.Itens)
            .NotEmpty()
            .WithMessage("A venda deve conter pelo menos um item.");

        RuleForEach(v => v.Itens).ChildRules(item =>
        {
            item.RuleFor(i => i.ProdutoId)
                .GreaterThan(0)
                .WithMessage("O identificador do produto deve ser maior que zero.");

            item.RuleFor(i => i.NomeProduto)
                .NotEmpty()
                .WithMessage("O nome do produto é obrigatório.");

            item.RuleFor(i => i.Quantidade)
                .GreaterThan(0)
                .WithMessage("A quantidade deve ser maior que zero.");

            item.RuleFor(i => i.PrecoUnitario)
                .GreaterThan(0)
                .WithMessage("O preço unitário deve ser maior que zero.");
        });
    }
}
