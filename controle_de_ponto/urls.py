from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/enviar-registro/', views.api_registrar_ponto, name='api_registrar_ponto'),
]