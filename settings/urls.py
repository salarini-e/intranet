from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('autenticacao.urls')),
    path('', include('core.urls')),
    path('instituicoes/', include('instituicoes.urls')),
    path('telefonia/', include('telefonia.urls')),
    path('softwares/', include('softwares.urls')),
    path('formfacil/', include('formfacil.urls')),
    path('chamados/', include('chamados.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)