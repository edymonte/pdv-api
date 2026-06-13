---
description: Bloco 6 — Gera a descrição do PR com o resumo de tudo que foi feito nos Blocos 2-5.
mode: chat
---

Gere a descrição deste PR resumindo as alterações feitas:

- Novo endpoint `POST /api/vendas/{id}/cancelar` com validação FluentValidation
- Service com lógica de devolução de estoque
- Integração com catálogo de produtos via MCP (verificação de produto ativo)
- Novo status `EmAnalise` e regra de cancelamento atualizada
- Correção automática de testes após autocorreção do agente (Bloco 4)
- Revisão aprovada pelo agente `@qa-boa-vista`

Siga o formato: título, resumo, o que foi alterado, testes adicionados, e como testar.
