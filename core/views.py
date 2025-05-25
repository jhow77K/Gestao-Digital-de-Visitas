from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Escola, Visita, Pagamento, Monitor, Usuario
from django.contrib import messages
import hashlib
from datetime import datetime, date, timedelta
from django.contrib.auth import authenticate, login, logout
from django.db.models import ProtectedError
from .filters import EscolaFilter
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.utils.timezone import now
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q



def adicionar_escola(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        responsavel = request.POST.get('responsavel')
        endereco = request.POST.get('endereco')
        bairro = request.POST.get('bairro')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        cnpj = request.POST.get('cnpj')

        # Remove máscara para comparar apenas os números
        cnpj_limpo = ''.join(filter(str.isdigit, cnpj))
        # Verifica se já existe escola com esse CNPJ (ignorando máscara)
        if Escola.objects.filter(cnpj__regex=rf'\D*{cnpj_limpo[:2]}\D*{cnpj_limpo[2:5]}\D*{cnpj_limpo[5:8]}\D*{cnpj_limpo[8:12]}\D*{cnpj_limpo[12:]}').exists():
            messages.error(request, "Já existe uma escola cadastrada com este CNPJ.")
            return render(request, 'core/adicionar_escola.html')

        # Criação de uma nova instância do modelo Escola
        escola = Escola(
            nome=nome,
            responsavel=responsavel,
            endereco=endereco,
            bairro=bairro,
            telefone=telefone,
            email=email,
            cnpj=cnpj
        )
        escola.save()  # Salva a instância no banco de dados

        # Mensagem de sucesso
        messages.success(request, "Escola adicionada com sucesso!")
        return redirect('adicionar_visita')  # Redireciona para a mesma página após salvar

    return render(request, 'core/adicionar_escola.html')

def adicionar_visita(request):
    if request.method == 'POST':
        escola_id = request.POST.get('escola')
        data = request.POST.get('data')
        periodo = request.POST.get('periodo')
        clima = request.POST.get('clima')
        serie_alunos = request.POST.get('serie_alunos')

        # Validação da data
        if data and date.fromisoformat(data) < date.today():
            messages.error(request, "A data da visita não pode ser anterior à data atual.")
            escolas = Escola.objects.all()
            return render(request, 'core/adicionar_visita.html', {'escolas': escolas, 'today': date.today()})


        escola = Escola.objects.get(id=escola_id)

        # Cria uma nova visita
        visita = Visita(
            escola=escola,
            data=data,
            periodo=periodo,
            clima=clima,
            serie_alunos=serie_alunos
        )
        visita.save()

        # Mensagem de sucesso
        messages.success(request, "Visita adicionada com sucesso!")
        return redirect('adicionar_pagamento')

    escolas = Escola.objects.all()
    today = date.today()  # Obtém a data atual
    return render(request, 'core/adicionar_visita.html', {'escolas': escolas, 'today': today})

def adicionar_pagamento(request):
    if request.method == 'POST':
        escola_id = request.POST.get('escola')
        numero_criancas_pagantes = int(request.POST.get('numero_criancas_pagantes'))
        valor_por_crianca = float(request.POST.get('valor_por_crianca'))
        numero_adultos_pagantes = int(request.POST.get('numero_adultos_pagantes'))
        valor_por_adulto = float(request.POST.get('valor_por_adulto'))
        forma_pagamento = request.POST.get('forma_pagamento')
        nota_fiscal = request.POST.get('nota_fiscal') == 'on'
        recibo = request.POST.get('recibo') == 'on'
        agencia = request.POST.get('agencia') == 'on'
        comissao_percentual = request.POST.get('comissao')  # Recebe o valor da comissão como percentual
        numero_previsto_criancas = int(request.POST.get('numero_previsto_criancas'))
        numero_adultos_cortesia = int(request.POST.get('numero_adultos_cortesia'))

        # Calcula o total
        total = (numero_criancas_pagantes * valor_por_crianca) + \
                (numero_adultos_pagantes * valor_por_adulto)


        comissao = (float(comissao_percentual) / 100) * total if comissao_percentual else None


        escola = Escola.objects.get(id=escola_id)

        # Cria um novo pagamento
        pagamento = Pagamento(
            escola=escola,
            numero_criancas_pagantes=numero_criancas_pagantes,
            valor_por_crianca=valor_por_crianca,
            numero_adultos_pagantes=numero_adultos_pagantes,
            valor_por_adulto=valor_por_adulto,
            total=total,
            forma_pagamento=forma_pagamento,
            nota_fiscal=nota_fiscal,
            recibo=recibo,
            agencia=agencia,
            comissao=comissao,  
            numero_previsto_criancas=numero_previsto_criancas,
            numero_adultos_cortesia=numero_adultos_cortesia
        )
        pagamento.save()


        messages.success(request, "Pagamento adicionado com sucesso!")
        return redirect('adicionar_monitores') 

    escolas = Escola.objects.all()
    return render(request, 'core/adicionar_pagamento.html', {'escolas': escolas})

def adicionar_monitores(request):
    if request.method == 'POST':
        visita_id = request.POST.get('visita')
        monitores_fazendinha = request.POST.get('monitores_fazendinha')
        monitores_free = request.POST.get('monitores_free')
        guia_fazendinha = request.POST.get('guia_fazendinha')
        guias_free = request.POST.get('guias_free') 
        historico_passeio = request.POST.get('historico_passeio')  

        visita = Visita.objects.get(id=visita_id)

        monitor = Monitor(
            escola=visita.escola, 
            visita=visita,
            monitores_fazendinha=monitores_fazendinha,
            monitores_free=monitores_free,
            guia_fazendinha=guia_fazendinha,
            guias_free=guias_free,  
            historico_passeio=historico_passeio  
        )
        monitor.save()

        messages.success(request, "Monitores adicionados com sucesso!")
        return redirect('visualizar_dados') 

    visitas = Visita.objects.all()
    return render(request, 'core/adicionar_monitores.html', {'visitas': visitas})

def excluir_registro(request, tabela, id_registro):

    messages.success(request, f"Registro excluído com sucesso!")
    return redirect('visualizar_dados')

def editar_registro(request, tabela, id_registro):
    if request.method == 'POST':
        dados = request.POST.dict()

        messages.success(request, f"Registro editado com sucesso!")
        return redirect('visualizar_dados')


    return render(request, 'core/editar_registro.html')

def formatar_cnpj(cnpj):
    cnpj = ''.join(filter(str.isdigit, cnpj))
    if len(cnpj) == 14:
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
    return cnpj

def adicionar_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()


        messages.success(request, "Usuário cadastrado com sucesso!")
        return redirect('tela_login')

    return render(request, 'core/adicionar_usuario.html')

def verificar_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()


        messages.success(request, "Login realizado com sucesso!")
        return redirect('dashboard')

    return render(request, 'core/tela_login.html')

def home(request):

    data_atual = now().date()


    total_escolas = Escola.objects.count()


    visitas_agendadas = Visita.objects.filter(feita=False).count()

    visitas_realizadas = Visita.objects.filter(feita=True).count()


    pagamentos_recebidos = Pagamento.objects.filter(confirmado=True).aggregate(total=Sum('total'))['total'] or 0


    escolas = Escola.objects.all().order_by('-data_cadastro')[:3]


    proximas_visitas = Visita.objects.filter(data__gte=data_atual, feita=False).order_by('data')[:3]


    pagamentos = Pagamento.objects.filter(confirmado=False).order_by('-id')[:3]

    # Dados para o relatório e gráficos
    total_visitas_por_escola = Escola.objects.annotate(total_visitas=Count('visita')).order_by('-total_visitas')[:5]
    total_pagamentos_por_escola = Escola.objects.annotate(total_pagamentos=Sum('pagamento__total')).order_by('-total_pagamentos')[:5]

    context = {
        'total_escolas': total_escolas,
        'visitas_agendadas': visitas_agendadas,
        'visitas_realizadas': visitas_realizadas,
        'pagamentos_recebidos': pagamentos_recebidos,
        'escolas': escolas,
        'proximas_visitas': proximas_visitas,
        'pagamentos': pagamentos,
        'total_visitas_por_escola': total_visitas_por_escola,
        'total_pagamentos_por_escola': total_pagamentos_por_escola,
    }

    return render(request, 'core/home.html', context)

def tela_login(request):
    return render(request, 'core/login.html')

def visualizar_dados(request):
    query = request.GET.get('q', '').strip()
    escolas = Escola.objects.all()
    visitas = Visita.objects.all()
    pagamentos = Pagamento.objects.all()
    monitores = Monitor.objects.all()

    if query:
        # Busca para escolas
        escolas = escolas.filter(
            Q(nome__icontains=query) |
            Q(responsavel__icontains=query) |
            Q(bairro__icontains=query) |
            Q(telefone__icontains=query) |
            Q(endereco__icontains=query) |
            Q(cnpj__icontains=query)
        )
        # Busca para visitas (tratando data)
        try:
            data_query = datetime.strptime(query, "%d/%m/%Y").date()
            visitas = visitas.filter(
                Q(escola__nome__icontains=query) |
                Q(data=data_query) |
                Q(periodo__icontains=query) |
                Q(clima__icontains=query) |
                Q(serie_alunos__icontains=query)
            )
        except ValueError:
            visitas = visitas.filter(
                Q(escola__nome__icontains=query) |
                Q(periodo__icontains=query) |
                Q(clima__icontains=query) |
                Q(serie_alunos__icontains=query)
            )
        # Busca para pagamentos (tratando booleanos)
        pagamentos = pagamentos.filter(
            Q(escola__nome__icontains=query) |
            Q(forma_pagamento__icontains=query) |
            Q(comissao__icontains=query) |
            Q(nota_fiscal=True) if query.lower() in ['sim', 'true', '1'] else Q() |
            Q(recibo=True) if query.lower() in ['sim', 'true', '1'] else Q()
        )
        # Busca para monitores
        monitores = monitores.filter(
            Q(escola__nome__icontains=query) |
            Q(visita__escola__nome__icontains=query) |
            Q(monitores_fazendinha__icontains=query) |
            Q(monitores_free__icontains=query) |
            Q(guia_fazendinha__icontains=query) |
            Q(guias_free__icontains=query) |
            Q(historico_passeio__icontains=query)
        )

    context = {
        'escolas': escolas,
        'visitas': visitas,
        'pagamentos': pagamentos,
        'monitores': monitores,
        'query': query,
    }
    return render(request, 'core/visualizar_dados.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        # Validação simples no backend
        if not username or not password:
            messages.error(request, "Preencha todos os campos.")
            return render(request, 'core/login.html')

        if len(username) < 3 or len(password) < 6:
            messages.error(request, "Usuário deve ter pelo menos 3 caracteres e senha pelo menos 6.")
            return render(request, 'core/login.html')

        # Autenticação padrão Django
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Usuário, email ou senha incorretos.")
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  

def editar_pagamento(request, pagamento_id):
    pagamento = get_object_or_404(Pagamento, id=pagamento_id)

    if request.method == 'POST':
        pagamento.numero_criancas_pagantes = request.POST.get('numero_criancas_pagantes')
        pagamento.valor_por_crianca = request.POST.get('valor_por_crianca')
        pagamento.numero_adultos_pagantes = request.POST.get('numero_adultos_pagantes')
        pagamento.valor_por_adulto = request.POST.get('valor_por_adulto')
        pagamento.forma_pagamento = request.POST.get('forma_pagamento')
        pagamento.nota_fiscal = request.POST.get('nota_fiscal') == 'on'
        pagamento.recibo = request.POST.get('recibo') == 'on'
        pagamento.agencia = request.POST.get('agencia') == 'on'
        pagamento.comissao = request.POST.get('comissao')
        pagamento.numero_previsto_criancas = request.POST.get('numero_previsto_criancas')
        pagamento.numero_adultos_cortesia = request.POST.get('numero_adultos_cortesia')

        pagamento.total = (int(pagamento.numero_criancas_pagantes) * float(pagamento.valor_por_crianca)) + \
                          (int(pagamento.numero_adultos_pagantes) * float(pagamento.valor_por_adulto))

        pagamento.save()
        messages.success(request, "Pagamento atualizado com sucesso!")
        return redirect('listar_pagamentos')

    return render(request, 'core/editar_pagamento.html', {'pagamento': pagamento})

def excluir_pagamento(request, pagamento_id):
    pagamento = get_object_or_404(Pagamento, id=pagamento_id)
    pagamento.delete()
    messages.success(request, "Pagamento excluído com sucesso!")
    return redirect('visualizar_dados')

def editar_escola(request, escola_id):
    escola = get_object_or_404(Escola, id=escola_id)

    if request.method == 'POST':

        escola.nome = request.POST.get('nome')
        escola.responsavel = request.POST.get('responsavel')
        escola.endereco = request.POST.get('endereco')
        escola.bairro = request.POST.get('bairro')
        escola.telefone = request.POST.get('telefone')
        escola.email = request.POST.get('email')
        escola.cnpj = request.POST.get('cnpj')
        escola.save()


        Visita.objects.filter(escola=escola).update(escola=escola)
        Pagamento.objects.filter(escola=escola).update(escola=escola)
        Monitor.objects.filter(escola=escola).update(escola=escola)

        messages.success(request, "Escola e dados relacionados atualizados com sucesso!")
        return redirect('visualizar_dados')

    return render(request, 'core/editar_escola.html', {'escola': escola})

def excluir_escola(request, escola_id):
    escola = get_object_or_404(Escola, id=escola_id)


    if escola.visita_set.exists() or Pagamento.objects.filter(escola=escola).exists() or Monitor.objects.filter(escola=escola).exists():
        messages.error(request, "Não é possível excluir a escola porque ela possui visitas, pagamentos ou monitores relacionados.")
        return redirect('visualizar_dados')

    try:
        escola.delete()
        messages.success(request, "Escola excluída com sucesso!")
    except ProtectedError:
        messages.error(request, "Não é possível excluir a escola porque ela está protegida por registros relacionados.")
    
    return redirect('visualizar_dados')

def editar_visita(request, visita_id):
    visita = get_object_or_404(Visita, id=visita_id)

    if request.method == 'POST':
        visita.data = request.POST.get('data')
        visita.periodo = request.POST.get('periodo')
        visita.clima = request.POST.get('clima')
        visita.serie_alunos = request.POST.get('serie_alunos')
        visita.save()

        messages.success(request, "Visita editada com sucesso!")
        return redirect('visualizar_dados')

    return render(request, 'core/editar_visita.html', {'visita': visita})

def excluir_visita(request, visita_id):
    visita = get_object_or_404(Visita, id=visita_id)
    visita.delete()
    messages.success(request, "Visita excluída com sucesso!")
    return redirect('visualizar_dados')

def editar_monitor(request, monitor_id):
    monitor = get_object_or_404(Monitor, id=monitor_id)

    if request.method == 'POST':
        monitor.monitores_fazendinha = request.POST.get('monitores_fazendinha')
        monitor.monitores_free = request.POST.get('monitores_free')
        monitor.guia_fazendinha = request.POST.get('guia_fazendinha')
        monitor.guias_free = request.POST.get('guias_free')
        monitor.historico_passeio = request.POST.get('historico_passeio')
        monitor.save()

        messages.success(request, "Monitor editado com sucesso!")
        return redirect('visualizar_dados')

    return render(request, 'core/editar_monitor.html', {'monitor': monitor})

def excluir_monitor(request, monitor_id):
    monitor = get_object_or_404(Monitor, id=monitor_id)
    monitor.delete()
    messages.success(request, "Monitor excluído com sucesso!")
    return redirect('visualizar_dados')

def listar_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'core/listar_usuarios.html', {'usuarios': usuarios})

def adicionar_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')


        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, "Usuário cadastrado com sucesso!")
        return redirect('listar_usuarios')

    return render(request, 'core/adicionar_usuario.html')

