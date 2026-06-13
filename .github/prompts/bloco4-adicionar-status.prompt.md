---
description: Bloco 4 — Prompt que PROPOSITALMENTE pode quebrar build/teste. É o gatilho do momento de autocorreção.
mode: agent
---

Adicione um novo status de venda "EmAnalise" no enum StatusVenda,
e atualize a regra de cancelamento: vendas "EmAnalise" também podem
ser canceladas (além das "Concluida").

Atualize o `VendaService`, o `CancelarVendaValidator` e os testes xUnit.
