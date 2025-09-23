import re
from django.db import models
from django.utils.timezone import now
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from datetime import date

class Escola(models.Model):
    nome = models.CharField(max_length=255)
    responsavel = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    cnpj = models.CharField(max_length=18)
    data_cadastro = models.DateTimeField(default=now) 

    def save(self, *args, **kwargs):
        
        cnpj_numerico = re.sub(r'\D', '', self.cnpj)
        # Formatação no padrão 00.000.000/0000-00
        if len(cnpj_numerico) == 14:
            self.cnpj = f"{cnpj_numerico[:2]}.{cnpj_numerico[2:5]}.{cnpj_numerico[5:8]}/{cnpj_numerico[8:12]}-{cnpj_numerico[12:]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

class Visita(models.Model):
    escola = models.ForeignKey(Escola, on_delete=models.PROTECT)  
    data = models.DateField()
    periodo = models.CharField(max_length=20)  
    clima = models.CharField(max_length=50)
    serie_alunos = models.CharField(max_length=50)
    feita = models.BooleanField(default=False) 
    
    def __str__(self):
        return f"Visita à {self.escola.nome} em {self.data}"

class Pagamento(models.Model):
    escola = models.ForeignKey(Escola, on_delete=models.SET_NULL, null=True, blank=True)
    visita = models.ForeignKey(Visita, on_delete=models.SET_NULL, null=True, blank=True)
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
    confirmado = models.BooleanField(default=False)  

class Monitor(models.Model):
    escola = models.ForeignKey(Escola, on_delete=models.SET_NULL, null=True, blank=True)
    visita = models.ForeignKey(Visita, on_delete=models.SET_NULL, null=True, blank=True)
    monitores_fazendinha = models.TextField()
    monitores_free = models.TextField()
    guia_fazendinha = models.CharField(max_length=255)
    guias_free = models.TextField(blank=True, null=True)  
    historico_passeio = models.TextField(blank=True, null=True)  
    
class Usuario(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class PreCadastroEscola(models.Model):
    nome = models.CharField(max_length=120)
    email = models.EmailField()
    cnpj = models.CharField(max_length=18)
    telefone = models.CharField(max_length=16, default="") 
    senha = models.CharField(max_length=128)
    aprovado = models.BooleanField(default=False)
    data_cadastro = models.DateTimeField(auto_now_add=True)

class PreCadastroVisita(models.Model):
    escola = models.ForeignKey(PreCadastroEscola, on_delete=models.CASCADE, related_name='pre_cadastros_visita')
    data_sugerida = models.DateField()
    observacoes = models.TextField(blank=True)
    numero_previsto_criancas = models.IntegerField(default=0)  
    numero_previsto_adultos = models.IntegerField(default=0)
    FORMA_PAGAMENTO_CHOICES = [
        ('pix', 'Pix'),
        ('dinheiro', 'Dinheiro'),
    ]
    forma_pagamento = models.CharField(max_length=10, choices=FORMA_PAGAMENTO_CHOICES, default='pix')
    data_envio = models.DateTimeField(default=now)
    aprovado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.escola.nome} ({self.data_sugerida})"



