# 👥 Time: Dev

Você está na branch **`feature/dev`** — branch oficial do time **Desenvolvimento**.

## Início rápido

```bash
git checkout feature/dev
git pull origin feature/dev
```

## Gerar evidência

Após executar todos os blocos do workshop:

```bash
python setup/gerar_evidencia.py --nome "Seu Nome Completo" --turma dev
```

O HTML de evidência será salvo em `evidencias/turma-dev-seu-nome.html`.

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
| **Bloco 8** | Abra PR de `feature/dev` → `main` e gere evidência |

> 💡 Todos os prompts prontos estão em `.github/prompts/` após ativar a governança.
