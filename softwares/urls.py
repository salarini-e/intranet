from django.contrib import admin
from django.urls import path
from . import views

app_name='soft'
urlpatterns = [
    path('sistemas/', views.sistemas, name='sistemas'),    
    path('sistemas/<slug>/', views.sistemas_listar, name='sistemas_listar'),    
    path('downloads/', views.downloads, name='downloads'),    
    path('downloads/<software_id>', views.download_file, name='download_file'),    

]
