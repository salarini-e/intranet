from django.contrib import admin
from django.urls import path
from . import views

app_name='core'
urlpatterns = [
    # path('admin/', views.admin, name='admin'),
    path('', views.index, name='index'),    
    path('termos-de-uso/', views.termos_de_uso, name='termos_de_uso'),
    path('post-satisfacao/', views.post_satisfacao, name='post_satisfacao'),
    path('swot/', views.swot, name='swot'),
    path('get-matriculas/<ano>/<mes>', views.api_prefeitura_nf, name='api-prefeitura-nf')
]