def editar_usuario(request, usuario_id):
    user = get_object_or_404(User, id=usuario_id)

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        password = request.POST.get('password')
        if password:
            user.set_password(password)
        user.save()

        messages.success(request, "Usuário atualizado com sucesso!")
        return redirect('listar_usuarios')

    return render(request, 'core/editar_usuario.html', {'user': user})

def excluir_usuario(request, usuario_id):
    user = get_object_or_404(User, id=usuario_id)
    user.delete()
    messages.success(request, "Usuário excluído com sucesso!")
    return redirect('listar_usuarios')

def agendamentos_proximos(request):

    hoje = date.today()

    # Filtra visitas com datas nos próximos 7 dias
    proximos_dias = hoje + timedelta(days=7)
    visitas_proximas = Visita.objects.filter(data__range=[hoje, proximos_dias]).order_by('data')

    return render(request, 'core/agendamentos_proximos.html', {'visitas_proximas': visitas_proximas})

def marcar_visita_feita(request, visita_id):
    visita = get_object_or_404(Visita, id=visita_id)
    visita.feita = True
    visita.save()
    messages.success(request, "Visita marcada como FEITA com sucesso!")
    return redirect('visualizar_dados')

def marcar_pagamento_confirmado(request, pagamento_id):
    pagamento = get_object_or_404(Pagamento, id=pagamento_id)
    pagamento.confirmado = True
    pagamento.save()
    messages.success(request, "Pagamento confirmado com sucesso!")
    return redirect('visualizar_dados')

def cadastro_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        # Validação backend
        if not username or not email or not password:
            messages.error(request, "Preencha todos os campos.")
            return render(request, 'core/cadastro.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Nome de usuário já existe.")
            return render(request, 'core/cadastro.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email já cadastrado.")
            return render(request, 'core/cadastro.html')

        if len(password) < 6:
            messages.error(request, "A senha deve ter pelo menos 6 caracteres.")
            return render(request, 'core/cadastro.html')

        # Criação do usuário
        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Usuário cadastrado com sucesso!")
        return redirect('login')
    return render(request, 'core/cadastro.html')
