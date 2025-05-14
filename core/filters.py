import django_filters
from .models import Escola

class EscolaFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains', label="Nome")
    bairro = django_filters.CharFilter(lookup_expr='icontains', label="Bairro")
    cnpj = django_filters.CharFilter(lookup_expr='icontains', label="CNPJ")

    class Meta:
        model = Escola
        fields = ['nome', 'bairro', 'cnpj']