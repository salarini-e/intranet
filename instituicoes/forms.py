from django import forms
from .models import Secretaria, Setor, Servidor

class SecretariaForm(forms.ModelForm):
    class Meta:
        model = Secretaria
        fields = ['nome', 'apelido','sigla', 'user_inclusao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'apelido': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'sigla': forms.TextInput(attrs={'class': 'form-control mb-3'}),

            'user_inclusao': forms.HiddenInput()
        }

class SetorForm(forms.ModelForm):
    class Meta:
        model = Setor
        fields = ['nome', 'apelido', 'sigla', 'cep', 'bairro', 'endereco', 'user_inclusao']
        widgets = {
            'secretaria': forms.Select(attrs={'class': 'form-control'}),
            'user_inclusao': forms.HiddenInput()
        }

class ServidorForm(forms.ModelForm):
    class Meta:
        model = Servidor
        fields = ['nome', 'cpf', 'dt_nascimento', 'matricula', 'telefone', 'email', 'setor', 'ativo', 'user_inclusao']        
        widgets = {
            'setor': forms.Select(attrs={'class': 'form-control'}),
            'user_inclusao': forms.HiddenInput()
        }

class ServidorEditForm(forms.ModelForm):
    class Meta:
        model = Servidor
        fields = ['nome', 'cpf', 'dt_nascimento', 'matricula', 'telefone', 'email', 'setor']
        widgets = {
            'setor': forms.Select(attrs={'class': 'form-control'}),
        }