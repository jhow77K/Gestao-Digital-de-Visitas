from django.urls import path
from core import views
from .views import login_view, logout_view
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('adicionar_escola/', views.adicionar_escola, name='adicionar_escola'),
    path('adicionar_visita/', views.adicionar_visita, name='adicionar_visita'),
    path('adicionar_pagamento/', views.adicionar_pagamento, name='adicionar_pagamento'),
    path('adicionar_monitores/', views.adicionar_monitores, name='adicionar_monitores'),
    path('excluir_registro/<str:tabela>/<int:id_registro>/', views.excluir_registro, name='excluir_registro'),
    path('editar_registro/<str:tabela>/<int:id_registro>/', views.editar_registro, name='editar_registro'),
    path('visualizar_dados/', views.visualizar_dados, name='visualizar_dados'),
    path('adicionar_usuario/', views.adicionar_usuario, name='adicionar_usuario'),
    path('verificar_login/', views.verificar_login, name='verificar_login'),
    path('editar_pagamento/<int:pagamento_id>/', views.editar_pagamento, name='editar_pagamento'),
    path('excluir_pagamento/<int:pagamento_id>/', views.excluir_pagamento, name='excluir_pagamento'),
    path('editar_escola/<int:escola_id>/', views.editar_escola, name='editar_escola'),
    path('excluir_escola/<int:escola_id>/', views.excluir_escola, name='excluir_escola'),
    path('editar_visita/<int:visita_id>/', views.editar_visita, name='editar_visita'),
    path('excluir_visita/<int:visita_id>/', views.excluir_visita, name='excluir_visita'),
    path('editar_monitor/<int:monitor_id>/', views.editar_monitor, name='editar_monitor'),
    path('excluir_monitor/<int:monitor_id>/', views.excluir_monitor, name='excluir_monitor'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/adicionar/', views.adicionar_usuario, name='adicionar_usuario'),
    path('usuarios/editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/excluir/<int:usuario_id>/', views.excluir_usuario, name='excluir_usuario'),
    path('agendamentos_proximos/', views.agendamentos_proximos, name='agendamentos_proximos'),
    path('marcar_visita_feita/<int:visita_id>/', views.marcar_visita_feita, name='marcar_visita_feita'),
    path('marcar_pagamento_confirmado/<int:pagamento_id>/', views.marcar_pagamento_confirmado, name='marcar_pagamento_confirmado'),

]