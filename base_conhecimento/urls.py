from django.urls import path
from . import views

app_name = 'base_conhecimento'

urlpatterns = [
    path('', views.index, name='index'),
    path('subtopicos/<int:topico_id>/', views.subtopicos, name='subtopicos'),
    path('subtopicos/<int:topico_id>/<int:subtopico_id>', views.displayVideo, name='display_video'),
    path('download-video/<int:topico_id>/<int:subtopico_id>/', views.download_video, name='download_video'),
]
