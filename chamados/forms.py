from django import forms
from .models import *

class TipoChamadoForm(forms.ModelForm):
    class Meta:
        model = TipoChamado
        fields = ['nome', 'sigla', 'descricao', 'user_inclusao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'sigla': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control mb-3'}),
            'user_inclusao': forms.HiddenInput(),
        }

class AtendenteForm(forms.ModelForm):
    class Meta:
        model = Atendente
        fields = ['servidor', 'tipo', 'user_inclusao', 'ativo']
        widgets = {
            'servidor': forms.Select(attrs={'class': 'form-control mb-3'}),
            'tipo': forms.SelectMultiple(attrs={'class': 'form-control mb-3'}),
            'user_inclusao': forms.HiddenInput(),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CriarChamadoForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):                
        super(CriarChamadoForm, self).__init__(*args, **kwargs)

        if 'initial' in kwargs:
            if 'secretaria' in kwargs['initial']:
                self.fields['secretaria'].initial = kwargs['initial']['secretaria']


    secretaria = forms.ModelChoiceField(queryset=Secretaria.objects.all(), empty_label='Selecione a secretaria', widget=forms.Select(attrs={'class': 'form-select mb-3', 'onchange': 'getSetores(this.value)'}))
    class Meta:
        model = Chamado
        fields = ['secretaria', 'setor', 'telefone', 'requisitante', 'tipo', 'assunto'
                  , 'descricao', 'user_inclusao', 'anexo']
        widgets = {            
            'setor': forms.Select(attrs={'class': 'form-select mb-3'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'requisitante': forms.Select(attrs={'class': 'form-control mb-3'}),
            'tipo': forms.HiddenInput(),
            'assunto': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'prioridade': forms.Select(attrs={'class': 'form-control mb-3'}),
            'status': forms.Select(attrs={'class': 'form-control mb-3'}),            
            'descricao': forms.Textarea(attrs={'class': 'form-control mb-3'}),            
            'user_inclusao': forms.HiddenInput(),
            'anexo': forms.ClearableFileInput(attrs={'class': 'form-control mb-3'}),
        }

    
class MensagemForm(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = ['chamado', 'mensagem', 'anexo', 'user_inclusao']
        widgets = {
            'chamado': forms.HiddenInput(),
            'mensagem': forms.Textarea(attrs={'class': 'form-control mb-3'}),
            'anexo': forms.ClearableFileInput(attrs={'class': 'form-control mb-3'}),
            'user_inclusao': forms.HiddenInput(),
        }

class OSInternetForm(forms.ModelForm):
    class Meta:
        model = OSInternet
        fields = ['chamado', 'nofcip']
        widgets = {
            'chamado': forms.HiddenInput(),
            'nofcip': forms.TextInput(attrs={'class': 'form-control mb-3'}),            
        }

class OSImpressoraForm(forms.ModelForm):
    class Meta:
        model = OSImpressora
        fields = ['chamado', 'n_serie', 'contador']
        widgets = {
            'chamado': forms.HiddenInput(),            
            'n_serie': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'contador': forms.TextInput(attrs={'class': 'form-control mb-3'}),            
        }

class OSSistemasForm(forms.ModelForm):
    class Meta:
        model = OSSistemas
        fields = ['chamado', 'sistema']
        widgets = {
            'chamado': forms.HiddenInput(),
            'sistema': forms.TextInput(attrs={'class': 'form-control mb-3'}),            
        }
