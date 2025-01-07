from django import forms
from .models import *
from django.utils import timezone
from autenticacao.functions import validate_cpf, clear_tel
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
    secretaria = forms.ModelChoiceField(
        queryset=Secretaria.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control mb-3'})
    )
    
    class Meta:
        model = Setor
        fields = ['secretaria', 'nome', 'apelido', 'sigla', 'cep', 'bairro', 'endereco', 'user_inclusao']
        widgets = {
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
        self.user = kwargs.pop('user', None) 
        super(CriarChamadoForm, self).__init__(*args, **kwargs)
        
        if self.user and (Atendente.objects.filter(servidor__user=self.user, ativo=True, nivel__in = ['0','2']).exists( ) or hasattr(self.user, 'atendente')):
            self.fields['prioridade'] = forms.ChoiceField(
                choices=Chamado.PRIORIDADE_CHOICES,
                widget=forms.Select(attrs={'class': 'form-select'}),
                label='Prioridade') 
            
            
            self.fields['requisitante'] = forms.ModelChoiceField(
                queryset=Servidor.objects.all(),
                widget=RequisitanteWidget(attrs={'class': 'form-select', 'required': 'required', 'onchange':'get_data_servidor(this)'}),
                label='Nome do Servidor'
            )

            self.fields['profissional_designado'] = forms.ModelChoiceField(
                queryset=Atendente.objects.filter(ativo=True),
                widget=forms.Select(attrs={'class': 'form-select'}),
                label='Profissional Designado'
            )

        else:
            try:
                servidor = Servidor.objects.get(user=self.user)
                self.fields['requisitante'] = forms.ModelChoiceField(
                    queryset=Servidor.objects.filter(user=self.user),
                    widget=forms.Select(attrs={'class': 'form-control mb-3'}),
                    label='Nome do Servidor',                    
                )
                # Define o valor inicial para o requisitante
                self.fields['requisitante'].initial = servidor.id
            except Servidor.DoesNotExist:
                self.requisitante = None
            if 'initial' in kwargs:
                if 'secretaria' in kwargs['initial']:
                    self.fields['secretaria'].initial = kwargs['initial']['secretaria']

    secretaria = forms.ModelChoiceField(
        queryset=Secretaria.objects.all(),
        empty_label='Selecione a secretaria',
        widget=SecretariaWidget(attrs={'class': 'form-select', 'onchange': 'getSetores(this.value)', 'required': 'required'})
    )

    class Meta:
        model = Chamado
        fields = [
            'requisitante', 'assunto', 'secretaria', 
            'endereco', 'telefone', 'tipo', 'descricao', 
            'user_inclusao', 'anexo'
        ]
        widgets = {                                    
            # 'setor': forms.Select(attrs={'class': 'form-select'}),
            'secretaria': SecretariaWidget(attrs={'class': 'form-control mb-3', 'onchange': 'getSetores(this.value)', 'required': 'required'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'onkeydown': 'mascara(this, itel)'}),
            'tipo': forms.HiddenInput(),
            'assunto': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'prioridade': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),            
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),  
            'user_inclusao': forms.HiddenInput(),
            'anexo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'secretaria': 'Para qual secretaria é o chamado?',
        }
    
    def clean_telefone(self):
        telefone = clear_tel(self.cleaned_data["telefone"])
        return telefone

    def save(self, commit=True):
        chamado = super().save(commit=False)
        chamado.telefone = clear_tel(self.cleaned_data.get("telefone", ""))
        
        if self.user and not self.user.is_superuser:
            chamado.prioridade = '-'
        elif chamado.prioridade == '':
            chamado.prioridade = '-'

        if commit:
            chamado.save()
        return chamado
    
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
        # fields = ['chamado', 'nofcip']
        fields = ['chamado']
        widgets = {
            'chamado': forms.HiddenInput(),
            # 'nofcip': forms.TextInput(attrs={'class': 'form-control mb-3'}),            
        }

