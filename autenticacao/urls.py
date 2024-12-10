from django.urls import path, include
from . import views
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView

app_name='autenticacao'
urlpatterns = [
    path('conta/', views.conta, name='conta'),
    path('conta/alterar-foto/', views.alterarFoto, name='alterar_foto'),
    path('conta/alterar-senha/', views.alterarSenha, name='alterar_senha'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('passwd_reset/', views.passwd_reset, name='passwd_reset'),
    path('passwd_reset_confirm/<uidb64>/<token>', views.PasswordResetConfirmView.as_view(), name='passwd_reset_confirm'),
    path('passwd_reset_done/', views.PasswordResetDoneView.as_view(), name='passwd_reset_done'),
    path('passwd_reset_complete/', views.PasswordResetCompleteView.as_view(), name='passwd_reset_complete'),

    path('cadastro/', views.cadastro_user, name='cadastrar_usuario'),
    path('cadastro/checkcpf/', views.checkCPF, name='checkcpf'),    

    path('cadastro-servidor/', views.cadastrar_servidor, name='cadastrar_servidor'),
    path('new-login/', views.new_login, name='new_login'),


    
]