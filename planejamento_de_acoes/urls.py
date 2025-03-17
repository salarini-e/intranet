from django.urls import path
from . import views

app_name = 'planejamento_acoes'
urlpatterns = [
    path('', views.index, name='index'),
]