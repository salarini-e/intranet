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
]
