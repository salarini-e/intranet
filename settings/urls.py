from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('autenticacao.urls')),
    path('', include('core.urls')),
    path('ponto/', include('controle_de_ponto.urls')),
    path('dashboard', include('dashboards.urls')),
    path('instituicoes/', include('instituicoes.urls')),
    path('telefonia/', include('telefonia.urls')),
    path('softwares/', include('softwares.urls')),
    path('formfacil/', include('formfacil.urls')),
    path('base-conhecimento/', include('base_conhecimento.urls')),
    path('chamados/', include('chamados.urls')),
    path("select2/", include("django_select2.urls")),
    path('agricultura/', include('agricultura_codigobarras.urls')),
    path('notificacoes/', include('notificacoes.urls')),
    path('noticias/', include('noticias.urls')),
    path('projetos/', include('projetos.urls')),
    path('planejamento-de-acoes/', include('planejamento_de_acoes.urls')),
    path('gestao-acao/', include('gestao_acao.urls')),
    path('ma/', include('ma_interno.urls')),
    # path('logwatcher/', include('django_logwatcher.urls')),
]   
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)