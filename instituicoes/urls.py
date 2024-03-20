from django.contrib import admin
from django.urls import path
from . import views

app_name='ins'
urlpatterns = [
    path('api/', views.api, name='api'),
    path('api/criar-instituicao/', views.criar_instituicao, name='criar_instituicao'),
    path('api/get-setores/<id>/', views.getSetores, name='getSetores'),
]
