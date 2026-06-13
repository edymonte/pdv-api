---
description: Bloco 3 (extensão) — MCP fetch. O agente busca documentação externa em tempo real e usa o conteúdo para implementar código. Demonstra que o agente não está limitado ao repositório local.
mode: agent
---

Use o MCP `fetch` para buscar o conteúdo desta página da ANVISA:
https://www.gov.br/anvisa/pt-br/assuntos/medicamentos/cmed/precos

Leia o conteúdo retornado e responda:
1. O que é a CMED e qual é o seu papel na regulação de preços de medicamentos?
2. Quais categorias de medicamentos estão sujeitas ao controle de preços?

Em seguida, com base no que você leu, adicione um comentário XML de documentação
no método `CriarVendaAsync` de `VendaService.cs` explicando a obrigatoriedade
de respeitar o preço máximo ao consumidor (PMC) definido pela CMED para
medicamentos — mesmo que a validação completa não esteja implementada nesta versão.

O comentário deve citar a fonte (ANVISA/CMED) e estar em português.
