from django.urls import path
from . import views

app_name = 'projetos'
urlpatterns = [
    path('', views.index, name='index'),
    path('<id>/board/', views.kanbanboard, name='index'),

    path('api/criar-projeto/', views.api_criar_projeto, name='api_criar_projeto'),
    path('api/criar-coluna/', views.api_criar_coluna, name='api_criar_coluna'),
    # path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    # path('project/new/', views.new_project, name='new_project'),
    # path('project/<int:project_id>/edit/', views.edit_project, name='edit_project'),
    # path('project/<int:project_id>/delete/', views.delete_project, name='delete_project'),
]