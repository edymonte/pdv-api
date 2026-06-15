# API Standards — Farmácia Boa Vista (bvista-dev)

> Skill de padrões de API REST para o time de desenvolvimento do pdv-api.
> Use esta skill ao criar ou revisar endpoints, DTOs e contratos de API.

---

## Convenções de Endpoint

### Nomenclatura de rotas
- Substantivos no plural e em minúsculas: `/vendas`, `/produtos`, `/clientes`
- IDs como segmento de rota: `GET /vendas/{id}`
- Ações específicas como sub-recursos: `POST /vendas/{id}/cancelar`
- Nunca verbos na URL: ~~`POST /cancelarVenda`~~

### Métodos HTTP
| Operação | Método | Exemplo |
|---|---|---|
| Listar todos | GET | `GET /vendas` |
| Buscar por ID | GET | `GET /vendas/{id}` |
| Criar | POST | `POST /vendas` |
| Atualizar total | PUT | `PUT /vendas/{id}` |
| Atualizar parcial | PATCH | `PATCH /vendas/{id}` |
| Cancelar/Excluir | DELETE | `DELETE /vendas/{id}` |
| Ação de negócio | POST | `POST /vendas/{id}/cancelar` |

---

## Status Codes obrigatórios

```csharp
// Sucesso
200 OK           → GET com resultado, PUT, PATCH, POST de ação
201 Created      → POST criando recurso (+ Location header)
204 No Content   → DELETE

// Erros de cliente
400 Bad Request  → Validação falhou (FluentValidation)
404 Not Found    → Recurso não existe
409 Conflict     → Estado inválido (ex: venda já cancelada)

// Erros de servidor
500 Internal     → Nunca expor detalhes — log interno apenas
```

---

## Padrão de Response

### Sucesso (201 Created)
```json
{
  "id": 42,
  "status": "Aberta",
  "total": 150.00,
  "criadaEm": "2026-06-14T10:30:00Z"
}
```

### Erro de validação (400)
```json
{
  "errors": {
    "itens": ["A venda deve ter pelo menos um item."],
    "clienteId": ["ClienteId é obrigatório."]
  }
}
```

### Erro não encontrado (404)
```json
{
  "message": "Venda não encontrada."
}
```

---

## Controller Pattern obrigatório

```csharp
[ApiController]
[Route("api/[controller]")]
public class VendasController : ControllerBase
{
    private readonly IVendaService _service;

    public VendasController(IVendaService service) => _service = service;

    [HttpPost("{id}/cancelar")]
    public async Task<IActionResult> Cancelar(int id)
    {
        // Nenhuma lógica aqui — apenas delegar e mapear response
        await _service.CancelarVendaAsync(id);
        return NoContent();
    }
}
```

---

## O que NUNCA fazer

- ❌ Lógica de negócio no Controller
- ❌ Acesso direto ao DbContext no Controller
- ❌ Expor exceções internas (`Exception.Message` no response)
- ❌ Retornar 200 para erros de validação
- ❌ Usar verbos na URL
