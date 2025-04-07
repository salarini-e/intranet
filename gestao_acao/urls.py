from django.urls import path, include
from . import views

app_name = 'gestao_acao'

urlpatterns = [
    path('', views.index, name='index'),
    path('atualiza-data/', views.atualizar_data, name='atualizar_data'),
    path('adicionar_acao/', views.adicionar_acao, name='adicionar_acao'),

]