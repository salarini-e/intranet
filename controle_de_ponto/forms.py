from django import forms
from instituicoes.models import Servidor, Setor
from django.utils import timezone
from autenticacao.functions import validate_cpf, clear_tel
from django_select2 import forms as s2forms

class ServidorWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "matricula__icontains",   
        "nome__icontains",        
    ]

# class SetorWidget(s2forms.ModelSelect2Widget):
#     search_fields = [
#         "nome__icontains",        
#     ]

class SearchServidorForm(forms.Form):
    
    servidor = forms.ModelChoiceField(
        queryset=Servidor.objects.all(),
        required=True,
        label="Servidor",
        widget=ServidorWidget(attrs={
            "class": "form-select",
            "data-placeholder": "Digite a matrícula ou nome do servidor"
        })
    )
    setor = forms.ModelChoiceField(
            queryset=Setor.objects.none(),
            required=False,
            label="Setor",
            widget=forms.Select(attrs={
                "class": "form-control",
                "data-placeholder": "Escolha o setor que você deseja alocar o servidor"
            })
        )

    def __init__(self, *args, **kwargs):
        responsavel = kwargs.pop('responsavel', None)
        super(SearchServidorForm, self).__init__(*args, **kwargs)
        
        if responsavel:
            self.fields['setor'].queryset = Setor.objects.filter(secretaria=responsavel.secretaria)
        else:
            self.fields['setor'].queryset = Setor.objects.none()