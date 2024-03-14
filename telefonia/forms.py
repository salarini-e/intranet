from django import forms
from .models import Ramal

class RamalForm(forms.ModelForm):
    class Meta:
        model = Ramal
        fields = ['secretaria', 'setor', 'referencia', 'responsavel', 'numero']
        labels = {
            'secretaria': 'Secretaria',
            'setor': 'Setor',
            'referencia': 'Referência', 
            'responsavel': 'Responsável', 
            'numero': 'Número',            
        }        