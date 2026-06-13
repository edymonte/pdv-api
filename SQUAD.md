# 👥 Time: Suporte

Você está na branch **`feature/suporte`** — branch oficial do time **Suporte**.

## Início rápido

```bash
git checkout feature/suporte
git pull origin feature/suporte
```

## Gerar evidência

Após executar todos os blocos do workshop:

```bash
python setup/gerar_evidencia.py --nome "Seu Nome Completo" --turma suporte
```

O HTML de evidência será salvo em `evidencias/turma-suporte-seu-nome.html`.

## Seu fluxo no workshop

| Bloco | O que fazer |
|-------|-------------|
| **Bloco 1** | Agente sem regras — observe o comportamento sem governança |
| **Bloco 2** | `bash setup/ativar-governanca.sh` → Instructions + Skills ativos |
| **Bloco 3** | MCP sqlite — consulta ao catálogo de produtos |
| **Bloco 4** | Hook de autocorreção — deixe o agente quebrar e se recuperar |
| **Bloco 5** | `@qa-boa-vista` — revisor de qualidade ativo |
| **Bloco 6** | Descrição automática de PR com modo:chat |
| **Bloco 7** | `gh copilot suggest` no terminal |
| **Bloco 8** | Abra PR de `feature/suporte` → `main` e gere evidência |

> 💡 Todos os prompts prontos estão em `.github/prompts/` após ativar a governança.
