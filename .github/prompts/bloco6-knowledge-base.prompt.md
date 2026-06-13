---
description: Bloco 6 — Knowledge Base. O agente consulta a wiki do projeto para implementar uma regra de negócio real sem que você precise repeti-la no prompt.
mode: agent
---

Consulte @file:docs/wiki/regras-de-negocio.md e implemente a validação de desconto máximo no `VendaService`.

O método `CriarVendaAsync` deve rejeitar criações onde qualquer item tenha desconto superior ao limite definido na wiki.

Regras (use os valores exatos da documentação — não hardcode percentuais diferentes):
- Aplique o limite geral de desconto por item
- Para produtos da categoria `controlado` (verifique no catálogo via MCP se disponível), aplique o limite específico para controlados
- Use as mensagens de erro exatas definidas na wiki
- Retornar HTTP 422 quando o desconto for inválido

Crie ou atualize:
- `CriarVendaValidator` com as novas regras de desconto
- Testes xUnit cobrindo: item com desconto dentro do limite, item com desconto acima do limite, produto controlado com desconto acima do limite específico
- Siga o padrão de nomenclatura e estrutura de testes definido em @file:docs/wiki/arquitetura-decisoes.md
