from django import forms
from django.forms import ModelForm, ValidationError, Form
from .models import *
from django.contrib.auth.forms import UserCreationForm


class Chamado_Form(ModelForm):
    class Meta:
        model = Chamado
        widgets = {
            'tipo': forms.Select(attrs={'readonly': True}),
        }
        exclude = ['tipo', 'dataAbertura', 'dataFechamento', 'prioridade', 'status', 'numero', 'atendente', 'requisitante', 'secretaria']
        labels = {
            'descricao': 'Descrição',
        }
        
# class SearchForm(Form):

#     REQUISITANTE_CHOICES = [(None,'-')]+[(obj.id, obj.nome) for obj in Servidor.objects.all()]
#     TIPO_CHOICES = [(None,'-')]+[(obj.id, obj.nome) for obj in Tipo.objects.all()]
#     PRIORIDADE_CHOICES = (
#         ('0', 'Baixa'),
#         ('1', 'Média'),
#         ('2', 'Alta'),
#         ('3', 'Todas')
#     )    
#     SETOR_CHOICES = [(None,'-')]+[(obj.id, obj.nome) for obj in Setor.objects.all()]
#     STATUS_CHOICES = (
#         ('0', 'Aberto'),
#         ('1', 'Pendente'),
#         ('2', 'Finalizado'),
#         ('3', 'Todos')
#     )
    
#     numero = forms.CharField(label='Número', max_length=10, required=False)
#     assunto = forms.CharField(label='Assunto', required=False)
#     requisitante = forms.ChoiceField(label='Requisitante', choices=REQUISITANTE_CHOICES, required=False)
#     tipo = forms.ChoiceField(label='Tipo', choices=TIPO_CHOICES, required=False)
#     prioridade = forms.ChoiceField(label='Prioridade', choices=PRIORIDADE_CHOICES, required=False)
#     setor = forms.ChoiceField(label='Setor', choices=SETOR_CHOICES, required=False)
#     status = forms.ChoiceField(label='Status', choices=STATUS_CHOICES, required=False)
      
#     dataInicio = forms.DateField(label='Data início', widget=forms.DateInput(attrs={'type': 'date'}), required=False)
#     dataFim = forms.DateField(label='Data fim', widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    

class editaChamadoForm(ModelForm):
    class Meta:
        model = Chamado
        fields = ['secretaria', 'setor', 'requisitante','prioridade', 'status', 'atendente', 'tipo', 'descricao', 'assunto']
        
    def __init__(self, *args, **kwargs):
        super(editaChamadoForm, self).__init__(*args, **kwargs)
        self.fields['atendente'].required = False
        self.fields['secretaria'].required = False
        self.fields['setor'].required = False
        self.fields['requisitante'].required = False
    

class ServidorForm(ModelForm):
    
    class Meta:
        model = Servidor
        fields = ['nome', 'contato', 'email', 'setor']
    
        labels = {
            'nome': 'Nome Completo',
            'contato': 'Telefone para contato (Completo, exemplo: +5522999991234)'
        }
        

class SetorForm(ModelForm):
    
    class Meta:
        model = Setor
        fields = ['secretaria', 'nome', 'cep', 'bairro', 'logradouro']

class ComentarioForm(ModelForm):
    
    class Meta:
        model = Comentario
        fields = ['texto', 'confidencial']
        

class OSInternet_Form(ModelForm):
    class Meta:
        model = OSInternet
        widgets = {
            'tipo': forms.Select(attrs={'readonly': True}),
        }
        exclude = ['dataAbertura', 'dataFechamento', 'prioridade', 'status', 'numero', 'atendente', 'requisitante', 'tipo', 'secretaria']
        labels = {
            'descricao': 'Descrição',
        }

class OSSistema_Form(ModelForm):
    class Meta:
        model = OSSistema
        widgets = {
            'tipo': forms.Select(attrs={'readonly': True}),
        }
        exclude = ['dataAbertura', 'dataFechamento', 'prioridade', 'status', 'numero', 'atendente', 'requisitante', 'tipo', 'secretaria']
        labels = {
            'descricao': 'Descrição',
        }

class OSImpressora_Form(ModelForm):
    class Meta:
        model = OSImpressora
        widgets = {
            'tipo': forms.Select(attrs={'readonly': True}),
        }
        exclude = ['dataAbertura', 'dataFechamento', 'prioridade', 'status', 'numero', 'atendente', 'requisitante', 'tipo', 'secretaria']
        labels = {
            'descricao': 'Descrição',
        }