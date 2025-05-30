from django.urls import path, include
from . import views
from .views.cadastro_de_almoxarifado import cadastro_de_almoxarifado, visualizar_cadastros_almoxarifado, exportar_cadastros_almoxarifado
from .views.avaliacao_el import avaliacao_sistemas_el
from .views.solicitacao_email_institucional import (
    cadastro_solicitacao_email_institucional,
    visualizar_cadastros_solicitacao_email_institucional,
    exportar_cadastros_solicitacao_email_institucional
)
from .views.treinamento_tributario import exportar_decretos_portaria_atos_to_excel

from .views.padronizacao_pagamento import exportar_padronizacao_pagamento_to_excel, cadastro_padronizacao_pagamento, visualizar_padronizacao_pagamento

from .views.processo_digital import exportar_processo_digital_to_excel, cadastro_processo_digital, visualizar_processo_digital

app_name = 'formfacil'
urlpatterns = [
    path('', views.index, name='index'),
    path('BA988BDD380A2EFD4E6CD29B225BA0C4/', views.IndicacaoComitePSP, name='indicacao_comite_psp'),
    path('webex/', views.webex, name='webex'),
    path('snct2024/', views.snct2024, name='snct2024'),
    path('snct2024/export', views.snct2024_export, name='snct2024_export'),
    path('cadastro-processo-digital', views.cadastroAulasProcessoDigial, name='cadastro-processo-digital'),
    path('cadastro-treinamento-tributario-emissores', views.cadastroTreinamentoTributarioEmissoresTaxas, name='cadastro-treinamento-tributario-emissores'),
    path('cadastro-treinamento-tributario-contadores', views.cadastroTreinamentoTributarioContadores, name='cadastro-treinamento-tributario-contadores'),
    path('cadastro-processo-digital', views.cadastroAulasProcessoDigial, name='cadastro-processo-digital'),
    path('inscricao-ato-prefeito', views.cadastroDecretos2024, name='inscricao-ato-prefeito'),

    path('inscricao-decretos-portaria-atos-prefeito', views.inscricaoDecretosPortariaAtosPrefeito, name='inscricao-decretos-portaria-atos-prefeito'),
    #### URLS PARA VISUALIZAÇÃO DE DADOS ####
    path('visualizar/cadastro-processo-digital/', views.visualizarDados_Aulas_Processo_Digital, name='visualizar_aulas_processo_digital'),

    path('visualizar/cadastros-treinamento-tributario-emissores/', views.visualizarDados_TT_Emissores, name='cadastros-treinamento-tributario-emissores'),
    path('visualizar/cadastros-treinamento-tributario-contadores/', views.visualizarDados_TT_Contadores, name='cadastros-treinamento-tributario-contadores'),
    path('visualizar/cadastros-decretos-portaria-atos-prefeito/', views.visualizarDados_Decreto_Portaria_Atos_Prefeito, name='cadastros-decretos-portaria-atos-prefeito'),
    path('exportar/decretos-portaria/', exportar_decretos_portaria_atos_to_excel, name='exportar_decretos_portaria'),
    path('exportar/cadastro-processo-digital/', views.exportar_aulas_processo_digital_to_excel, name='exportar_aulas_processo_digital'),
    path('exportar/treinamento-tributario-emissores-taxas/', views.exportar_aulas_tributario_emissores_to_excel, name='exportar_treinamento_tributario_emissores_taxas'),
    path('exportar/treinamento-tributario-contadores/', views.exportar_aulas_tributario_contadores_to_excel, name='exportar_treinamento_tributario_contadores'),
    path('cadastros-repetidos/', views.logCadastrosRepetidos, name='cadastros_repetidos'),
    path('cadastro-almoxarifado/', cadastro_de_almoxarifado, name='cadastro_almoxarifado'),
    path('visualizar/cadastros-almoxarifado/', visualizar_cadastros_almoxarifado, name='visualizar_cadastros_almoxarifado'),
    path('exportar/cadastros-almoxarifado/', exportar_cadastros_almoxarifado, name='exportar_cadastros_almoxarifado'),
    path('avaliacao-sistemas-el/', avaliacao_sistemas_el, name='avaliacao_sistemas_el'),
    path('habitacao/', views.form_augusto, name='form_augusto'),
    path('cadastro-solicitacao-email-institucional/', cadastro_solicitacao_email_institucional, name='cadastro_solicitacao_email_institucional'),
    path('visualizar/solicitacao-email-institucional/', visualizar_cadastros_solicitacao_email_institucional, name='visualizar_solicitacao_email_institucional'),
    path('exportar/solicitacao-email-institucional/', exportar_cadastros_solicitacao_email_institucional, name='exportar_solicitacao_email_institucional'),
    path('cadastro-processo-digital-2025/', views.cadastro_processo_digital, name='cadastro_processo_digital'),
    path('visualizar/processo-digital-2025/', views.visualizar_processo_digital, name='visualizar_processo_digital'),
    path('cadastro-padronizacao-pagamento-2025/', views.cadastro_padronizacao_pagamento, name='cadastro_padronizacao_pagamento'),
    path('visualizar/padronizacao-pagamento-2025/', views.visualizar_padronizacao_pagamento, name='visualizar_padronizacao_pagamento'),

    path('exportar/padronizacao-pagamento/', exportar_padronizacao_pagamento_to_excel, name='exportar_padronizacao_pagamento'),

    path('exportar/processo-digital/', exportar_processo_digital_to_excel, name='exportar_processo_digital'),



]
