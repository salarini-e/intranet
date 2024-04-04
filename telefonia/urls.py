from django.contrib import admin
from django.urls import path
from . import views

app_name='tel'
urlpatterns = [
    path('', views.index, name='index'),
    path('editar-ramal/<ramal_id>/', views.editar_ramal, name='editar_ramal'),
    path('api/', views.index, name='api'),
    path('api/criar-ramal/', views.criarRamal, name='criarRamal'),
    path('api/getSetores/<id>/', views.getSetores, name='getSetores'),

]
