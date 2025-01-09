from django.urls import path
from . import views

urlpatterns = [
    path('', views.kanbanboard, name='index'),
    # path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    # path('project/new/', views.new_project, name='new_project'),
    # path('project/<int:project_id>/edit/', views.edit_project, name='edit_project'),
    # path('project/<int:project_id>/delete/', views.delete_project, name='delete_project'),
]