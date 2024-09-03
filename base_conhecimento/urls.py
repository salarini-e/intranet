from django.contrib import admin
from django.urls import path
from . import views

app_name='base_conhecimento'
urlpatterns = [
    path('', views.index, name='index'),
    path('subtopicos/<int:topico_id>/', views.subtopicos, name='subtopicos'),

]
