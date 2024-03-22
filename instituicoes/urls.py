from django.contrib import admin
from django.urls import path
from . import views

app_name='ins'
urlpatterns = [
    path('', views.index, name='index'),
    path('criar-secretaria/', views.criar_secretaria, name='criar_secretaria'),
    path('api/', views.api, name='api'),    
    path('api/get-setores/<id>/', views.getSetores, name='getSetores'),
]
