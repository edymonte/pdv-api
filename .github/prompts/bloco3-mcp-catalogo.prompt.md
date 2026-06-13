---
description: Bloco 3 — Integração com MCP de catálogo de produtos. O agente consulta o banco SQLite antes de devolver o estoque.
mode: agent
---

Antes de devolver o estoque no cancelamento de venda, valide se cada
produto da venda ainda existe no catálogo de produtos.

Use o MCP de produtos (banco SQLite `db/catalogo-produtos.db`) para consultar
a tabela `produtos` e verificar se o produto está ativo (`ativo = 1`).

Se um produto não existir mais no catálogo (como o produto id=5, descontinuado),
registre um log de aviso em português mas continue o cancelamento normalmente.

Atualize `VendaService.CancelarVendaAsync` para incluir essa validação.
