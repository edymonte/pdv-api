# Regulatório e Conformidade — Farmácia Boa Vista

> Regras derivadas de legislação vigente. O código deve aderir a estes requisitos.
> Não faça exceções sem aprovação da equipe de compliance.

---

## Medicamentos Controlados — ANVISA (Portaria SVS/MS 344/98)

- Venda exige **receita médica válida** — sem exceção
- A receita deve ser **retida** pela farmácia e o número registrado no sistema
- Limite por receita:
  - Psicotrópicos (Lista C1, C3): **1 embalagem**
  - Entorpecentes (Lista A1, A2): **1 embalagem**
  - Outros controlados: conforme indicação da receita, máximo 2
- Campos obrigatórios na venda de controlado:
  - `numero_receita` — número da receita médica
  - `crm_medico` — CRM do médico prescritor
  - `data_receita` — data de emissão (validade: 30 dias para manipulados, 60 dias para industrializados)
- Mensagem de erro quando receita ausente: `"Venda de medicamento controlado exige receita médica válida."`

## LGPD — Dados Pessoais de Saúde (Lei 13.709/2018, Art. 11)

- Dados de saúde são **dados sensíveis** — tratamento exige consentimento explícito
- **Nunca logar** em texto aberto: CPF, número de receita, CRM, histórico de doenças
- Use mascaramento nos logs: CPF → `***.***.***-**`, CRM → `CRM-***`
- Retenção de histórico de compras: **máximo 5 anos** após a última compra
- Consentimento para programas de fidelidade deve ser registrado com timestamp
- Em caso de vazamento: notificar a ANPD em até **72 horas**

## Nota Fiscal Eletrônica (NF-e)

- Emissão obrigatória para vendas acima de **R$ 50,00**
- NF-e deve ser emitida em até **10 minutos** após conclusão da venda
- Campos obrigatórios: CNPJ da farmácia, CPF do cliente (opcional se < R$ 500), itens, CFOP
- Para medicamentos controlados: incluir número da receita no campo de observações

## Auditoria e Rastreabilidade

- Toda alteração de status de venda deve ser registrada com: usuário, timestamp, motivo
- Logs de acesso a dados sensíveis devem ser mantidos por **2 anos**
- Cancelamentos de vendas com controlados geram registro automático no livro de ocorrências
