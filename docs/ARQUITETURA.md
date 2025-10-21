Arquitetura — Gestão Digital de Visitas

Este documento detalha a arquitetura técnica, o modelo de domínio e as decisões de implementação do sistema de Gestão de Visitas.

1. Stack de Tecnologias

A aplicação foi construída sobre uma stack moderna e robusta, seguindo o padrão MTV (Model-Template-View) do Django.

Backend:

Framework: Django

Linguagem: Python

Frontend:

Renderização: Django Templates (HTML renderizado no servidor)

Interatividade: JavaScript

Gráficos: Chart.js para visualização de dados no dashboard.

Banco de Dados:

Produção: MySQL (conforme README.md)

2. Modelo de Domínio

O núcleo do sistema é modelado em quatro entidades principais que se relacionam para gerenciar o fluxo de visitas.

Entidades Principais

Escola: Armazena os dados cadastrais da instituição. O CNPJ é formatado e validado automaticamente ao salvar.

Visita: Representa o agendamento em si, contendo informações como status (SOLICITADO, CONFIRMADO, etc.), data sugerida, período, responsáveis, estimativa de participantes, observações e feedback pós-visita.

Pagamento: Modela os dados financeiros, incluindo valores totais e por participante (criança/adulto), informações de nota fiscal/recibo, comissões e status de confirmação.

Monitor: Gerencia a alocação de monitores e guias para as visitas, mantendo um histórico de participações.

Relacionamentos

[Escola] 1--N [Visita] 1--N [Pagamento (Opcional)]
                      |
                      1--N [Monitor (Opcional)]


Uma Escola pode ter múltiplas Visitas.

Uma Visita pode ter múltiplos Pagamentos associados.

Uma Visita pode ter múltiplos Monitores alocados.

3. Fluxos Principais do Sistema

O ciclo de vida de uma visita segue um fluxo de trabalho bem definido:

Cadastro Inicial: O usuário cadastra uma nova Escola no sistema.

Agendamento: Uma nova Visita é criada com o status inicial SOLICITADO. O sistema realiza o bloqueio de horários para evitar conflitos.

Operação e Confirmação: A equipe de operações altera o status da visita para CONFIRMADO, REALIZADO ou CANCELADO, e pode registrar o feedback do cliente após a conclusão.

Gestão Financeira: Os Pagamentos são vinculados à visita, permitindo o controle de valores e o anexo de documentos fiscais.

4. Performance e Otimizações

Para garantir uma experiência de usuário fluida, diversas otimizações foram implementadas:

Otimização de Queries:

Uso de select_related('escola') nas listagens de visitas para evitar o problema de N+1 queries.

Utilização de .only(...) em consultas onde apenas um subconjunto de campos é necessário.

Indexação de Banco de Dados:

Criação de índices nos campos mais consultados da tabela Visita: data_sugerida, status e periodo.

Implementação de um índice composto em (status, data_sugerida) para acelerar filtros combinados.

Ambiente de Desenvolvimento:

Recomendação de uso do MySQL para agilidade no setup local.

Utilização da django-debug-toolbar para inspecionar queries, tempo de renderização e outras métricas de performance durante o desenvolvimento.

5. Análises e Dashboard (Página Home)

A página inicial funciona como um dashboard analítico para fornecer insights rápidos sobre a operação.

KPIs (Key Performance Indicators):

Receita total acumulada.

Tamanho médio de grupo por visita.

Gráficos:

Visitas por Mês: Gerado com TruncMonth para agregar os dados.

Visitas por Status: Gerado com Count e group_by para exibir a distribuição.

Implementação: Os dados são agregados no backend (view) e renderizados no frontend com a biblioteca Chart.js.

6. Segurança

As seguintes medidas foram adotadas para proteger a aplicação:

Credenciais Seguras: Todas as chaves secretas e credenciais são gerenciadas através de variáveis de ambiente com o pacote python-decouple, lendo a partir de um arquivo .env.

Controle de Acesso: O acesso ao painel administrativo e a áreas restritas é controlado pelos flags is_staff e is_superuser do modelo de usuário do Django.

Proteção contra CSRF: Todos os formulários POST são protegidos com o token CSRF padrão do Django para prevenir ataques de Cross-Site Request Forgery.

7. Backlog e Próximos Passos

Funcionalidades planejadas para futuras versões do projeto:

[ ] Implementar paginação e filtros server-side para otimizar a performance em listagens com grande volume de dados.

[ ] Desenvolver uma suíte de testes unitários e de integração para os models e views.

[ ] Criar funcionalidades para exportação de relatórios em formato CSV/Excel.

[ ] Implementar um sistema de logs de auditoria mais detalhado para registrar ações críticas dos usuários.