from django import forms
from .models import *
from django.utils import timezone
from django_select2 import forms as s2forms

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

class RequisitanteWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "nome__icontains",        
    ]

class SecretariaWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "nome__icontains",        
        "apelido__icontains",     
    ]

class SetorWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "nome__icontains",        
        "apelido__icontains",     
        "secretaria__nome__icontains",
        "secretaria__apelido__icontains",
    ]

class CriarSetorForm(forms.ModelForm):
    class Meta:
        model = Setor
        fields = ['secretaria', 'nome', 'apelido', 'sigla', 'cep', 'bairro', 'endereco', 'user_inclusao']
        widgets = {
            'secretaria': SecretariaWidget(attrs={'class': 'form-control mb-3'}),
            'nome': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'apelido': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'sigla': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'cep': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control mb-3'}),            
            'user_inclusao': forms.HiddenInput(),
        }
class CriarChamadoForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):                
        super(CriarChamadoForm, self).__init__(*args, **kwargs)

        if 'initial' in kwargs:
            if 'secretaria' in kwargs['initial']:
                self.fields['secretaria'].initial = kwargs['initial']['secretaria']


    secretaria = forms.ModelChoiceField(queryset=Secretaria.objects.all(), empty_label='Selecione a secretaria', widget=forms.Select(attrs={'class': 'form-select', 'onchange': 'getSetores(this.value)', 'required': 'required'}))
    # secretaria = SecretariaWidget(attrs={'class': 'form-control mb-3','onchange': 'getSetores(this.value)', 'required': 'required'})
    class Meta:
        model = Chamado
        fields = ['secretaria', 'setor', 'telefone', 'requisitante', 'tipo', 'assunto'
                  , 'descricao', 'periodo_preferencial', 'user_inclusao', 'anexo']
        widgets = {                        
            # 'secretaria': SecretariaWidget(attrs={'class': 'form-control mb-3','onchange': 'getSetores(this.value)', 'required': 'required'}),
            'setor': forms.Select(attrs={'class': 'form-select'}),
            'secretaria': SecretariaWidget(attrs={'class': 'form-control mb-3','onchange': 'getSetores(this.value)', 'required': 'required'}),
            # 'setor': SetorWidget(attrs={'class': 'form-control mb-3'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            # 'requisitante': forms.Select(attrs={'class': 'form-control'}),
            'requisitante': RequisitanteWidget(attrs={'class': 'form-control'}),
            'tipo': forms.HiddenInput(),
            'assunto': forms.TextInput(attrs={'class': 'form-control'}),
            'prioridade': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),            
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),  
            'periodo_preferencial': forms.CheckboxSelectMultiple(),
            'user_inclusao': forms.HiddenInput(),
            'anexo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'secretaria': 'Para qual secretaria é o chamado?',
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

class OSTelefoniaForm(forms.ModelForm):
    class Meta:
        model = OSTelefonia
        fields = ['chamado', 'ramal']
        widgets = {
            'chamado': forms.HiddenInput(),
            'ramal': forms.TextInput(attrs={'class': 'form-control mb-3'}),            
        }

class ServidorForm(forms.ModelForm):    
    class Meta:
        model = Servidor
        fields = [ 'setor', 'nome', 'cpf', 'dt_nascimento', 'matricula', 'telefone', 'email', 'ativo', 'user_inclusao']        
        widgets = {            
            'nome': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control mb-3', 'onkeydown': 'mascara(this, icpf)'}),
            'dt_nascimento': forms.DateInput(attrs={'class': 'form-control mb-3'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control mb-3', 'onkeydown':'mascara(this, itel)'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mb-3'}),
            'setor': SetorWidget(attrs={'class': 'form-control mb-3'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'mb-3'}),
            
            'user_inclusao': forms.HiddenInput()
        }
    
    def create_user(self):
        user = User.objects.create_user(self.cleaned_data['matricula'], self.cleaned_data['email'], self.cleaned_data['cpf'])
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
            raise forms.ValidationError(('O CPF deve conter 11 dígitos'), code='invalid1')
        if cpf in ["00000000000", "11111111111", "22222222222", "33333333333", "44444444444", "55555555555", "66666666666", "77777777777", "88888888888", "99999999999"]:
            raise forms.ValidationError(('CPF inválido'), code='invalid2')

        sum = 0
        weight = 10
        for i in range(9):
            sum += int(cpf[i]) * weight
            weight -= 1
        check_digit = 11 - (sum % 11)
        if check_digit > 9:
            check_digit = 0
        if check_digit != int(cpf[9]):
            raise forms.ValidationError(('CPF inválido'), code='invalid2')
        sum = 0
        weight = 11
        for i in range(10):
            sum += int(cpf[i]) * weight
            weight -= 1
        check_digit = 11 - (sum % 11)
        if check_digit > 9:
            check_digit = 0
        if check_digit != int(cpf[10]):
            raise forms.ValidationError(('CPF inválido'), code='invalid2')
        
        if Servidor.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError(('CPF já cadastrado'), code='invalid2')
        return cpf
    
class Form_Agendar_Atendimento(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = ('dt_agendamento',)
        widgets = {
            'dt_agendamento': forms.DateInput(attrs={'class': 'form-control mb-3', 'type': 'date'}),
        }
    
    def clean_dt_agendamento(self):
        dt_agendamento = self.cleaned_data.get('dt_agendamento')
        dt_agendamento_com_hora = timezone.make_aware(
            timezone.datetime.combine(dt_agendamento, timezone.now().time())
        )

        if dt_agendamento_com_hora < timezone.now():
            raise forms.ValidationError("A data de agendamento não pode ser no passado.")

        return dt_agendamento
    
class Form_Motivo_Pausa(forms.ModelForm):
    class Meta:
        model = Pausas_Execucao_do_Chamado
        fields = ('motivo',)
        widgets = {
            'motivo': forms.Textarea(attrs={'class': 'form-control mb-3'}),
        }
    
    def clean_motivo(self):
        motivo = self.cleaned_data.get('motivo')
        if motivo == '':
            raise forms.ValidationError("O motivo não pode ser vazio.")
        return motivo