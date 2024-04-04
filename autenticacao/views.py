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
            return redirect('autenticacao:conta')                    
            
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
        username = request.POST['username']
        password = request.POST['password']
        try:
            pessoa=Pessoa.objects.get(cpf=username)    
            user = authenticate(request, username=pessoa.email, password=password)
        except:            
            user = None
        if user == None:
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
            try:
                return redirect(request.GET['next'])
            except Exception as E:
                print(E)
                return redirect('/')
        else:
            context = {
                'error': True,
            }
    return render(request, 'adm/login.html', context)

def passwd_reset(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Solicitação de alteração de senha do sistema Desenvolve NF"
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
def cadastro_user(request):
    
    if request.user.is_authenticated:
        return redirect('/')

       

    if request.method == "POST":
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
        cpf_oculto = request.POST.get('cpf_oculto')
        cpf_oculto = cpf_oculto.replace('*', '')
        cpf = request.POST.get('cpf')
        if cpf_oculto in cpf:
            form = ServidorForm2(request.POST)        
            if form.is_valid():
                servidor = form.save()
                servidor.setor = form.get_setor(request)
                servidor.user = form.create_user()
                servidor.user_inclusao = request.user
                servidor.save()
                messages.success(request, f'Servidor {servidor.nome} cadastrada com sucesso!')
        
                return redirect('/')            
            else:
                print(form.errors)
                messages.error(request, 'Erro ao cadastrar servidor.')
        else:
            messages.error(request, 'CPF incorreto!')
            
        
        if False:

        
            user = User.objects.create_user(
                username=request.POST['email'], email=request.POST['email'], password=request.POST['password'])
            user.first_name = request.POST['nome']
            user.save()

            # servidor = form_pessoa.save(commit=False)
            # servidor.user = user

            #             pessoa.save()
            #             messages.success(request, 'Usuário cadastrado com sucesso!')
            #             user = authenticate(request, username=request.POST['email'], password=request.POST['password'])
            #             if user is not None:
            #                     login(request, user)
            #                     if pessoa.possui_cnpj:
            #                         return redirect('empreendedor:cadastrar_empresa')
            #                     try:
            #                         return redirect(request.GET['next'])
            #                     except:
            #                         return redirect('/')
            #             else:
            #                     context = {
            #                         'error': True,
            #                     }
            #         except Exception as e:
            #             messages.error(
            #                 request, 'Email de usuário já cadastrado')
                        
            #     messages.error(
            #         request, 'A senha deve possuir pelo menos 8 caracteres')
            # else:                
            #     messages.error(request, 'As senhas digitadas não se coincidem')
    context = {
        
    }    
    return render(request, 'adm/cadastro.html', context)


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
