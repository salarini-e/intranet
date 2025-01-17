from django.urls import path
from . import views

app_name='controle_de_ponto'
urlpatterns = [
    path('', views.index, name='index'),
    path('painel/', views.painel, name='painel'),
    path('api/enviar-registro/', views.api_registrar_ponto, name='api_registrar_ponto'),
]