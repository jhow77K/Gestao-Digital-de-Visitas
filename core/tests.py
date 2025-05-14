from django.test import TestCase
from .models import Escola, Visita, Pagamento, Monitor, Usuario

class EscolaModelTest(TestCase):
    def setUp(self):
        self.escola = Escola.objects.create(
            nome="Escola Teste",
            responsavel="Responsável Teste",
            endereco="Endereço Teste",
            bairro="Bairro Teste",
            telefone="123456789",
            email="teste@escola.com",
            cnpj="12.345.678/0001-90"
        )

    def test_escola_creation(self):
        self.assertEqual(self.escola.nome, "Escola Teste")
        self.assertEqual(self.escola.responsavel, "Responsável Teste")

class VisitaModelTest(TestCase):
    def setUp(self):
        self.escola = Escola.objects.create(
            nome="Escola Teste",
            responsavel="Responsável Teste",
            endereco="Endereço Teste",
            bairro="Bairro Teste",
            telefone="123456789",
            email="teste@escola.com",
            cnpj="12.345.678/0001-90"
        )
        self.visita = Visita.objects.create(
            escola=self.escola,
            data="2023-10-01",
            periodo="Manhã",
            clima="Ensolarado",
            serie_alunos="5º ano"
        )

    def test_visita_creation(self):
        self.assertEqual(self.visita.escola, self.escola)
        self.assertEqual(self.visita.clima, "Ensolarado")

class PagamentoModelTest(TestCase):
    def setUp(self):
        self.escola = Escola.objects.create(
            nome="Escola Teste",
            responsavel="Responsável Teste",
            endereco="Endereço Teste",
            bairro="Bairro Teste",
            telefone="123456789",
            email="teste@escola.com",
            cnpj="12.345.678/0001-90"
        )
        self.pagamento = Pagamento.objects.create(
            escola=self.escola,
            numero_criancas_pagantes=10,
            valor_por_crianca=20.0,
            numero_adultos_pagantes=5,
            valor_por_adulto=30.0,
            total=200.0,
            forma_pagamento="Dinheiro",
            nota_fiscal=True,
            recibo=True,
            agencia=1,
            comissao=10.0,
            numero_previsto_criancas=15,
            numero_adultos_cortesia=2
        )

    def test_pagamento_creation(self):
        self.assertEqual(self.pagamento.total, 200.0)
        self.assertEqual(self.pagamento.forma_pagamento, "Dinheiro")

class MonitorModelTest(TestCase):
    def setUp(self):
        self.escola = Escola.objects.create(
            nome="Escola Teste",
            responsavel="Responsável Teste",
            endereco="Endereço Teste",
            bairro="Bairro Teste",
            telefone="123456789",
            email="teste@escola.com",
            cnpj="12.345.678/0001-90"
        )
        self.visita = Visita.objects.create(
            escola=self.escola,
            data="2023-10-01",
            periodo="Manhã",
            clima="Ensolarado",
            serie_alunos="5º ano"
        )
        self.monitor = Monitor.objects.create(
            escola=self.escola,
            visita=self.visita,
            monitores_fazendinha="Monitor 1",
            monitores_free="Monitor 2",
            guia_fazendinha="Guia 1",
            guias_free="Guia 2",
            historico_passeio="Histórico Teste"
        )

    def test_monitor_creation(self):
        self.assertEqual(self.monitor.monitores_fazendinha, "Monitor 1")
        self.assertEqual(self.monitor.historico_passeio, "Histórico Teste")

class UsuarioModelTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(
            username="usuario_teste",
            senha_hash="hashed_password"
        )

    def test_usuario_creation(self):
        self.assertEqual(self.usuario.username, "usuario_teste")