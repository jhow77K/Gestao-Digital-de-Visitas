## Stack
- Django (MTV), MySQL em dev, templates + JS (Chart.js para análises).

## Domínio
- Escola: dados cadastrais, CNPJ formatado no save.
- Visita: agendamento (status, data_sugerida, periodo, responsáveis, estimativas, observações, feedback).
- Pagamento: totais e valores por criança/adulto, NF/recibo, comissão, confirmado.
- Monitor: alocação de monitores/guias e histórico.

Relacionamentos:
- Escola 1—N Visita
- Visita 1—N Pagamento 
- Visita 1—N Monitor 

## Fluxos
1. Cadastro de escola e usuário.
2. Agendar visita (status SOLICITADO) e bloquear horários.
3. Operação altera status (CONFIRMADO/REALIZADO/CANCELADO) e feedback.
4. Pagamentos vinculados à visita (totais e documentos).

## Performance
- Queries: `select_related('escola')` nas listas de visitas e `.only(...)` quando aplicável.
- Índices: `Visita.data_sugerida`, `Visita.status`, `Visita.periodo` (+ índice composto `status, data_sugerida`).
- Dev: usar MySQL; inspecionar com django-debug-toolbar.

## Análises (home)
- KPIs: receita total, tamanho médio de grupo.
- Gráficos: visitas por mês (TruncMonth), visitas por status (Count).
- Render com Chart.js no template.

## Segurança
- Credenciais via `.env` (python-decouple).
- Acesso admin com `is_staff`/`is_superuser`.
- CSRF em formulários.

## Backlog
- Paginação e filtros server-side.
- Testes para models/views.
- Exportação CSV/Excel e logs de auditoria.