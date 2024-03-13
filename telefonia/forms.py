from django import forms
from .models import Ramal

class RamalForm(forms.ModelForm):
    class Meta:
        model = Ramal
        fields = ['secretaria', 'setor', 'referencia', 'numero', 'webex']
        labels = {
            'secretaria': 'Secretaria',
            'setor': 'Setor',
            'referencia': 'Referência', 
            'numero': 'Número',
            'webex': 'Webex'
        }