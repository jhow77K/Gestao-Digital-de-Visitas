from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Escola, Visita
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime, time, timedelta

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
    escola = Escola.objects.filter(email=request.user.email).first()
    visitas = Visita.objects.filter(escola=escola) if escola else []
    context = {
        'escola': escola,
        'visitas': visitas,
    }
    return render(request, 'core/home.html', context)

@login_required
def cadastrar_visita(request):
    escola = Escola.objects.get(email=request.user.email)
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
        # Novo: converte o horário para objeto time
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
                horario=horario_obj,  # <-- salva o horário no novo campo
                numero_previsto_criancas=request.POST.get('numero_previsto_criancas'),
                numero_previsto_adultos=request.POST.get('numero_previsto_adultos'),
                forma_pagamento=request.POST.get('forma_pagamento'),
                responsavel=request.POST.get('responsavel'),
                agencia=request.POST.get('agencia'),
                observacoes=request.POST.get('observacoes'),
            )
            messages.success(request, "Visita agendada com sucesso!")
            return redirect('acompanhamento_visitas')

    return render(request, 'core/cadastrar_visita.html', {
        'data_escolhida': data_escolhida,
        'horarios_lista': horarios_lista,
    })

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
    visitas_recentes = Visita.objects.order_by('-id')[:10]
    return render(request, 'core/admin_dashboard.html', {'visitas': visitas_recentes})

@login_required
def acompanhamento_visitas(request):
    escola = Escola.objects.get(email=request.user.email)
    visitas = Visita.objects.filter(escola=escola).order_by('-id')
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
    return redirect('admin_dashboard')

