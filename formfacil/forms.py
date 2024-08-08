from django import forms
from .models import *

class FormIndicacaoComitePSPForm(forms.ModelForm):
    class Meta:
        model = FormIndicacaoComitePSP
        fields = ['secretaria', 'setor', 'nome', 'matricula','email', 'telefone', 'observação']
        widgets = {
            'secretaria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'setor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'matricula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'observação': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '', 'rows': 4}),
        }

    # def __init__(self, *args, **kwargs):
    #     super(FormIndicacaoComitePSPForm, self).__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control'
    #         field.widget.attrs['required'] = True
        
class FormCadastroWebex(forms.ModelForm):
    class Meta:
        model = CadastroWebex
        fields = ['secretaria', 'setor', 'nome', 'email', 'ramal']
        widgets ={
            'secretaria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'setor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'ramal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
        }

class FormSugestaoSemanaNacionalCET2024Form(forms.ModelForm):
    class Meta:
        model = FormSugestaoSemanaNacionalCET2024
        # fields = ['nome', 'telefone', 'email', 'sugestao']
        exclude = ['dt_inclusao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'sugestao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '', 'rows': 4}),
        }

class CadastroELForm(forms.ModelForm):
    class Meta:
        model = CadastroEL
        fields = ['cpf', 'nome', 'matricula', 'pdf_memorando', 'sistemas', 'observacao']
        widgets = {
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'matricula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'pdf_memorando': forms.FileInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'sistemas': forms.CheckboxSelectMultiple(),
            'observacao': forms.Textarea(attrs={'class': 'form-control mb-3', 'placeholder': '', 'rows': 4}),
        }