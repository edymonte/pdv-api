# Regras de Negócio — PDV Farmácia Boa Vista

> Este documento é a fonte de verdade para regras de negócio do sistema PDV.
> O Copilot consulta este arquivo para gerar código alinhado com as políticas da Boa Vista.

---

## Cancelamento de Vendas

- Venda pode ser cancelada se `status = Concluida` ou `status = EmAnalise`
- Cancelamento gera **devolução automática ao estoque** de todos os itens
- Prazo máximo para cancelamento: **30 dias** após a data da venda
- Vendas com medicamento controlado exigem registro obrigatório de motivo (`motivo_cancelamento`)
- Mensagem de erro quando fora do prazo: `"Cancelamento fora do prazo permitido de 30 dias."`

## Descontos

- Desconto máximo sem aprovação gerencial: **15%** por item
- Descontos acima de 15% exigem campo `aprovacao_gerente_id` preenchido
- Para produtos da categoria **medicamento controlado**: desconto máximo de **5%**
- Mensagem de erro quando desconto excede o limite: `"Desconto de {valor}% excede o limite permitido de {limite}% para este produto."`
- Mensagem de erro quando falta aprovação: `"Desconto acima de 15% requer aprovação gerencial."`

## Estoque

- Alerta de reposição quando quantidade em estoque **< 10 unidades**
- Produtos com `ativo = 0` **não podem** entrar em novas vendas
  - Mensagem: `"Produto {nome} está inativo no catálogo e não pode ser vendido."`
- Devolução de estoque é **obrigatória** em todo cancelamento — sem exceções
- Estoque nunca pode ficar negativo; rejeitar venda se quantidade disponível < quantidade solicitada
  - Mensagem: `"Estoque insuficiente para {nome}: disponível {qtd}, solicitado {qtd_pedida}."`

## Fluxo de Status da Venda

```
Pendente ──→ Concluida      (pagamento confirmado)
Pendente ──→ Cancelada      (desistência antes do pagamento)
Concluida ─→ EmAnalise      (contestação aberta, suspeita de fraude)
EmAnalise ─→ Concluida      (contestação resolvida em favor da farmácia)
EmAnalise ─→ Cancelada      (fraude confirmada ou devolução aprovada)
```

Transições **não permitidas**:
- `Cancelada` → qualquer estado (cancelamento é irreversível)
- `Concluida` → `Cancelada` diretamente (deve passar por `EmAnalise` se houver suspeita)

## Produtos Controlados

- Identificados pelo campo `categoria = 'controlado'` no catálogo de produtos
- Exigem **receita médica válida** para venda (campo `numero_receita` obrigatório)
- Limite: **uma embalagem por receita** para psicotrópicos e entorpecentes
- O número de CRM do médico e número da receita devem ser registrados na venda
