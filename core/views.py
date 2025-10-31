from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.views.decorators.http import require_POST
from datetime import datetime, time, timedelta
from django.contrib.admin.views.decorators import staff_member_required 

from .models import Escola, Visita

def formatar_cnpj(cnpj):
    cnpj = ''.join(filter(str.isdigit, cnpj))
    if len(cnpj) == 14:
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
    return cnpj

def cadastro_escola(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cep = request.POST.get('cep')
        endereco = request.POST.get('endereco')
        bairro = request.POST.get('bairro')
        cidade = request.POST.get('cidade')
        estado = request.POST.get('estado')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        cnpj = request.POST.get('cnpj')
        senha = request.POST.get('senha')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Já existe um usuário com este e-mail.")
            return render(request, 'core/cadastro_escola.html')

        user = User.objects.create_user(username=email, email=email, password=senha)
        user.save()

        escola = Escola.objects.create(
            nome=nome,
            cep=cep,
            endereco=endereco,
            bairro=bairro,
            cidade=cidade,
            estado=estado,
            telefone=telefone,
            email=email,
            cnpj=cnpj,
        )
        escola.save()

        messages.success(request, "Cadastro realizado com sucesso! Faça login para continuar.")
        return redirect('login')
    return render(request, 'core/cadastro_escola.html')

def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username_or_email or not password:
            messages.error(request, "Preencha todos os campos.")
            return render(request, 'core/login.html')

        user = authenticate(request, username=username_or_email, password=password)

        if user is None:
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin_dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, "Usuário, email ou senha incorretos.")
            return render(request, 'core/login.html')

    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    if request.user.is_superuser or request.user.is_staff:
        escolas = Escola.objects.all()
        visitas = (
            Visita.objects.select_related('escola')
            .only(
                'id', 'data_sugerida', 'periodo', 'status', 'responsavel',
                'numero_previsto_criancas', 'numero_previsto_adultos',
                'forma_pagamento', 'agencia', 'observacoes',
                'escola__nome'
            )
            .order_by('data_sugerida')
        )
        visitas_agendadas = visitas.filter(status__in=['CONFIRMADO', 'SOLICITADO']).count()
        visitas_concluidas = visitas.filter(status='REALIZADO').count()
        return render(request, 'core/home.html', {
            'escola': None,
            'escolas': escolas,
            'visitas': visitas,
            'visitas_agendadas': visitas_agendadas,
            'visitas_concluidas': visitas_concluidas,
            'is_admin': True,
        })

    try:
        escola = Escola.objects.get(email=request.user.email)
    except Escola.DoesNotExist:
        messages.info(request, "Nenhuma escola vinculada a este usuário. Cadastre sua escola.")
        return redirect('cadastro_escola')

    visitas = Visita.objects.filter(escola=escola).order_by('data_sugerida')
    visitas_agendadas = visitas.filter(status__in=['CONFIRMADO', 'SOLICITADO']).count()
    visitas_concluidas = visitas.filter(status='REALIZADO').count()

    return render(request, 'core/home.html', {
        'escola': escola,
        'visitas': visitas,
        'visitas_agendadas': visitas_agendadas,
        'visitas_concluidas': visitas_concluidas,
    })

@login_required
def cadastrar_visita(request):
    escola = None
    if request.user.is_superuser or request.user.is_staff:
        escola_id = request.GET.get('escola_id') or request.POST.get('escola_id')
        if escola_id:
            escola = get_object_or_404(Escola, id=escola_id)
        else:
            escola = Escola.objects.first()
            if not escola:
                messages.info(request, "Nenhuma escola cadastrada. Cadastre uma escola primeiro.")
                return redirect('cadastro_escola')
    else:
        try:
            escola = Escola.objects.get(email=request.user.email)
        except Escola.DoesNotExist:
            messages.info(request, "Nenhuma escola vinculada a este usuário. Cadastre sua escola.")
            return redirect('cadastro_escola')

    data_escolhida = request.GET.get('data')
    if not data_escolhida:
        data_escolhida = datetime.now().date().strftime('%Y-%m-%d')

    horarios = ['10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00']
    visitas_data = Visita.objects.filter(data_sugerida=data_escolhida)
    horarios_ocupados = set(visita.periodo for visita in visitas_data)
    horarios_lista = []
    for h in horarios:
        status = 'reservado' if h in horarios_ocupados else 'disponivel'
        horarios_lista.append({'hora': h, 'status': status})

    if request.method == 'POST':
        periodo = request.POST.get('periodo')
        data_sugerida = request.POST.get('data_sugerida')

        horario_obj = None
        if periodo:
            try:
                horario_obj = datetime.strptime(periodo, "%H:%M").time()
            except ValueError:
                horario_obj = None

        if periodo in horarios_ocupados:
            messages.error(request, "Esse horário já está reservado!")
        else:
            Visita.objects.create(
                escola=escola,
                data_sugerida=data_sugerida,
                periodo=periodo,
                horario=horario_obj,
                numero_previsto_criancas=request.POST.get('numero_previsto_criancas'),
                numero_previsto_adultos=request.POST.get('numero_previsto_adultos'),
                forma_pagamento=request.POST.get('forma_pagamento'),
                responsavel=request.POST.get('responsavel'),
                agencia=request.POST.get('agencia'),
                observacoes=request.POST.get('observacoes'),
            )
            messages.success(request, "Visita agendada com sucesso!")
            return redirect('acompanhamento_visitas')

    context = {
        'data_escolhida': data_escolhida,
        'horarios_lista': horarios_lista,
    }
    if request.user.is_superuser or request.user.is_staff:
        context['escolas'] = Escola.objects.all()
        context['selected_escola_id'] = getattr(escola, 'id', None)

    return render(request, 'core/cadastrar_visita.html', context)

