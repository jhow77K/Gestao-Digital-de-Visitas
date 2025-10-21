# Gestão Digital de Visitas

Este projeto é uma aplicação web desenvolvida pelos alunos do grupo 10 da UNIVESP utilizando o framework **Django**. O objetivo é fornecer uma solução completa para o gerenciamento de visitas escolares, incluindo funcionalidades para cadastro, edição, exclusão e visualização de escolas, visitas, pagamentos, monitores e usuários.

---

## Novidades e Melhorias Visuais

A interface foi completamente redesenhada para uma experiência mais moderna e intuitiva:

* **Novo Padrão Visual:** Todas as telas foram modernizadas com cards informativos, containers brancos, bordas arredondadas, sombras suaves e cores institucionais.
* **Dashboard Inicial:** Apresenta cards para escola, visitas agendadas e visitas concluídas, com contadores dinâmicos e layout responsivo.
* **Cards de Visitas:** A listagem das próximas visitas é feita em cards horizontais, exibindo informações detalhadas e ações rápidas.
* **Botão de Ação Destacado:** Um botão verde para agendar nova visita está sempre visível e acessível.
* **Interface Simplificada:** Elementos desnecessários, como saudações e alguns ícones, foram removidos para focar no conteúdo principal.
* **Formulários Aprimorados:** Os campos de formulários agora possuem maior espaçamento, melhorando a usabilidade.
* **Página de Login:** Conta com uma imagem de fundo para um visual mais atrativo.
* **Cadastro Inteligente de Escola:** Integração com a API ViaCEP para preenchimento automático de endereço a partir do CEP.
* **Padronização Visual:** Cards e tabelas seguem um padrão consistente, com cabeçalhos verdes, linhas alternadas, efeito `hover` e responsividade.
* **Feedback ao Usuário:** Mensagens de erro e sucesso foram padronizadas em todas as telas para uma melhor comunicação com o usuário.

## Funcionalidades Principais

* **Autenticação de Usuários:** Sistema de login seguro com senhas criptografadas.
* **Gerenciamento de Escolas:** CRUD completo para escolas.
* **Gerenciamento de Visitas:** Controle de visitas agendadas e realizadas, com detalhes como série dos alunos, clima e período.
* **Controle de Pagamentos:** Registro de pagamentos vinculados a visitas, com detalhamento de valores, formas de pagamento, nota fiscal, etc.
* **Cadastro de Monitores:** Gerenciamento de monitores vinculados às escolas.
* **Logs de Ações:** Registro de todas as ações importantes realizadas no sistema (`quem`, `o quê` e `quando`).
* **Busca e Filtros:** Funcionalidades de pesquisa por nome, série, escola, entre outros.
* **Paginação:** Listas longas são paginadas para uma navegação mais fluida.
* **Gráficos:** Visualização gráfica de visitas e pagamentos por escola.
* **Validação de Dados:** Validação no frontend (com máscaras) e no backend para garantir a integridade dos dados.
* **Responsividade:** Layout adaptado para uma boa experiência em desktops, tablets e smartphones.
* **Controle de Permissões:** Proteção de rotas sensíveis com login obrigatório.
* **Painel de Administração:** Acesso ao painel administrativo padrão do Django para gerenciamento avançado.

## Banco de Dados (MySQL)

O projeto utiliza o **MySQL** como banco de dados. Para rodar localmente, é necessário ter o MySQL instalado e configurado.

1.  No arquivo `settings.py`, configure as credenciais de acesso ao seu banco:

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

2.  Instale o conector do MySQL para Python:
    ```bash
    pip install mysqlclient
    ```

## Estrutura do Projeto

/ ├── manage.py ├── django_project/ │ ├── settings.py │ └── urls.py └── core/ ├── models.py ├── views.py ├── admin.py ├── filters.py ├── migrations/ ├── templates/core/ │ ├── base.html │ ├── home.html │ ├── login.html │ ├── cadastro_escola.html │ └── ... └── static/ ├── css/ ├── js/ └── images/


## Como Executar o Projeto

Siga os passos abaixo para configurar e rodar o ambiente de desenvolvimento.

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/jhow77K/projeto-django.git](https://github.com/jhow77K/projeto-django.git)
    cd projeto-django
    ```

2.  **Instale as dependências:**
    *(É recomendado criar um ambiente virtual antes)*
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure o banco de dados:**
    Crie um banco de dados no seu MySQL e atualize as credenciais no arquivo `settings.py`.

4.  **Execute as migrações:**
    ```bash
    python manage.py migrate
    ```

5.  **Crie um superusuário:**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Inicie o servidor de desenvolvimento:**
    ```bash
    python manage.py runserver
    ```

7.  **Acesse a aplicação** em seu navegador:
    [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Contribuição

Contribuições são muito bem-vindas! Sinta-se à vontade para abrir uma *issue* para relatar bugs ou sugerir melhorias, ou enviar um *pull request* com suas implementações.

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo `LICENSE` para mais detalhes.
