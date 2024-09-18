from django import forms
from .models import *
from autenticacao.functions import validate_cpf, clear_tel

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
        fields = ['cpf', 'nome', 'telefone', 'email', 'matricula', 'pdf_memorando', 'sistemas', 'observacao']
        widgets = {
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'matricula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'pdf_memorando': forms.FileInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'sistemas': forms.CheckboxSelectMultiple(),
            'observacao': forms.Textarea(attrs={'class': 'form-control mb-3', 'placeholder': '', 'rows': 4}),
        }

# # #############################################################################
class FormCadastroAulasProcessoDigital(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra apenas as turmas que estão ativas
        self.fields['turma_escolhida'].queryset = Opcao_Turmas.objects.filter(ativo=True)
    
    class Meta:
        model = Cadastro_Aulas_Processo_Digital
        fields = ['nome', 'matricula', 'secretaria', 'setor', 'telefone', 'turma_escolhida']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'matricula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'secretaria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'setor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'turma_escolhida': forms.Select(attrs={'class': 'form-select mb-3'})
        }


class CadastroAulasEmissoresForm(forms.ModelForm):
    class Meta:
        model = Cadastro_Aulas_Treinamento_Tributario_Emissores_Taxas
        fields = ['nome','cpf', 'matricula', 'secretaria', 'setor', 'telefone']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'onkeydown': 'mascara(this, icpf)'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control'}),
            'secretaria': forms.TextInput(attrs={'class': 'form-control'}),
            'setor': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'onkeydown': 'mascara(this, itel)' }),
        }

    def clean_cpf(self):
        cpf = validate_cpf(self.cleaned_data["cpf"])
        if Cadastro_Aulas_Treinamento_Tributario_Emissores_Taxas.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError("Este CPF já está cadastrado no sistema. Por favor, verifique.")
        return cpf
    
    def clean_telefone(self):
        telefone = clear_tel(self.cleaned_data["telefone"])
        return telefone

class CadastroAulasContadoresForm(forms.ModelForm):
    class Meta:
        model = Cadastro_Aulas_Treinamento_Tributario_Contadores
        fields = ['nome','cpf', 'matricula', 'secretaria', 'setor', 'telefone']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'onkeydown': 'mascara(this, icpf)'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control'}),
            'secretaria': forms.TextInput(attrs={'class': 'form-control'}),
            'setor': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'onkeydown': 'mascara(this, itel)'}),
        }

    def clean_cpf(self):
        cpf = validate_cpf(self.cleaned_data["cpf"])

        if Cadastro_Aulas_Treinamento_Tributario_Contadores.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError("Este CPF já está cadastrado no sistema. Por favor, verifique.")
        return cpf
    
    def clean_telefone(self):
        telefone = clear_tel(self.cleaned_data["telefone"])
        return telefone