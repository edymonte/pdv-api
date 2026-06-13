---
description: Bloco 2 — Mesma tarefa do Bloco 1, agora COM instructions e skill ativas. Resultado esperado: código limpo, validação FluentValidation, testes no padrão AAA.
mode: agent
---

Implemente um endpoint POST /api/vendas/{id}/cancelar no pdv-api,
seguindo nossas instructions e o padrão da skill gerar-testes-pdv.

A regra de negócio: venda só pode ser cancelada se status = "Concluida",
e o estoque dos itens deve ser devolvido.

Crie:
- O método `CancelarVendaAsync(int id)` em `IVendaService` e `VendaService`
- O `CancelarVendaValidator` com FluentValidation
- O endpoint no `VendasController`
- Testes xUnit cobrindo: sucesso, venda já cancelada, e venda inexistente
