---
applyTo: "src/**/Validators/*.cs"
---

# Padrões de Validação — pdv-api

Ao gerar ou modificar Validators neste projeto:

## Estrutura obrigatória

```csharp
using FluentValidation;
using PdvApi.Models;

namespace PdvApi.Validators;

public class NomeDaAcaoValidator : AbstractValidator<NomeDoRequest>
{
    public NomeDaAcaoValidator()
    {
        RuleFor(x => x.Propriedade)
            .NotEmpty().WithMessage("Mensagem de erro em português.");
    }
}
```

## Regras de negócio para Vendas

- **Cancelamento:** somente vendas com `Status == StatusVenda.Concluida` podem ser canceladas
- Vendas `Cancelada` ou `Pendente` devem retornar erro de validação — não lançar exceção
- Mensagens de erro sempre em **português (pt-BR)**

## Exemplos de mensagens

```
"Venda não encontrada."
"Somente vendas com status 'Concluída' podem ser canceladas."
"Quantidade deve ser maior que zero."
```

## Integração com Controller

O Controller deve usar `IValidator<T>` via injeção de dependência e retornar `BadRequest(result.Errors)` quando a validação falhar — nunca deixar a exceção subir para o middleware.
