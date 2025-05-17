import re
from django.db import models
from django.utils.timezone import now
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

class Escola(models.Model):
    nome = models.CharField(max_length=255)
    responsavel = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    cnpj = models.CharField(max_length=18)
    data_cadastro = models.DateTimeField(default=now)  # Define um valor padrão válido

    def save(self, *args, **kwargs):
        # Remove qualquer caractere que não seja número
        cnpj_numerico = re.sub(r'\D', '', self.cnpj)
        # Formata o CNPJ no padrão 00.000.000/0000-00
        if len(cnpj_numerico) == 14:
            self.cnpj = f"{cnpj_numerico[:2]}.{cnpj_numerico[2:5]}.{cnpj_numerico[5:8]}/{cnpj_numerico[8:12]}-{cnpj_numerico[12:]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

class Visita(models.Model):
    escola = models.ForeignKey(Escola, on_delete=models.PROTECT)  # Protege a exclusão
    data = models.DateField()
    periodo = models.CharField(max_length=20)  # Manhã, Tarde ou Integral
    clima = models.CharField(max_length=50)
    serie_alunos = models.CharField(max_length=50)
    feita = models.BooleanField(default=False)  # Novo campo

    def __str__(self):
        return f"Visita à {self.escola.nome} em {self.data}"

class Pagamento(models.Model):
    escola = models.ForeignKey(Escola, on_delete=models.SET_NULL, null=True, blank=True)
    visita = models.ForeignKey(Visita, on_delete=models.SET_NULL, null=True, blank=True)
    visita = models.ForeignKey(Visita, on_delete=models.CASCADE)
    numero_criancas_pagantes = models.IntegerField()
    valor_por_crianca = models.DecimalField(max_digits=10, decimal_places=2)
    numero_adultos_pagantes = models.IntegerField()
    valor_por_adulto = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    forma_pagamento = models.CharField(max_length=50)
    nota_fiscal = models.BooleanField(default=False)
    recibo = models.BooleanField(default=False)
    agencia = models.BooleanField(default=False)
    comissao = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    numero_previsto_criancas = models.IntegerField()
    numero_adultos_cortesia = models.IntegerField()
    confirmado = models.BooleanField(default=False)  # Novo campo

class Monitor(models.Model):
    escola = models.ForeignKey(Escola, on_delete=models.SET_NULL, null=True, blank=True)
    visita = models.ForeignKey(Visita, on_delete=models.SET_NULL, null=True, blank=True)
    monitores_fazendinha = models.TextField()
    monitores_free = models.TextField()
    guia_fazendinha = models.CharField(max_length=255)
    guias_free = models.TextField(blank=True, null=True)  # Novo campo
    historico_passeio = models.TextField(blank=True, null=True)  # Novo campo
    
class Usuario(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

# Exemplo para exclusão
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

