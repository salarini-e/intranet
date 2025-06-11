from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.views import PasswordContextMixin
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError

from .models import *
from .forms import *

from django.contrib.auth.decorators import login_required
from urllib.parse import urlparse, urlunparse

from django.conf import settings
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import (
    url_has_allowed_host_and_scheme, urlsafe_base64_decode,
)
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from instituicoes.models import Secretaria, Setor, Servidor
from settings.settings import hCAPTCHA_PRIVATE_KEY, hCAPTCHA_PUBLIC_KEY
import requests

def conta(request):
    if request.method == 'POST':
        servidor = Servidor.objects.get(user=request.user)
        servidor.avatar = request.FILES['foto']
        servidor.save()
    context = {
        'servidor': Servidor.objects.get(user=request.user)
    }
    return render(request, 'autenticacao/index.html', context)

def alterarSenha(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')                    
            
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
        'titulo': 'Mudar Senha'
    }
    return render(request, 'autenticacao/form_senha.html', context)

def alterarFoto(request):
    if request.method == 'POST':
        servidor = Servidor.objects.get(user=request.user)
        servidor.foto = request.FILES['foto']
        servidor.save()
        return redirect('autenticacao:conta')
    
    context = {
        'servidor': Servidor.objects.get(user=request.user)
    }
    return render(request, 'autenticacao/form.html', context)

def alterarDados(request):
    if request.method == 'POST':
        servidor = Servidor.objects.get(user=request.user)
        servidor.nome = request.POST['nome']
        servidor.email = request.POST['email']
        servidor.telefone = request.POST['telefone']
        servidor.celular = request.POST['celular']
        servidor.save()
        return redirect('autenticacao:conta')
    
    context = {
        'servidor': Servidor.objects.get(user=request.user)
    }
    return render(request, 'autenticacao/form.html', context)

