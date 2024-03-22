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
