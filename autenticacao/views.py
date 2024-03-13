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


def cadastro_user(request):
    
    form_pessoa = ''
    pessoa = ''
    is_user = False

    if request.user.is_authenticated:
        is_user = True

        try:
            pessoa = Pessoa.objects.get(user=request.user)
            form_pessoa = Form_Pessoa(initial={'email': request.user.email}, instance=pessoa)
            
        except Exception as e:
            form_pessoa = Form_Pessoa(initial={'email': request.user.email})
    else:
        form_pessoa = Form_Pessoa()

    if request.method == "POST":
        if pessoa:
            form_pessoa = Form_Pessoa(request.POST, instance=pessoa)
        else:
            form_pessoa = Form_Pessoa(request.POST)

        if form_pessoa.is_valid():

            # com o objetivo de diminuir a identação, e não sendo possível utilizar guard clauses, optei em 
            # verificar o is_user duas vezes
            if is_user or request.POST['password'] == request.POST['password2']:
                if is_user or len(request.POST['password']) >= 8:
                    try:
                        user = ''

                        if is_user:
                            user = User.objects.get(id=request.user.id)
                            user.email = request.POST['email']
                            user.save()
                        else:
                            user = User.objects.create_user(
                                username=request.POST['email'], email=request.POST['email'], password=request.POST['password'])
                            user.first_name = request.POST['nome']
                            user.save()

                        pessoa = form_pessoa.save(commit=False)
                        pessoa.user = user

                        pessoa.save()
                        messages.success(request, 'Usuário cadastrado com sucesso!')
                        user = authenticate(request, username=request.POST['email'], password=request.POST['password'])
                        if user is not None:
                                login(request, user)
                                if pessoa.possui_cnpj:
                                    return redirect('empreendedor:cadastrar_empresa')
                                try:
                                    return redirect(request.GET['next'])
                                except:
                                    return redirect('/')
                        else:
                                context = {
                                    'error': True,
                                }
                    except Exception as e:
                        messages.error(
                            request, 'Email de usuário já cadastrado')
                        
                messages.error(
                    request, 'A senha deve possuir pelo menos 8 caracteres')
            else:                
                messages.error(request, 'As senhas digitadas não se coincidem')
    context = {
        'form_pessoa': form_pessoa,
        'is_user': is_user
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