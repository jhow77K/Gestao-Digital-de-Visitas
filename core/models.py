import re
from django.db import models
from django.utils.timezone import now
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from datetime import date

class Escola(models.Model):
    nome = models.CharField(max_length=255)
    cep = models.CharField(max_length=9)
    endereco = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)
    estado = models.CharField(max_length=2)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    cnpj = models.CharField(max_length=18)
    data_cadastro = models.DateTimeField(default=now) 

    def save(self, *args, **kwargs):
        cnpj_numerico = re.sub(r'\D', '', self.cnpj)
        if len(cnpj_numerico) == 14:
            self.cnpj = f"{cnpj_numerico[:2]}.{cnpj_numerico[2:5]}.{cnpj_numerico[5:8]}/{cnpj_numerico[8:12]}-{cnpj_numerico[12:]}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

class Visita(models.Model):
    STATUS_CHOICES = [
        ('SOLICITADO', 'Solicitado'),
        ('CONFIRMADO', 'Confirmado'),
        ('REALIZADO', 'Realizado'),
        ('CANCELADO', 'Cancelado'),
    ]
    HORARIO_CHOICES = [
        ('10:00', '10:00'),
        ('11:00', '11:00'),
        ('12:00', '12:00'),
        ('13:00', '13:00'),
        ('14:00', '14:00'),
        ('15:00', '15:00'),
        ('16:00', '16:00'),
        ('17:00', '17:00'),
    ]
    AGENCIA_CHOICES = [
        ('Sim', 'Sim'),
        ('Não', 'Não'),
    ]
    escola = models.ForeignKey(Escola, on_delete=models.PROTECT)
    data_sugerida = models.DateField()
    numero_previsto_criancas = models.IntegerField()
    numero_previsto_adultos = models.IntegerField()
    forma_pagamento = models.CharField(max_length=20, choices=[('dinheiro', 'Dinheiro'), ('pix', 'Pix')])
    periodo = models.CharField(max_length=5, choices=HORARIO_CHOICES)
    responsavel = models.CharField(max_length=255)
    agencia = models.CharField(max_length=3, choices=AGENCIA_CHOICES) 
    observacoes = models.TextField(blank=True, null=True)
    feita = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SOLICITADO')
    feedback = models.TextField(blank=True)
    horario = models.TimeField(null=True, blank=True)  # Novo campo para horário exato

    def __str__(self):
        return f"Visita à {self.escola.nome} em {self.data_sugerida} às {self.periodo}"

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

