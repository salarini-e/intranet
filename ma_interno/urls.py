from django.urls import path
from . import views

urlpatterns = [
    path('imagem/<int:primary_key>/', views.imagem, name='imagem'),
    path('imagem_bkp/<int:primary_key>/', views.imagem_bkp, name='imagem_bkp'),
    path('canudos/<int:primary_key>/', views.canudos, name='canudos'),
    path('canudos_bkp/<int:primary_key>/', views.canudos_bkp, name='canudos_bkp'),
    path('abre/<str:arquivo>/', views.abre, name='abre'),
]