def teste_email(request):
    send_mail(
        'Bem-vindo à Gestão de Visitas Escolares!',
        'Olá!\n\nSeu cadastro foi realizado com sucesso.\n\nObrigado por se cadastrar!',
        None,
        ['pokejhow2053@gmail.com'],
        fail_silently=False,
    )
    return HttpResponse('E-mail de teste enviado com sucesso!')

@staff_member_required
def admin_dashboard(request):
    visitas_recentes = (
        Visita.objects.select_related('escola')
        .only('id','data_sugerida','periodo','status','responsavel','escola__nome')
        .order_by('-id')[:10]
    )
    return render(request, 'core/admin_dashboard.html', {'visitas': visitas_recentes})

@login_required
def acompanhamento_visitas(request):
    try:
        escola = Escola.objects.get(email=request.user.email)
    except Escola.DoesNotExist:
        if request.user.is_superuser or request.user.is_staff:
            visitas = (
                Visita.objects.select_related('escola')
                .only('id','data_sugerida','periodo','status','responsavel','observacoes','escola__nome')
                .order_by('-id')
            )
            horarios = ['10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00']
            return render(request, 'core/admin_dashboard.html', {
                'visitas': visitas,
                'horarios': horarios,
            })
        messages.info(request, "Nenhuma escola vinculada a este usuário. Cadastre sua escola.")
        return redirect('cadastro_escola')

    visitas = (
        Visita.objects.filter(escola=escola)
        .select_related('escola')
        .only('id','data_sugerida','periodo','status','responsavel','observacoes','escola__nome')
        .order_by('-id')
    )
    horarios = ['10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00']
    return render(request, 'core/acompanhamento_visitas.html', {
        'visitas': visitas,
        'horarios': horarios,
    })

@staff_member_required
@require_POST
def atualizar_status_visita(request, visita_id):
    visita = get_object_or_404(Visita, id=visita_id)
    novo_status = request.POST.get('status')
    novo_feedback = request.POST.get('feedback', '')
    if novo_status in dict(Visita.STATUS_CHOICES):
        visita.status = novo_status
        visita.feedback = novo_feedback
        visita.save()
        messages.success(request, "Status e feedback atualizados com sucesso!")
    else:
        messages.error(request, "Status inválido.")
    # Optional redirect target (useful when updating from pages other than admin dashboard)
    nxt = request.POST.get('next')
    if nxt and isinstance(nxt, str) and nxt.startswith('/'):
        return redirect(nxt)
    return redirect('admin_dashboard')

@login_required
def detalhes_visita(request, visita_id):
    visita = get_object_or_404(Visita, id=visita_id)

    if not (request.user.is_superuser or request.user.is_staff):
        try:
            escola_user = Escola.objects.get(email=request.user.email)
        except Escola.DoesNotExist:
            return redirect('cadastro_escola')
        if visita.escola_id != escola_user.id:
            return redirect('home')

    pagamentos = getattr(visita, 'pagamento_set', None)
    if pagamentos is not None:
        pagamentos = visita.pagamento_set.all()

    context = {
        'visita': visita,
        'pagamentos': pagamentos,
    }
    return render(request, 'core/detalhes_visita.html', context)

@login_required
def editar_visita(request, id):
    visita = get_object_or_404(Visita, id=id)
    
    if request.method == 'POST':
        visita.data_sugerida = request.POST.get('data_sugerida')
        visita.periodo = request.POST.get('periodo')
        visita.numero_previsto_criancas = request.POST.get('numero_previsto_criancas')
        visita.numero_previsto_adultos = request.POST.get('numero_previsto_adultos')
        visita.forma_pagamento = request.POST.get('forma_pagamento')
        visita.responsavel = request.POST.get('responsavel')
        visita.agencia = request.POST.get('agencia')
        visita.observacoes = request.POST.get('observacoes')
        visita.save()
        messages.success(request, "Visita atualizada com sucesso!")
        return redirect('acompanhamento_visitas')

    return render(request, 'core/editar_visita.html', {'visita': visita})

@login_required
def cancelar_visita(request, id):
    visita = get_object_or_404(Visita, id=id)
    visita.status = 'CANCELADO'
    visita.save()
    messages.success(request, "Visita cancelada com sucesso!")
    return redirect('acompanhamento_visitas')

def duvidas(request):
    return render(request, 'core/duvidas.html')

