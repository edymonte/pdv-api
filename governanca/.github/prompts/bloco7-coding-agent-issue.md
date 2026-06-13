# Bloco 7 — Texto da Issue para o Coding Agent Demo

> Use o conteúdo abaixo ao criar a issue no GitHub.com para atribuir ao Copilot.
> Acesse: github.com/edymonte/pdv-api/issues → New issue

---

## Título da issue

```
feat: endpoint GET /api/vendas/relatorio — contagem por status
```

## Corpo da issue

```
### Contexto

O time precisa de um endpoint de relatório que permita visualizar rapidamente
quantas vendas existem em cada status do sistema PDV.

### Critérios de aceite

- Endpoint: `GET /api/vendas/relatorio`
- Retorno: objeto com contagem de vendas agrupadas por `StatusVenda`
- Formato de resposta:
  ```json
  {
    "Pendente": 5,
    "Concluida": 12,
    "Cancelada": 3,
    "EmAnalise": 1
  }
  ```
- Seguir os padrões de arquitetura do repositório (services, FluentValidation onde aplicável)
- Adicionar teste unitário cobrindo o novo endpoint
- Sem queries SQL com interpolação de string

### Como atribuir ao Copilot

No campo **Assignees**, selecione **Copilot**.
O agente vai explorar o codebase, implementar seguindo o `AGENTS.md` e abrir um draft PR automaticamente.
```

---

## O que observar durante a execução

1. O Copilot vai ler `.github/copilot-instructions.md` antes de escrever qualquer linha
2. Vai buscar o padrão de controllers e services já existentes no projeto
3. Vai escrever testes seguindo `testes.instructions.md`
4. O CI vai rodar automaticamente no PR — se quebrar, o Copilot itera sozinho
5. O PR abre como **draft** com scan de segurança incluso