class OSImpressoraForm(forms.ModelForm):
    class Meta:
        model = OSImpressora
        # fields = ['chamado', 'n_serie', 'contador']
        fields = ['chamado']
        widgets = {
            'chamado': forms.HiddenInput(),            
            # 'n_serie': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            # 'contador': forms.TextInput(attrs={'class': 'form-control mb-3'}),            
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
    setor = forms.ModelChoiceField(
        queryset=Setor.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control mb-3'})
    )
    
    class Meta:
        model = Servidor
        fields = ['setor', 'nome', 'cpf', 'dt_nascimento', 'matricula', 'telefone', 'email', 'ativo', 'user_inclusao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control mb-3', 'onkeydown': 'mascara(this, icpf)'}),
            'dt_nascimento': forms.DateInput(attrs={'class': 'form-control mb-3'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control mb-3', 'onkeydown': 'mascara(this, itel)'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mb-3'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'mb-3'}),
            'user_inclusao': forms.HiddenInput(),
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
        telefone = telefone.replace('(', '').replace(')', '').replace(' ', '').replace('-', '')
        return telefone

    def validate_cpf(self, cpf):
        cpf = cpf.replace('.', '').replace('-', '')
        if len(cpf) != 11:
            raise forms.ValidationError('O CPF deve conter 11 dígitos', code='invalid1')
        if cpf in ["00000000000", "11111111111", "22222222222", "33333333333", "44444444444", "55555555555", "66666666666", "77777777777", "88888888888", "99999999999"]:
            raise forms.ValidationError('CPF inválido', code='invalid2')

        sum = 0
        weight = 10
        for i in range(9):
            sum += int(cpf[i]) * weight
            weight -= 1
        check_digit = 11 - (sum % 11)
        if check_digit > 9:
            check_digit = 0
        if check_digit != int(cpf[9]):
            raise forms.ValidationError('CPF inválido', code='invalid2')
        
        sum = 0
        weight = 11
        for i in range(10):
            sum += int(cpf[i]) * weight
            weight -= 1
        check_digit = 11 - (sum % 11)
        if check_digit > 9:
            check_digit = 0
        if check_digit != int(cpf[10]):
            raise forms.ValidationError('CPF inválido', code='invalid2')
        
        if Servidor.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError('CPF já cadastrado', code='invalid2')
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
    

class FormDetalhesDoChamado(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormDetalhesDoChamado, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            chamado = kwargs['instance']
            self.fields['subtipo'].queryset = SubTipoChamado.objects.filter(tipo=chamado.tipo)              
    class Meta:
        model = Chamado
        fields = ['dt_execucao', 'subtipo', 'relatorio']
        widgets = {
            'dt_execucao': forms.DateInput(attrs={'class': 'form-control mb-3', 'type': 'date'}),
            'subtipo': forms.Select(attrs={'class': 'form-control mb-3'}),
            'relatorio': forms.Textarea(attrs={'class': 'form-control mb-3', 'style': 'height: 150px;'}),
        }

class FormEditarChamado(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = [
                  'tipo',
                  'secretaria', 
                  'telefone', 
                  'endereco', 
                  'assunto',
                  'descricao',
                  ]
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control mb-3'}),
            'secretaria': forms.Select(attrs={'class': 'form-control mb-3'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'assunto': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control mb-3', 'style': 'height: 150px;'}),
        }
    
    def clean_dt_agendamento(self):
        dt_agendamento = self.cleaned_data.get('dt_agendamento')
        dt_agendamento_com_hora = timezone.make_aware(
            timezone.datetime.combine(dt_agendamento, timezone.now().time())
        )

        if dt_agendamento_com_hora < timezone.now():
            raise forms.ValidationError("A data de agendamento não pode ser no passado.")

        return dt_agendamento

class FormSatisfacao(forms.ModelForm):
    class Meta:
        model = chamadoSatisfacao
        fields = ['avaliacao', 'comentario']
        