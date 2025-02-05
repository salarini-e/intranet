from django.urls import path
from . import views

app_name='controle_de_ponto'
urlpatterns = [
    path('', views.index, name='index'),
    path("exportar-excel/", views.exportar_excel, name="export_excel"),
    path('painel/', views.alocar_servidor, name='alocar_servidor'),
    path('painel/listagem/', views.painel, name='painel'),
    # path('gambiarra', views.gambiarra, name='gambiarra'),
    path('api/enviar-registro/', views.api_registrar_ponto, name='api_registrar_ponto'),
    path('api/detalhes-registro/<matricula>/', views.api_detalhes_registro, name='api_detalhes_registro'),
]