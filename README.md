# Django Project

Este projeto é uma aplicação web desenvolvida com Django, que permite o gerenciamento de visitas a escolas, incluindo funcionalidades para adicionar, editar, excluir e visualizar registros de escolas, visitas, pagamentos e monitores.

## Estrutura do Projeto

- **manage.py**: Ponto de entrada para a linha de comando do Django.
- **django_project/**: Contém a configuração principal do projeto.
  - **__init__.py**: Indica que este diretório é um pacote Python.
  - **asgi.py**: Configuração para o ASGI (Asynchronous Server Gateway Interface).
  - **settings.py**: Configurações do projeto, incluindo banco de dados e aplicativos instalados.
  - **urls.py**: Define as rotas principais do projeto.
  - **wsgi.py**: Configuração para o WSGI (Web Server Gateway Interface).
- **app/**: Contém a lógica da aplicação.
  - **__init__.py**: Indica que este diretório é um pacote Python.
  - **admin.py**: Registro de modelos no painel de administração do Django.
  - **apps.py**: Configuração da aplicação.
  - **migrations/**: Contém arquivos de migração do banco de dados.
  - **models.py**: Define os modelos do banco de dados.
  - **tests.py**: Testes automatizados para a aplicação.
  - **urls.py**: Rotas específicas da aplicação.
  - **views.py**: Contém as views da aplicação.
- **templates/**: Contém templates HTML.
  - **base.html**: Template base para a aplicação.
- **static/**: Contém arquivos estáticos (CSS, JavaScript, imagens).
- **db.sqlite3**: Banco de dados SQLite utilizado pelo projeto.

## Como Executar o Projeto

1. Clone o repositório:
   ```
   git clone <URL_DO_REPOSITORIO>
   cd django_project
   ```

2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

3. Execute as migrações:
   ```
   python manage.py migrate
   ```

4. Inicie o servidor de desenvolvimento:
   ```
   python manage.py runserver
   ```

5. Acesse a aplicação em seu navegador: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.