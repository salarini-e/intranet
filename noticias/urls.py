from django.urls import path
from . import views

app_name = 'noticias'   
urlpatterns = [
    # path('', views.index, name='index'),
    path('<int:noticia_id>/', views.detalhe, name='detalhe'),
]