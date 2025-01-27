from django.urls import path
from . import views

app_name='controle_de_ponto'
urlpatterns = [
    path('', views.index, name='index'),
    path("exportar-excel/", views.exportar_excel, name="export_excel"),
    path('painel/', views.painel, name='painel'),
    path('painel/alocar-servidor/', views.alocar_servidor, name='alocar_servidor'),
    path('gambiarra', views.gambiarra, name='gambiarra'),
    path('api/enviar-registro/', views.api_registrar_ponto, name='api_registrar_ponto'),
]