from django import forms
from .models import Equipamento

class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = ['descricao', 'numero_convenio']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_convenio': forms.TextInput(attrs={'class': 'form-control'}),
        }
