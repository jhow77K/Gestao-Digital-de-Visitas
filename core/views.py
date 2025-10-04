from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Escola, Visita
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

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
    try:
        escola = Escola.objects.get(email=request.user.email)
    except Escola.DoesNotExist:
        messages.error(request, "Escola não encontrada para este usuário.")
        return redirect('login')

    if request.method == 'POST':
        data_sugerida = request.POST.get('data_sugerida')
        numero_previsto_criancas = request.POST.get('numero_previsto_criancas')
        numero_previsto_adultos = request.POST.get('numero_previsto_adultos')
        forma_pagamento = request.POST.get('forma_pagamento')
        periodo = request.POST.get('periodo')
        responsavel = request.POST.get('responsavel')
        agencia = request.POST.get('agencia')
        observacoes = request.POST.get('observacoes')

        Visita.objects.create(
            escola=escola,
            data_sugerida=data_sugerida,
            numero_previsto_criancas=numero_previsto_criancas,
            numero_previsto_adultos=numero_previsto_adultos,
            forma_pagamento=forma_pagamento,
            periodo=periodo,
            responsavel=responsavel,
            agencia=agencia,
            observacoes=observacoes
        )
        messages.success(request, "Visita agendada com sucesso!")
        return redirect('home')
    return render(request, 'core/cadastrar_visita.html')

def teste_email(request):
    send_mail(
        'Bem-vindo à Gestão de Visitas Escolares!',
        'Olá!\n\nSeu cadastro foi realizado com sucesso.\n\nObrigado por se cadastrar!',
        None,
        ['pokejhow2053@gmail.com'],
        fail_silently=False,
    )
    return HttpResponse('E-mail de teste enviado com sucesso!')
