from django.urls import path
from . import views

app_name = 'django_logwatcher'

urlpatterns = [
    # Página inicial que pode exibir um resumo ou visão geral dos logs
    path('', views.log_list_view, name='index'),
    path('json/', views.log_list_json, name='log_list_json'),
    # Página para exibir logs filtrados ou por categoria
    # path('logs/', views.logs, name='logs'),

    # Página para exibir detalhes de um log específico
    # path('logs/<int:log_id>/', views.log_detail, name='log_detail'),

    # Caso queira implementar um filtro de logs por data ou severidade
    # path('logs/filter/', views.filter_logs, name='filter_logs'),
]
