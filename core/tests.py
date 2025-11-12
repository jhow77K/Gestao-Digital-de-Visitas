from django.test import TestCase
from .models import Escola, Visita, Pagamento, Monitor

class EscolaModelTest(TestCase):
    def setUp(self):
        self.escola = Escola.objects.create(
            nome="Escola Teste",
            cep="12345678",
            endereco="Rua Teste",
            bairro="Centro",
            cidade="Cidade",
            estado="SP",
            telefone="11999999999",
            email="teste@email.com",
            cnpj="12.345.678/0001-90"
        )

    def test_escola_creation(self):
        self.assertEqual(self.escola.nome, "Escola Teste")

class VisitaModelTest(TestCase):
    def setUp(self):
        self.escola = Escola.objects.create(
            nome="Escola Teste",
            cep="12345678",
            endereco="Rua Teste",
            bairro="Centro",
            cidade="Cidade",
            estado="SP",
            telefone="11999999999",
            email="teste@email.com",
            cnpj="12.345.678/0001-90"
        )

    def test_visita_creation(self):
        pass

class PagamentoModelTest(TestCase):
    def setUp(self):
        self.escola = Escola.objects.create(
            nome="Escola Teste",
            cep="12345678",
            endereco="Rua Teste",
            bairro="Centro",
            cidade="Cidade",
            estado="SP",
            telefone="11999999999",
            email="teste@email.com",
            cnpj="12.345.678/0001-90"
        )

    def test_pagamento_creation(self):
        pass

class MonitorModelTest(TestCase):
    def setUp(self):
        self.escola = Escola.objects.create(
            nome="Escola Teste",
            cep="12345678",
            endereco="Rua Teste",
            bairro="Centro",
            cidade="Cidade",
            estado="SP",
            telefone="11999999999",
            email="teste@email.com",
            cnpj="12.345.678/0001-90"
        )

    def test_monitor_creation(self):
        pass

