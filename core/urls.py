from django.urls import path
from .views import (
    home,
    login_view,
    logout_view,
    cadastro_escola,
    cadastrar_visita,
    teste_email,
)
from django.views.generic import TemplateView

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('cadastro_escola/', cadastro_escola, name='cadastro_escola'),
    path('cadastrar-visita/', cadastrar_visita, name='cadastrar_visita'),
    path('teste-email/', teste_email, name='teste_email'),
    path('politica-cookies/', TemplateView.as_view(template_name='core/politica_cookies.html'), name='politica_cookies'), 
]