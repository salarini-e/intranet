from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'chamados'
urlpatterns = [
    path('', views.pagina_inicial, name='index'),   
    path('dashboard/', views.painel_controle, name='painel_controle'),   
    path('relatorio/', views.gerar_relatorio, name='relatorio'),
    path("detalhesTicketsNaoResolvidos/", views.ver_detalhes_tickets_nao_resolvidos, name="detalhesTicketsNaoResolvidos"),    
    path('zerar-filtros/', views.zerar_filtros, name='zerar_filtros'),
    path('criar-chamado/', views.criarChamadoEscolher, name='criar_chamado_escolher'),
    path('criar-chamado/<sigla>/', views.criarChamado, name='criar'),

    path('<hash>/detalhes/', views.detalhes, name='detalhes'),    
    path('<hash_chamado>/detalhes/editar/', views.editar_chamado, name='editar'),    
    path('<hash>/detalhes/att/', views.attChamado, name='attChamado'),    
    path('<hash>/iniciar-atendimento/', views.iniciar_atendimento, name='inicializar'),
    path('<hash>/pausar/', views.declarar_motivo_pausa, name='motivo'),
    path('<hash>/pausar/motivo/', views.pausar_atendimento, name='pausar'),
    path('<hash>/retomar/', views.retomar_atendimento, name='retomar'),
    path('<hash>/finalizar-atendimento/', views.finalizar_atendimento, name='finalizar'),
    path('<hash>/detalhes/agendar', views.agendar_atendimento, name='agendar_atendimento'),    
    path('<hash>/detalhes/imprimir', views.detalhes_imprimir, name='imprimir'), 

    path('<matricula>/ver-perfil/', views.ver_perfil, name='ver-perfil'),

    path('criar-periodos/', views.criar_periodos, name='criar_periodos'),
    path('api/', views.index, name='api'),

    path('api/mudar/status/', views.api_mudar_status, name='api_status'),
    path('api/mudar/prioridade/', views.api_mudar_prioridade, name='api_prioridade'),
    path('api/mudar/atendente/', views.api_mudar_atendente, name='api_atendente'),
    path('api/setor/', views.api_criar_setor, name='api_criar_setor'),
    path('api/servidor/', views.api_criar_servidor, name='api_criar_servidor'),
    path('api/<hash>/relatorio/', views.api_relatorio, name='api_relatorio'),
    path('api/<hash>/relatorio/form/', views.api_montarFormRelatorio, name='api_form_relatorio'),
    path('api/get-data-servidor/', views.api_get_data_servidor, name='api_get_data_servidor'),

    path('tickets/', views.tickets, name ='tickets'),
    path('tickets/mesclar/', views.mesclar_chamados, name ='mesclar'),
    path('tickets/ordernar/', views.ordenarPorNaoFechados, name ='ordernarPorNaoFechados'),
    path('verificar-atualizacoes/', views.verificar_atualizacoes, name='verificar-atualizacoes'),

    path('download/relatorio/', views.download_relatorio, name='download_relatorio'),
]
