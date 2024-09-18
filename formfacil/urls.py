from django.urls import path, include
from . import views

app_name = 'formfacil'
urlpatterns = [
    path('', views.index, name='index'),
    path('BA988BDD380A2EFD4E6CD29B225BA0C4/', views.IndicacaoComitePSP, name='indicacao_comite_psp'),
    path('webex/', views.webex, name='webex'),
    path('cadastro-el/', views.cadastro_el_view, name='cadastro_el'),
    path('snct2024/', views.snct2024, name='snct2024'),
    path('snct2024/export', views.snct2024_export, name='snct2024_export'),
    path('cadastro-processo-digital', views.cadastroAulasProcessoDigial, name='cadastro-processo-digital'),
    path('cadastro-treinamento-tributario-emissores', views.cadastroTreinamentoTributarioEmissoresTaxas, name='cadastro-treinamento-tributario-emissores'),
    path('cadastro-treinamento-tributario-contadores', views.cadastroTreinamentoTributarioContadores, name='cadastro-treinamento-tributario-contadores'),
    path('cadastro-processo-digital', views.cadastroAulasProcessoDigial, name='cadastro-processo-digital'),

    #### URLS PARA VISUALIZAÇÃO DE DADOS ####
    path('visualizar/cadastro-processo-digital/', views.visualizarDados_Aulas_Processo_Digital, name='visualizar_aulas_processo_digital'),

    path('visualizar/cadastros-treinamento-tributario-emissores/', views.visualizarDados_TT_Emissores, name='cadastros-treinamento-tributario-emissores'),
    path('visualizar/cadastros-treinamento-tributario-contadores/', views.visualizarDados_TT_Contadores, name='cadastros-treinamento-tributario-contadores'),
    
    path('exportar/cadastro-processo-digital/', views.exportar_aulas_processo_digital_to_excel, name='exportar_aulas_processo_digital'),
    path('exportar/treinamento-tributario-emissores-taxas/', views.exportar_aulas_tributario_emissores_to_excel, name='exportar_treinamento_tributario_emissores_taxas'),
    path('exportar/treinamento-tributario-contadores/', views.exportar_aulas_tributario_contadores_to_excel, name='exportar_treinamento_tributario_contadores'),
    path('cadastros-repetidos/', views.logCadastrosRepetidos, name='cadastros_repetidos'),
       
]
