from django.urls import path
from . import views

app_name = 'backup_maneger'
urlpatterns = [
    path('', views.index, name='index'),
    path('listar/<str:subdir>/', views.list_db_files, name='list_db_files'),
    path('download/<str:subdir>/<str:file_name>/', views.download_file, name='download_file'),
    path('novo-backup/', views.novo_backup, name='novo_backup'),
]