def login_view(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('/')
    

    if request.method == 'POST':

        #  Abaixo recebemos a validação da API do Google do reCAPTCHA
        ''' Begin reCAPTCHA validation '''
        recaptcha_response = request.POST.get('h-captcha-response')
        data = {
            'secret': hCAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://hcaptcha.com/siteverify', data=data)
        result = r.json()
        ''' End reCAPTCHA validation '''
        # result={'success': True}
        
        if not result['success']:
            messages.error(request, 'Por favor, confirme que você não é um robô.')
            context = {
                'hCAPTCHA': hCAPTCHA_PUBLIC_KEY,
            }
            return render(request, 'adm/new_login.html', context)
        
        username = request.POST['username']
        password = request.POST['password']
        if len(username)==5 and username.isdigit():
            username = '0'+username
        try:
            pessoa=Pessoa.objects.get(cpf=username)    
            user = authenticate(request, username=pessoa.email, password=password)
        except:            
            user = None
        if user == None:
            if len(username)==5 and username.isdigit():
                user = authenticate(request, username='0'+username, password=password)
            else:
                user = authenticate(request, username=username, password=password)
        if user == None:           
            try:                                    
                pessoa=Pessoa.objects.get(cpf=username)                                
                user = authenticate(request, username=pessoa.cpf, password=password)
            except:
                user = None
            if user == None:                
                user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.POST.get('next')
            
            # Verifica se a URL é segura
            if url_has_allowed_host_and_scheme(next_url, allowed_hosts=request.get_host()):
                return redirect(next_url)
            else:
                print("URL não segura, redirecionando para a página inicial.")
                return redirect('/')
        else:
            if User.objects.filter(username=username).exists():
                msg = 'Login ou senha invalidos'
            else:
                msg = 'Usuário não cadastrado. Por favor, cadastre-se.'
            
            context = {
                'error': True,
                'msg': msg,
                'hCAPTCHA': hCAPTCHA_PUBLIC_KEY,
            }
    else:
        context = {
            'hCAPTCHA': hCAPTCHA_PUBLIC_KEY,
        }   
    return render(request, 'adm/new_login.html', context)

def passwd_reset(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Solicitação de alteração de senha do sistema INTRANET"
                    email_template_name = "adm/email_passwd_reset.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'https',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, user.email, [
                                  user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("autenticacao:passwd_reset_done")
            else:
                messages.error(request, 'Email não cadastrado no sistema.')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="adm/passwd_reset.html", context={"password_reset_form": password_reset_form})

class PasswordResetDoneView(PasswordContextMixin, TemplateView):
    template_name = 'adm/passwd_reset_done.html'
    title = _('Password reset sent')
    
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/login')
    else:
        return redirect('/')

INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'

class PasswordResetConfirmView(PasswordContextMixin, FormView):
    form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    reset_url_token = 'set-password'
    success_url = reverse_lazy('autenticacao:passwd_reset_complete')
    template_name = 'adm/passwd_reset_confirm.html'
    title = _('Entre com a nova senha')
    token_generator = default_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs

        self.validlink = False
        self.user = self.get_user(kwargs['uidb64'])

        if self.user is not None:
            token = kwargs['token']
            if token == self.reset_url_token:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                   
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(token, self.reset_url_token)
                    return HttpResponseRedirect(redirect_url)
        
        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        try:            
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist, ValidationError):
            user = None
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        if self.post_reset_login:
            auth_login(self.request, user, self.post_reset_login_backend)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context['validlink'] = True
        else:
            context.update({
                'form': None,
                'title': _('Falha ao redefinir a senha.'),
                'validlink': False,
            })
        return context

class PasswordResetCompleteView(PasswordContextMixin, TemplateView):
    template_name = 'adm/passwd_reset_complete.html'
    title = _('Senha redefinida')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url(settings.LOGIN_URL)
        return context

from instituicoes.forms import ServidorForm2
from .functions import enviar_email_apos_cadastrar
def cadastro_user(request):
    if request.user.is_authenticated:
        return redirect('/')

    context = {
        'hCAPTCHA': hCAPTCHA_PUBLIC_KEY,
    }

    if request.method == "POST":

         #  Abaixo recebemos a validação da API do Google do reCAPTCHA
        ''' Begin reCAPTCHA validation '''
        recaptcha_response = request.POST.get('h-captcha-response')
        data = {
            'secret': hCAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://hcaptcha.com/siteverify', data=data)
        result = r.json()
        ''' End reCAPTCHA validation '''
        # result={'success': True}
        
        if not result['success']:
            messages.error(request, 'Por favor, confirme que você não é um robô.')
            return render(request, 'adm/new_cadastro.html', context)
        
        """
        'csrfmiddlewaretoken': ['MD2KkFbCaaV1X8jUHnC4xOmKjuSuQqpJDR2y4u6v6Ig2dKWeBLL3lh4yE2auEm3O'], 
        'matricula': ['63508'], 
        'name': ['LUIS EDUARDO CORDEIRO SALARINI'], 
        'cpf_oculto': ['***.535.177-**'], 
        'cpf': ['152.535.177-07'], 
        'secretaria': ['1'], 
        'setor': ['0'], 
        'outro': ['Teste'], 
        'email': ['eduardo.pmnf@gmail.com'], 
        'telefone': ['(22) 99252-2121'], 
        'consentimento': ['on']}>

        """        
        cpf_oculto = request.POST.get('cpf_oculto', '').replace('*', '')
        cpf = request.POST.get('cpf', '')
        form = ServidorForm2(request.POST)
        if cpf_oculto in cpf:
            if form.is_valid():
                try:
                    servidor = form.save(commit=False)
                    servidor.setor = form.get_setor(request)
                    servidor.user = form.create_user()
                    servidor.user_inclusao = None
                    servidor.save()
                    messages.success(request, f'Servidor cadastrado(a) com sucesso! Foi enviado um email com as informações do seu login.')
                    enviar_email_apos_cadastrar(servidor.user)
                    return redirect('/')
                except Exception as e:
                    messages.error(request, f'Erro ao cadastrar servidor: {str(e)}')
                    context['form'] = form
                    context['form_errors'] = form.errors
                    return render(request, 'adm/new_cadastro.html', context)
            else:
                context['form'] = form
                context['form_errors'] = form.errors
                messages.error(request, 'Erro ao cadastrar servidor. Verifique os campos destacados.')
                return render(request, 'adm/new_cadastro.html', context)
        else:
            messages.error(request, 'CPF incorreto!')
            context['form'] = form
            return render(request, 'adm/new_cadastro.html', context)

    context['form'] = ServidorForm2()
    return render(request, 'adm/new_cadastro.html', context)


import json
def checkCPF(request):    
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        cpf = data.get('cpf')
        try:
            cpf = validate_cpf(cpf)
        except:
            response_data = {'exists': True, 'message': 'CPF inválido.'}
            return JsonResponse(response_data)
        try:
            pessoa = Pessoa.objects.get(cpf=cpf)
            response_data = {'exists': True, 'message': 'CPF já existe no banco de dados.'}
        except:
                response_data = {'exists': False}

        return JsonResponse(response_data)
    return JsonResponse({})


def cadastrar_servidor(request):
    if request.method == 'POST':
        cpf_oculto = request.POST.get('cpf_oculto')
        cpf_oculto = cpf_oculto.replace('*', '')
        cpf = request.POST.get('cpf')
        if cpf_oculto in cpf:
            print("Os dígitos ocultos estão contidos no CPF completo.")
        else:
            messages.error(request, 'CPF incorreto!')
            
        
    return render(request, 'instituicoes/cadastrar_servidor.html')

def new_login(request):
    return render(request, 'adm/new_login.html')

def new_cadastrar(request):
    return render(request, 'adm/new_cadastrar.html')
import os
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import HttpResponse

def upload_csv_view(request):
    if request.method == 'POST' and 'file' in request.FILES:
        uploaded_file = request.FILES['file']
        if uploaded_file.name.endswith('.csv'):  # Verifica se é um CSV
            file_name = uploaded_file.name
            file_path = os.path.join(settings.MEDIA_ROOT, 'grdData.csv')

            # Salvar o arquivo dentro de MEDIA_ROOT
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            return render(request, 'autenticacao/upload_csv.html', {'status': True})
        else:
            return HttpResponse("Por favor, envie um arquivo CSV.", content_type="text/html")

    return render(request, 'autenticacao/upload_csv.html')

from .management.commands.verificar_metaservidores import processar_csv
from .management.commands.cadastrar_nao_encontrados import cadastrar_nao_encontrados


def atualizar_meta_servidores_1(request):
    try:
        processar_csv()
        msg = 'Processamento finalizado. Verifique o arquivo de log: matriculas_nao_encontradas.csv'
        print('opa')
    except Exception as e:        
        print('Erro ao processar o arquivo:', str(e))
        if  str(e)== "'Matricula'":
            msg = {'status': 400, 'msg': 'Altere o cabeçaho do arquivo CSV<br>conforme as instruções ao lado.'}
        else:
            msg = {'status': 400, 'msg': f'Erro ao processar o arquivo: {str(e)}'}
        return render(request, 'autenticacao/upload_csv.html', {'status': False, 'msg': msg})
    return redirect('autenticacao:atualizar-meta-servidores2')
        
    
    return render(request, 'autenticacao/upload_csv.html', {'status': False, 'msg': msg})

def atualizar_meta_servidores_2(request):    
    try:
        cadastrar_nao_encontrados()
        msg = {'status': 200, 'msg': 'Processamento finalizado. Banco atualizado!'}
    except Exception as e:
        msg = {'status': 400, 'msg': f'Erro ao processar o arquivo: {str(e)}'}
    return render(request, 'autenticacao/upload_csv.html', {'status': False, 'msg': msg})

