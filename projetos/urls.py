from django.urls import path
from . import views

app_name = 'projetos'
urlpatterns = [
    path('', views.index, name='index'),
    path('all/', views.todos_projetos, name='all'),
    path('<id>/board/', views.kanbanboard, name='index'),

    path('api/criar-projeto/', views.api_criar_projeto, name='api_criar_projeto'),
    path('api/criar-coluna/', views.api_criar_coluna, name='api_criar_coluna'),
    path('api/criar-card/', views.api_criar_card, name='api_criar_card'),
    path('api/deletar-card/', views.api_remover_card, name='api_remover_card'),
    path('api/mover-card/column/', views.api_mover_card_coluna, name='api_mover_card_coluna'),
    path('api/mover-card/line/', views.api_mover_card_linha, name='api_mover_card_linha'),
    path('api/check-card/', views.api_check_card, name='api_check_card'),
    path('api/editar-tarefa/', views.api_editar_tarefa, name='api_editar_tarefa'),
    path('<id>/detalhes/', views.api_get_detalhes_projeto, name='api_get_detalhes_projeto'),
    path('api/busca-membros/', views.api_busca_membros, name='api_busca_membros'),
    path('api/criar-grupo/', views.api_criar_grupo, name='api_criar_grupo'),
    path('api/meus-grupos/', views.api_meus_grupos, name='api_meus_grupos'),
    path('api/editar-projeto/', views.api_editar_projeto, name='api_editar_projeto'),
    path('api/editar-nome-coluna/', views.api_editar_nome_coluna, name='api_editar_coluna'),
    path('api/mover-coluna/', views.api_mover_coluna, name='api_mover_coluna'),
    path('api/get-grupos-projeto/<id>/', views.api_get_grupos_projeto, name='api_get_grupos_projeto'),
    path('api/atualizar-autorizacoes/', views.api_atualizar_autorizacoes, name='api_atualizar_autorizacoes'),
    path('api/enviar-anexo/', views.api_enviar_anexo, name='api_enviar_anexo'),
    path('api/get-projeto-comentarios/<id>/', views.api_get_projeto_comentarios, name='api_get_projeto_comentarios'),
    path('api/enviar-comentario/', views.api_enviar_comentario, name='api_enviar_comentario'),
    # path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    # path('project/new/', views.new_project, name='new_project'),
    # path('project/<int:project_id>/edit/', views.edit_project, name='edit_project'),
    # path('project/<int:project_id>/delete/', views.delete_project, name='delete_project'),
]