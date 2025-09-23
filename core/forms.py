from django import forms
from .models import PreCadastroVisita

class PreCadastroVisitaForm(forms.ModelForm):
    data_sugerida = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = PreCadastroVisita
        fields = [
            'data_sugerida',
            'numero_previsto_criancas',
            'numero_previsto_adultos',
            'forma_pagamento',
            'observacoes',
        ]