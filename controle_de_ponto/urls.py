from django.urls import path
from . import views

app_name='controle_de_ponto'
urlpatterns = [
    path('', views.index, name='index'),
    path("exportar-excel/", views.exportar_excel, name="export_excel"),
    path('painel/', views.alocar_servidor, name='alocar_servidor'),
    path('painel/listagem/', views.painel, name='painel'),
    path('painel/acertar-ponto/', views.menu_acertar_ponto, name='menu_acertar_ponto'),
    path('painel/acertar-ponto/update/', views.menu_acertar_ponto_update, name='menu_acertar_ponto_update'),
    # path('gambiarra', views.gambiarra, name='gambiarra'),
    path('api/enviar-registro/', views.api_registrar_ponto, name='api_registrar_ponto'),
    path('api/detalhes-registro/<matricula>/', views.api_detalhes_registro, name='api_detalhes_registro'),
    path('registrar/<str:matricula>/', views.registrar_ponto_anterior, name='registrar_ponto_anterior'),
]