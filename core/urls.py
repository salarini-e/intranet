from django.contrib import admin
from django.urls import path
from . import views

app_name='core'
urlpatterns = [
    path('', views.index, name='index'),
    path('post-satisfacao/', views.post_satisfacao, name='post_satisfacao'),
]
