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
        widgets= {
            'secretaria': forms.Select(attrs={'class': 'form-select mb-3', 'onchange': 'callSetor(this)'}),
            'setor': forms.Select(attrs={'class': 'form-select mb-3'}),
            'referencia': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'responsavel': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'numero': forms.TextInput(attrs={'class': 'form-control mb-3'}),
        }