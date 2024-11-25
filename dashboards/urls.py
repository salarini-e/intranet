from django.urls import path, include
from . import views

app_name = 'dashboards'
urlpatterns = [
   path('', views.index, name='index'),
   path('api/get-dados-atendimento/', views.api_graf_total_atendimentos_realizados, name='get-dados-atendimento'),
   path('api/get-dados-servicos/', views.api_graf_tipo_servico, name='get-dados-servicos'),
   path('api/get-dados-internet/', views.api_graf_evolucao_chamados, name='get-dados-internet'),
   path('api/graf-evolucao-atendimentos/', views.api_graf_evolucao_atendimentos, name='get-dados-evolucao-atendimentos'),
   path('api/get-total-atendimentos-por-atendente/', views.api_total_atendimentos_por_atendente, name='get-total-atendimentos-por-atendente'),
   path('api/get-dados-impressora/', views.api_graf_evolucao_chamados_impressora, name='get-dados-impressora'),
   path('api/get-dados-computadores/', views.api_graf_evolucao_chamados_computadores, name='get-dados-computadores'),
   path('api/get-dados-sistemas/', views.api_graf_evolucao_chamados_sistemas, name='get-dados-sistemas'),
   path('api/get-dados-telefonia/', views.api_graf_evolucao_chamados_telefonia, name='get-dados-telefonia'),
   path('api/graf-chamados-secretaria/', views.api_graf_chamados_secretaria, name='get-dados-chamados-secretaria'),
   path('api/valores-tabela/', views.api_valores_dashboard, name='get-valores-tabela'),
]   