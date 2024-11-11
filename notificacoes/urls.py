from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('check/', views.checkNotificationNew, name='check_notifications'),
      path('marcar_como_lida/', views.marcar_como_lida, name='marcar_como_lida'),
]