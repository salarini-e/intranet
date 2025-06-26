from django.urls import path
from . import views
from .views.cadastro_de_almoxarifado import cadastro_de_almoxarifado, visualizar_cadastros_almoxarifado, exportar_cadastros_almoxarifado
from .views.avaliacao_el import avaliacao_sistemas_el
from .views.solicitacao_email_institucional import cadastro_solicitacao_email_institucional, visualizar_cadastros_solicitacao_email_institucional, exportar_cadastros_solicitacao_email_institucional
from .views.treinamento_tributario import exportar_decretos_portaria_atos_to_excel, cadastroTreinamentoTributarioEmissoresTaxas, cadastroTreinamentoTributarioContadores
from .views.padronizacao_pagamento import exportar_padronizacao_pagamento_to_excel, cadastro_padronizacao_pagamento, visualizar_padronizacao_pagamento
from .views.processo_digital import exportar_processo_digital_to_excel, cadastro_processo_digital, visualizar_processo_digital
from .views.sistema_GPI_contadores import cadastro_sistema_GPI_contadores, visualizar_sistema_GPI_contadores, exportar_sistema_GPI_contadores
from .views.treinamento_tributario import cadastroDecretos2024, visualizarDados_TT_Emissores, visualizarDados_TT_Contadores, visualizarDados_Decreto_Portaria_Atos_Prefeito, exportar_aulas_tributario_emissores_to_excel, exportar_aulas_tributario_contadores_to_excel
from .views.aulas_processo_digital import cadastroAulasProcessoDigial, inscricaoDecretosPortariaAtosPrefeito, visualizarDados_Aulas_Processo_Digital, exportar_aulas_processo_digital_to_excel, logCadastrosRepetidos

app_name = 'formfacil'
urlpatterns = [
    path('', views.index, name='index'),
    path('BA988BDD380A2EFD4E6CD29B225BA0C4/', views.IndicacaoComitePSP, name='indicacao_comite_psp'),
    path('webex/', views.webex, name='webex'),
    path('snct2024/', views.snct2024, name='snct2024'),
    path('snct2024/export', views.snct2024_export, name='snct2024_export'),
    path('habitacao/', views.form_augusto, name='form_augusto'),
    path('avaliacao-sistemas-el/', avaliacao_sistemas_el, name='avaliacao_sistemas_el'),
    
    path('cadastro-processo-digital', cadastroAulasProcessoDigial, name='cadastro-processo-digital'),
    path('visualizar/cadastro-processo-digital/', visualizarDados_Aulas_Processo_Digital, name='visualizar_aulas_processo_digital'),
    path('exportar/cadastro-processo-digital/', exportar_aulas_processo_digital_to_excel, name='exportar_aulas_processo_digital'),
    path('cadastros-repetidos/', logCadastrosRepetidos, name='cadastros_repetidos'),
    path('inscricao-decretos-portaria-atos-prefeito', inscricaoDecretosPortariaAtosPrefeito, name='inscricao-decretos-portaria-atos-prefeito'),
    
    path('cadastro-treinamento-tributario-emissores', cadastroTreinamentoTributarioEmissoresTaxas, name='cadastro-treinamento-tributario-emissores'),
    path('visualizar/cadastros-treinamento-tributario-emissores/', visualizarDados_TT_Emissores, name='cadastros-treinamento-tributario-emissores'),
    path('exportar/treinamento-tributario-emissores-taxas/', exportar_aulas_tributario_emissores_to_excel, name='exportar_treinamento_tributario_emissores_taxas'),
    path('inscricao-ato-prefeito', cadastroDecretos2024, name='inscricao-ato-prefeito'),
    
    path('cadastro-treinamento-tributario-contadores', cadastroTreinamentoTributarioContadores, name='cadastro-treinamento-tributario-contadores'),
    path('visualizar/cadastros-treinamento-tributario-contadores/', visualizarDados_TT_Contadores, name='cadastros-treinamento-tributario-contadores'),
    path('exportar/treinamento-tributario-contadores/', exportar_aulas_tributario_contadores_to_excel, name='exportar_treinamento_tributario_contadores'),
    path('visualizar/cadastros-decretos-portaria-atos-prefeito/', visualizarDados_Decreto_Portaria_Atos_Prefeito, name='cadastros-decretos-portaria-atos-prefeito'),
    path('exportar/decretos-portaria/', exportar_decretos_portaria_atos_to_excel, name='exportar_decretos_portaria'),
   
    path('cadastro-almoxarifado/', cadastro_de_almoxarifado, name='cadastro_almoxarifado'),
    path('visualizar/cadastros-almoxarifado/', visualizar_cadastros_almoxarifado, name='visualizar_cadastros_almoxarifado'),
    path('exportar/cadastros-almoxarifado/', exportar_cadastros_almoxarifado, name='exportar_cadastros_almoxarifado'),

    path('cadastro-solicitacao-email-institucional/', cadastro_solicitacao_email_institucional, name='cadastro_solicitacao_email_institucional'),
    path('visualizar/solicitacao-email-institucional/', visualizar_cadastros_solicitacao_email_institucional, name='visualizar_solicitacao_email_institucional'),
    path('exportar/solicitacao-email-institucional/', exportar_cadastros_solicitacao_email_institucional, name='exportar_solicitacao_email_institucional'),


    path('cadastro-processo-digital-2025/', cadastro_processo_digital, name='cadastro_processo_digital'),
    path('visualizar/processo-digital-2025/', visualizar_processo_digital, name='visualizar_processo_digital'),
    path('exportar/processo-digital/', exportar_processo_digital_to_excel, name='exportar_processo_digital'),

    path('cadastro-padronizacao-pagamento-2025/', cadastro_padronizacao_pagamento, name='cadastro_padronizacao_pagamento'),
    path('visualizar/padronizacao-pagamento-2025/', visualizar_padronizacao_pagamento, name='visualizar_padronizacao_pagamento'),
    path('exportar/padronizacao-pagamento/', exportar_padronizacao_pagamento_to_excel, name='exportar_padronizacao_pagamento'),


    path('cadastro-sistema-GPI-contadores/', cadastro_sistema_GPI_contadores, name='cadastro_sistema_GPI_contadores'),
    path('visualizar/cadastro-sistema-GPI-contadores/', visualizar_sistema_GPI_contadores, name='visualizar_sistema_GPI_contadores'),
    path('exportar/cadastro-sistema-GPI-contadores/', exportar_sistema_GPI_contadores, name='exportar_sistema_GPI_contadores'),
]
