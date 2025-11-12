from . import views
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro-escola/', views.cadastro_escola, name='cadastro_escola'),
    path('cadastrar-visita/', views.cadastrar_visita, name='cadastrar_visita'),
    path('teste-email/', views.teste_email, name='teste_email'),
    path('politica-cookies/', TemplateView.as_view(template_name='core/politica_cookies.html'), name='politica_cookies'), 
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('acompanhamento/', views.acompanhamento_visitas, name='acompanhamento_visitas'),
    path('atualizar-status/<int:visita_id>/', views.atualizar_status_visita, name='atualizar_status_visita'),
    path('detalhes-visita/<int:visita_id>/', views.detalhes_visita, name='detalhes_visita'),
    path('editar-visita/<int:id>/', views.editar_visita, name='editar_visita'),
    path('cancelar-visita/<int:id>/', views.cancelar_visita, name='cancelar_visita'),
    path('duvidas/', views.duvidas, name='duvidas'),
]