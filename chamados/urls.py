from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'chamados'
urlpatterns = [
    path('', views.index, name='index'),        
    path('criar-chamado/<sigla>/', views.criarChamado, name='criar'),
    path('<hash>/detalhes/', views.detalhes, name='detalhes'),    
    path('<hash>/detalhes/att/', views.attChamado, name='attChamado'),    
]
