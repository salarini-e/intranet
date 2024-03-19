from . import views
from django.urls import path

app_name = 'chamados'
urlpatterns = [
    path('', views.mainPage, name='mainPage'),
    path('login/',views.loginView, name='login'),
    path('cadastro/',views.cadastroView, name='cadastro'),
    path('sairFunc/', views.sairFunc, name='sairFunc'),
    path('chamado/<int:idChamado>',views.chamado, name='chamado'),
    path('abrirChamado/<str:tipo>', views.abrirChamado, name='abrirChamado'),
    path('abrirChamadoInternet/', views.abrirChamadoInternet, name='abrirChamadoInternet'),
    path('abrirChamadoSistema/', views.abrirChamadoSistema, name='abrirChamadoSistema'),
    path('abrirChamadoImpressora/', views.abrirChamadoImpressora, name='abrirChamadoImpressora'),
    path('indicadores/', views.indicadores, name='indicadores'),
    path('atendentes/', views.atendentes, name='atendentes'),
    path('servidores/', views.listaServidores, name='servidores'),
    path('servidor/<int:idServidor>', views.servidor, name='servidor'),
    path('apagaServidor/<int:idServidor>', views.apagaServidor, name='apagaServidor'),
    path('editaChamado/<int:idChamado>/', views.editaChamado, name='editaChamado'),
    path('addSetor/', views.addSetor, name='addSetor'), 
    path('addComentario/<int:idChamado>/', views.addComentario, name='addComentario'), 
    path('atualizaChamado/<int:idChamado>/', views.atualizaChamado, name='atualizaChamado'),
    path('transformaParaAtendente/', views.transformaParaAtendente, name='transformaParaAtendente'),
    path('transformaParaServidor/<int:atendente>', views.transformaParaServidor, name='transformaParaServidor'),
    path('userIsStaff/', views.userIsStaff, name='userIsStaff'),        
]
