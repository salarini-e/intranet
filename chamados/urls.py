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
    path('<hash>/iniciar-atendimento/', views.iniciar_atendimento, name='inicializar'),
    path('<hash>/finalizar-atendimento/', views.finalizar_atendimento, name='finalizar'),

    path('criar-periodos/', views.criar_periodos, name='criar_periodos'),
    path('api/', views.index, name='api'),
    path('api/setor/', views.api_criar_setor, name='api_criar_setor'),
    path('api/servidor/', views.api_criar_servidor, name='api_criar_servidor')
]
