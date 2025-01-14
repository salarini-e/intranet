from django import forms
from .models import Projetos

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
        # Alterar o widget para exibir status como uma lista suspensa (dropdown)
        self.fields['status'].widget = forms.Select(choices=Projetos.STATUS_CHOICES)

        # Opcionalmente, você pode adicionar validação personalizada aqui, se necessário

