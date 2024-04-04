from typing import Any
from django import forms
from .models import Secretaria, Setor, Servidor
from django.contrib.auth.models import User
from django.forms import ValidationError

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
        fields = ['nome', 'apelido', 'sigla', 'cep', 'bairro', 'endereco', 'secretaria', 'user_inclusao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'apelido': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'sigla': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'cep': forms.TextInput(attrs={'class': 'form-control mb-3', 'onkeydown': 'icep(this)','onblur':'getCEP(this)'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control mb-3', 'onchange': 'getCEP(this)'}),
            'secretaria': forms.HiddenInput(),
            'user_inclusao': forms.HiddenInput()
        }

class ServidorForm(forms.ModelForm):
    username = forms.CharField(label='Nome de usuário', widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
    class Meta:
        model = Servidor
        fields = ['username', 'nome', 'cpf', 'dt_nascimento', 'matricula', 'telefone', 'email', 'setor', 'ativo', 'user_inclusao']        
        widgets = {            
            'nome': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control mb-3', 'onkeydown': 'mascara(this, icpf)'}),
            'dt_nascimento': forms.DateInput(attrs={'class': 'form-control mb-3'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control mb-3', 'onkeydown':'mascara(this, itel)'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mb-3'}),
            'setor': forms.HiddenInput(),
            'ativo': forms.CheckboxInput(attrs={'class': 'mb-3'}),
            
            'user_inclusao': forms.HiddenInput()
        }
    
    def create_user(self):
        user = User.objects.create_user(self.cleaned_data['username'], self.cleaned_data['email'], self.cleaned_data['cpf'])
        user.save()
        return user
    
    def clean_cpf(self):
        cpf = self.validate_cpf(self.cleaned_data["cpf"])
        return cpf
    
    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']
        telefone = telefone.replace('(', '')
        telefone = telefone.replace(')', '')
        telefone = telefone.replace(' ', '')
        telefone = telefone.replace('-', '')
        return telefone
    
    def validate_cpf(self, cpf):
        """
        Function that validates a CPF.
        """
        cpf = cpf.replace('.', '')
        cpf = cpf.replace('-', '')
        if len(cpf) != 11:
            raise ValidationError(('O CPF deve conter 11 dígitos'), code='invalid1')
        if cpf in ["00000000000", "11111111111", "22222222222", "33333333333", "44444444444", "55555555555", "66666666666", "77777777777", "88888888888", "99999999999"]:
            raise ValidationError(('CPF inválido'), code='invalid2')

        sum = 0
        weight = 10
        for i in range(9):
            sum += int(cpf[i]) * weight
            weight -= 1
        check_digit = 11 - (sum % 11)
        if check_digit > 9:
            check_digit = 0
        if check_digit != int(cpf[9]):
            raise ValidationError(('CPF inválido'), code='invalid2')
        sum = 0
        weight = 11
        for i in range(10):
            sum += int(cpf[i]) * weight
            weight -= 1
        check_digit = 11 - (sum % 11)
        if check_digit > 9:
            check_digit = 0
        if check_digit != int(cpf[10]):
            raise ValidationError(('CPF inválido'), code='invalid2')
        
        if Servidor.objects.filter(cpf=cpf).exists():
            raise ValidationError(('CPF já cadastrado'), code='invalid2')
        return cpf
    
class ServidorForm2(forms.ModelForm):
    
    secretaria = forms.CharField(label='Secretaria', widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
    outro = forms.CharField(label='Outro', widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'required': False}), required=False)

    class Meta:
        model = Servidor
        fields = ['nome', 'cpf', 'dt_nascimento', 'matricula', 'telefone', 'email', 'ativo', 'user_inclusao']        
        widgets = {            
            'nome': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control mb-3', 'onkeydown': 'mascara(this, icpf)'}),
            'dt_nascimento': forms.DateInput(attrs={'class': 'form-control mb-3'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control mb-3', 'onkeydown':'mascara(this, itel)'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mb-3'}),
            # 'setor': forms.HiddenInput(),
            'ativo': forms.CheckboxInput(attrs={'class': 'mb-3'}),
            
            'user_inclusao': forms.HiddenInput()
        }
    
    def create_user(self):
        user = User.objects.create_user(self.cleaned_data['matricula'], self.cleaned_data['email'], self.cleaned_data['cpf'])
        user.save()
        return user
    def get_setor(self, request):
        
        if request.POST['setor'] == 0:
            try:
                setor=Setor.objects.create(nome=self.cleaned_data['outro'],
                                 apelido='Sem setor', 
                                 sigla='SS', 
                                 cep='00000-000', 
                                 bairro='Sem bairro', 
                                 endereco='Sem endereço', 
                                 secretaria=Secretaria.objects.get(id=request.POST['secretaria']), 
                                 )
            except:
                raise ValidationError(('Erro ao criar setor'), code='invalid2')
            return setor
        setor = Setor.objects.get(id=request.POST['setor'])
        return setor
        
    def clean_cpf(self):
        cpf = self.validate_cpf(self.cleaned_data["cpf"])
        return cpf
    
    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']
        telefone = telefone.replace('(', '')
        telefone = telefone.replace(')', '')
        telefone = telefone.replace(' ', '')
        telefone = telefone.replace('-', '')
        return telefone
    
    def validate_cpf(self, cpf):
        """
        Function that validates a CPF.
        """
        cpf = cpf.replace('.', '')
        cpf = cpf.replace('-', '')
        if len(cpf) != 11:
            raise ValidationError(('O CPF deve conter 11 dígitos'), code='invalid1')
        if cpf in ["00000000000", "11111111111", "22222222222", "33333333333", "44444444444", "55555555555", "66666666666", "77777777777", "88888888888", "99999999999"]:
            raise ValidationError(('CPF inválido'), code='invalid2')

        sum = 0
        weight = 10
        for i in range(9):
            sum += int(cpf[i]) * weight
            weight -= 1
        check_digit = 11 - (sum % 11)
        if check_digit > 9:
            check_digit = 0
        if check_digit != int(cpf[9]):
            raise ValidationError(('CPF inválido'), code='invalid2')
        sum = 0
        weight = 11
        for i in range(10):
            sum += int(cpf[i]) * weight
            weight -= 1
        check_digit = 11 - (sum % 11)
        if check_digit > 9:
            check_digit = 0
        if check_digit != int(cpf[10]):
            raise ValidationError(('CPF inválido'), code='invalid2')
        
        if Servidor.objects.filter(cpf=cpf).exists():
            raise ValidationError(('CPF já cadastrado'), code='invalid2')
        return cpf

class ServidorEditForm(forms.ModelForm):
    class Meta:
        model = Servidor
        fields = ['nome', 'cpf', 'dt_nascimento', 'matricula', 'telefone', 'email', 'setor']
        widgets = {
            'setor': forms.Select(attrs={'class': 'form-control'}),
        }