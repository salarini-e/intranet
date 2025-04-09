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
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'matricula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'pdf_memorando': forms.FileInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'sistemas': forms.CheckboxSelectMultiple(),
            'observacao': forms.Textarea(attrs={'class': 'form-control mb-3', 'placeholder': '', 'rows': 4}),
        }

# # #############################################################################
class FormCadastroAulasProcessoDigital(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        cpf = validate_cpf(cpf = self.cleaned_data["cpf"].strip())
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
        cpf = self.cleaned_data["cpf"].replace('.', '').replace('-', '').strip()
        cpf = validate_cpf(cpf)

        if Cadastro_Aulas_Treinamento_Tributario_Contadores.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError("Este CPF já está cadastrado no sistema. Por favor, verifique.")
        return cpf
    
    def clean_telefone(self):
        telefone = clear_tel(self.cleaned_data["telefone"])
        return telefone
    
class CadastroDecretos2024Form(forms.ModelForm):
    
    class Meta:
        model = Inscricao_Decretos_Portaria_E_Atos_Do_Prefeito
        fields = ['nome','cpf', 'matricula', 'secretaria', 'setor', 'telefone', 'horarios']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'onkeydown': 'mascara(this, icpf)'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control'}),
            'secretaria': forms.TextInput(attrs={'class': 'form-control'}),
            'setor': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'onkeydown': 'mascara(this, itel)'}),
            'horarios': forms.Select(attrs={'class': 'form-select mb-3'}),
        }   

    def clean_cpf(self):
        cpf = self.cleaned_data["cpf"].replace('.', '').replace('-', '').strip()
        cpf = validate_cpf(cpf)
        if Inscricao_Decretos_Portaria_E_Atos_Do_Prefeito.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError("Este CPF já está cadastrado no sistema. Por favor, verifique.")
        return cpf
    
    def clean_telefone(self):
        telefone = clear_tel(self.cleaned_data["telefone"])
        return telefone

class CadastroDeAlmoxarifadoForm(forms.ModelForm):
    class Meta:
        model = Cadastro_de_Almoxarifado
        fields = ['nome_requisitante', 'matricula', 'cpf', 'secretaria', 'autorizador', 'responsavel_material']
        widgets = {
            'nome_requisitante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'matricula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'secretaria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'autorizador': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'responsavel_material': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
        }

class AvaliacaoSistemaELForm(forms.ModelForm):
    class Meta:
        model = AvaliacaoSistemaEL
        fields = ['sistema', 'usuario_nome', 'usuario_matricula', 'satisfacao', 'houve_lentidao', 'sugestao', 'usuario_inclusao']
        widgets = {
            'sistema': forms.HiddenInput(),  # Hidden input for the system name
            'usuario_nome': forms.TextInput(attrs={'class': 'form-control'}),
            'usuario_matricula': forms.TextInput(attrs={'class': 'form-control'}),
            'satisfacao': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'houve_lentidao': forms.RadioSelect(choices=[(1, 'Sim'), (0, 'Não')]),
            'sugestao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class SolicitacaoEmailInstitucionalForm(forms.ModelForm):
    class Meta:
        model = SolicitacaoEmailInstitucional
        fields = ['nome', 'matricula', 'cpf', 'telefone', 'secretaria', 'email_institucional']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),            
            'matricula': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'onkeydown': 'mascara(this, icpf)'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'onkeydown': 'mascara(this, itel)'}),
            'secretaria': forms.TextInput(attrs={'class': 'form-control'}),                       
            'email_institucional': forms.EmailInput(attrs={'class': 'form-control'}),            
        }
    def clean_cpf(self):
        cpf = self.cleaned_data["cpf"].replace('.', '').replace('-', '').strip()
        cpf = validate_cpf(cpf)
        if SolicitacaoEmailInstitucional.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError("Este CPF já está cadastrado no sistema. Por favor, verifique.")
        return cpf
