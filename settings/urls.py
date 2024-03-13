from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('autenticacao.urls')),
    path('', include('core.urls')),
    path('instituicoes/', include('instituicoes.urls')),
    path('telefonia/', include('telefonia.urls')),
    path('formfacil/', include('formfacil.urls')),
]
