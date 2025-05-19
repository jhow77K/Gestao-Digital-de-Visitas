# Sistema de Gerenciamento de Visitas Escolares

Este projeto é uma aplicação web desenvolvida pelos alunos do grupo 10 da UNIVESP utilizando o framework Django para o gerenciamento de visitas a escolas, incluindo funcionalidades completas para cadastro, edição, exclusão e visualização de escolas, visitas, pagamentos, monitores e usuários.

## Funcionalidades

- **Autenticação de Usuários:** Utiliza o sistema padrão do Django, com senhas criptografadas.
- **Cadastro e Gerenciamento de Escolas:** Adição, edição, exclusão e listagem de escolas.
- **Cadastro e Gerenciamento de Visitas:** Controle de visitas agendadas e realizadas, com série dos alunos, clima, período e vínculo com a escola.
- **Pagamentos:** Registro de pagamentos vinculados a visitas e escolas, com detalhamento de valores, formas de pagamento, nota fiscal, comissão, cortesia, etc.
- **Cadastro de Monitores:** Gerenciamento de monitores vinculados às escolas.
- **Logs de Ações:** Registro de quem fez o quê e quando no sistema.
- **Mensagens de Feedback:** Sucesso e erro em todas as ações importantes.
- **Busca e Filtros:** Pesquisa por nome, série, escola, etc.
- **Paginação:** Listas de escolas, visitas e pagamentos paginadas para melhor navegação.
- **Gráficos:** Visualização gráfica de visitas e pagamentos por escola.
- **Validação de Dados:** Validação no frontend e backend para todos os formulários.
- **Formatação Automática:** Máscaras para CNPJ, telefone e email nos formulários.
- **Responsividade:** Layout adaptado para dispositivos móveis.
- **Permissões:** Proteção de views sensíveis com login obrigatório.
- **Administração:** Painel administrativo padrão do Django para gerenciamento avançado.

## Banco de Dados

O projeto utiliza o **MySQL** como banco de dados principal.  
Para rodar localmente, é necessário ter o MySQL instalado e configurado.  
No arquivo `settings.py`, configure as credenciais de acesso ao seu banco, por exemplo:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nome_do_banco',
        'USER': 'usuario_mysql',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

Também é necessário instalar o conector do MySQL para Python:
```
pip install mysqlclient
```

## Estrutura do Projeto

- **manage.py**: Ponto de entrada para a linha de comando do Django.
- **django_project/**: Configuração principal do projeto.
  - **settings.py**: Configurações globais, apps instalados, banco de dados, etc.
  - **urls.py**: Rotas principais do projeto.
- **core/**: Aplicação principal.
  - **models.py**: Modelos de Escola, Visita, Pagamento, Monitor, LogAcao, etc.
  - **views.py**: Lógica das views (cadastro, edição, exclusão, autenticação, logs, etc).
  - **admin.py**: Registro dos modelos no admin.
  - **forms.py**: (Opcional) Formulários customizados.
  - **migrations/**: Arquivos de migração do banco de dados.
  - **filters.py**: Filtros de busca.
- **templates/core/**: Templates HTML.
  - **base.html**: Template base.
  - **home.html**: Página inicial com dashboards e gráficos.
  - **login.html**: Tela de login.
  - **adicionar_escola.html**, **adicionar_visita.html**, **adicionar_pagamento.html**, etc.
  - **visualizar_dados.html**: Listagem e busca de dados.
- **static/**: Arquivos estáticos (CSS, JS, imagens).

## Como Executar o Projeto

1. Clone o repositório:
   ```
   git clone https://github.com/jhow77K/projeto-django.git
   cd django_project
   ```

2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

3. Configure o banco de dados MySQL no `settings.py` e crie o banco no MySQL.

4. Execute as migrações:
   ```
   python manage.py migrate
   ```

5. Crie um superusuário para acessar o admin:
   ```
   python manage.py createsuperuser
   ```

6. Inicie o servidor de desenvolvimento:
   ```
   python manage.py runserver
   ```

7. Acesse a aplicação em seu navegador: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.