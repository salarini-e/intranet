from django.urls import path
from .views import cadastrar_equipamento, visualizar_equipamento, index, ler_codido, visualizar_equipamento_hash, detalhes_imprimir_agricultura

app_name = 'agricultura_codigobarras' 

urlpatterns = [
    path('', index, name='index'),
    path('ler-codigo-de-barras/', ler_codido, name='ler_codigo_barra'),
    path('cadastrar-equipamento/', cadastrar_equipamento, name='cadastrar_equipamento'),
    path('visualizar-equipamento/<str:codigo_barra>/', visualizar_equipamento, name='visualizar_equipamento'),
    path('visualizar/<int:hash>/', visualizar_equipamento_hash, name='visualizar-equipamento-hash'),
    path('<hash>/detalhes/imprimir', detalhes_imprimir_agricultura, name='imprimir'), 
]

