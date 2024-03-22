from django.urls import path, include
from . import views
urlpatterns = [
#    path('', views.index, name='index'),
    path('BA988BDD380A2EFD4E6CD29B225BA0C4/', views.IndicacaoComitePSP, name='indicacao_comite_psp'),
    path('webex/', views.IndicacaoComitePSP, name='indicacao_comite_psp')
]
