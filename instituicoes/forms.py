#formulario para cadatrar secretaris e setores

from django import forms
from .models import Secretaria, Setor

class SecretariaForm(forms.ModelForm):
    class Meta:
        model = Secretaria
        fields = ['nome', 'sigla', 'telefone', 'email', 'endereco', 'descricao']

class SetorForm(forms.ModelForm):
    class Meta:
        model = Setor
        fields = ['nome', 'sigla', 'telefone', 'email', 'endereco', 'descricao', 'secretaria']
        widgets = {
            'secretaria': forms.Select(attrs={'class': 'form-control'}),
        }
