from django.contrib import admin
from django.urls import path
from . import views

app_name='tel'
urlpatterns = [
    path('', views.index, name='index'),
    path('api/criar-ramal/', views.criarRamal, name='criarRamal'),

]
