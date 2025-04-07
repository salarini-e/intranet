from django import forms
from .models import PlanejamentoAcao
from django_select2 import forms as s2forms

class ResponsavelWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "nome__icontains",
    ]

class PlanejamentoAcaoForm(forms.ModelForm):
    class Meta:
        model = PlanejamentoAcao
        fields = ['descricao', 'data', 'horario', 'local', 'responsavel', 'status']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': True}),
            'horario': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'step': '60', 'required': True}),
            'local': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'responsavel': ResponsavelWidget(attrs={'class': 'form-control', 'required': True}),
            'status': forms.Select(attrs={'class': 'form-control', 'required': True}),
        }
