from django import forms
from .models import Projetos, Demandas

class ProjetosForm(forms.ModelForm):
    class Meta:
        model = Projetos
        fields = ['status', 'nome', 'descricao', 'data_inicio', 'data_fim', 'user_inclusao']
        widgets = {
            'nome': forms.TextInput(attrs={'size': 50, 'class': 'form-control mb-3'}),            
            'data_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control mb-3'}),
            'data_fim': forms.DateInput(attrs={'type': 'date', 'class': 'form-control mb-3'}),
            'descricao': forms.Textarea(attrs={'rows': 4, 'cols': 50, 'class': 'form-control mb-3'}),
            'user_inclusao': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super(ProjetosForm, self).__init__(*args, **kwargs)
        self.fields['status'].widget = forms.Select(choices=Projetos.STATUS_CHOICES)

class DemandasForm(forms.ModelForm):
    class Meta:
        model = Demandas
        fields = ['nome', 'descricao', 'prioridade', 'data_prevista_execucao', 'rotina', 'ordem_dia']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'descricao': forms.Textarea(attrs={'rows': 3, 'class': 'form-control mb-3'}),
            'prioridade': forms.Select(attrs={'class': 'form-select mb-3'}),
            'data_prevista_execucao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control mb-3'}),
            'rotina': forms.CheckboxInput(attrs={'class': 'form-check-input mb-3'}),
            'ordem_dia': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
        }

