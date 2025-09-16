from django import forms
from .models import PreCadastroVisita

class PreCadastroVisitaForm(forms.ModelForm):
    class Meta:
        model = PreCadastroVisita
        fields = ['nome_escola', 'email', 'telefone', 'cnpj', 'data_sugerida', 'observacoes']