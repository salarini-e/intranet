from django.contrib import admin
from django.urls import path
from . import views

app_name='ins'
urlpatterns = [
    path('', views.index, name='index'),
    path('criar-secretaria/', views.criar_secretaria, name='criar_secretaria'),
    path('<id>/editar-secretaria/', views.editar_secretaria, name='editar_secretaria'),

    path('<id>/setores/', views.setores, name='setores'),
    path('<id>/setores/adicionar/', views.criar_setor, name='criar_setor'),
    path('<id>/setores/editar/', views.editar_setor, name='editar_setor'),
    path('<id>/setores/<id_setor>/adicionar-setor/', views.adicionar_servidor, name='adicionar_servidor'),

    path('api/', views.api, name='api'),    
    path('api/get-setores/<id>/', views.getSetores, name='getSetores'),
    path('api/get-servidor/', views.api_get_servidor, name='getServidor'),
    path('api/testar-cpf/', views.api_teste_cpf, name='testar_cpf'),
    

    path('get-servidores-from-site/90e7d30f99c6d6b95a29f40f68f46d53ad40b46a6b4a08e41d8532ee396f17a/', views.get_servidores_from_site, name='get_servidores_from_site'),
    path('cadastro-servidor/', views.cadastrar_servidor, name='cadastrar_servidor'),
]
