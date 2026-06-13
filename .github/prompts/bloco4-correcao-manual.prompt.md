---
description: Bloco 4 — Plano B. Use se o hook não disparar automaticamente. Cole a saída do dotnet test onde indicado.
mode: agent
---

Os testes abaixo falharam após a última alteração. Analise o erro,
identifique a causa raiz e corrija o código necessário para que os
testes voltem a passar, sem alterar o comportamento das regras de
negócio já existentes.

Saída do `dotnet test`:

```
[COLE AQUI A SAÍDA DO TERMINAL]
```

---

> **Plano B do Plano B — "quebra garantida"** (se o Prompt 4 não quebrar nada):
>
> Renomeie o método `CancelarVendaAsync` no `IVendaService` e na implementação
> para `CancelarAsync`, mantendo a mesma assinatura.
>
> Isso garantirá erro de build em todos os lugares que chamam o nome antigo.
