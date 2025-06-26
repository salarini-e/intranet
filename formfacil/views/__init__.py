from django.shortcuts import render
from ..forms import *
import pandas as pd
from django.http import HttpResponse
from ..models import FormSugestaoSemanaNacionalCET2024
from django.contrib.auth.decorators import login_required
import pytz

def IndicacaoComitePSP(request):
    if request.method == 'POST':
        form = FormIndicacaoComitePSPForm(request.POST)
        if form.is_valid():
            form.save()
            context = {
                'titulo': 'Formulário para indicação de representante no Comitê de Padronização dos Sistemas Públicos Municipais',    
                'subtitulo': 'Subsecretaria de TI',
                'mensagem': "<span class='text-success'>Formulário enviado com sucesso!</span> Estamos entusiasmados com a oportunidade de colaborar com você e aproveitar ao máximo sua valiosa contribuição."
            }
            return render(request, 'formfacil/formfacil_success.html', context)
    else:
        form = FormIndicacaoComitePSPForm()
    context = {
            'form': form,
            'titulo': 'Formulário para indicação de representante no Comitê de Padronização dos Sistemas Públicos Municipais',
            'subtitulo': 'Subsecretaria de TI',
            'mensagem': 'Agradecemos antecipadamente pela sua disposição em servir como representante no Comitê de Padronização dos Sistemas Públicos Municipais. Seu comprometimento e expertise serão fundamentais para impulsionar melhorias significativas em nossos sistemas.'
        }
    return render(request, 'formfacil/formfacil_form.html', context)


def webex(request):
    if request.method == 'POST':
        form = FormCadastroWebex(request.POST)
        if form.is_valid():
            form.save()
            context = {
                'titulo': 'Formulário de cadastro de usuário no WEBEX',    
                'subtitulo': 'Subsecretaria de TI',
                'mensagem': "<span class='text-success'><i class='fa-solid fa-circle-check me-2'></i>Formulário enviado com sucesso!</span>"
            }
            return render(request, 'formfacil/formfacil_success.html', context)
    else:
        form = FormCadastroWebex()
    context = {
            'form': form,
            'titulo': 'Formulário de cadastro de usuário no WEBEX',    
                'subtitulo': 'Subsecretaria de TI',
                'mensagem': "Formulário para levantamento de usuários cadastrados no sistema WEBEX."
        }
    return render(request, 'formfacil/formfacil_form.html', context)

def snct2024(request):
    if request.method == 'POST':
        form = FormSugestaoSemanaNacionalCET2024Form(request.POST)
        if form.is_valid():
            form.save()
            context = {
                'titulo': 'Formulário para sugestões de atividades para a Semana Nacional de Ciência e Tecnologia 2024',    
                'subtitulo': 'Secretaria Municipal de Ciência, Tecnologia, Inovação e Educação Profissionalizante Superior',
                'mensagem': "<span class='text-success'><i class='fa-solid fa-circle-check me-2'></i>Formulário enviado com sucesso!</span>"
            }
            return render(request, 'formfacil/formfacil_success.html', context)
    else:
        form = FormSugestaoSemanaNacionalCET2024Form()
        
    context = {
            'form': form,
            'titulo': 'Formulário para sugestões de atividades para a Semana Nacional de Ciência e Tecnologia 2024',    
                'subtitulo': 'Secretaria Municipal de Ciência, Tecnologia, Inovação e Educação Profissionalizante Superior',
                'mensagem': "Convidamos você a contribuir com sugestões de atividades para a Semana Nacional de Ciência e Tecnologia 2024. Sua participação é essencial para o sucesso do evento, cujo tema este ano é 'Biomas do Brasil: diversidade, saberes e tecnologia social. Agradecemos sua colaboração."
        }
    return render(request, 'formfacil/formfacil_form.html', context)


# @login_required
def snct2024_export(request):
    suggestions = FormSugestaoSemanaNacionalCET2024.objects.all()

    data = []
    for suggestion in suggestions:
        data.append({
            'Nome': suggestion.nome,
            'Sugestão': suggestion.sugestao,
            'Telefone': suggestion.telefone,
            'Email': suggestion.email,
             'Data de Inclusão': suggestion.dt_inclusao.astimezone(pytz.utc).replace(tzinfo=None), 
        })

    df = pd.DataFrame(data)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=sugestoes_snct2024.xlsx'

    df.to_excel(response, index=False, engine='openpyxl')

    return response

def index(request):
    context = {
        'registros':{
            'decretos_protaria_e_atos_do_prefeito_total': Inscricao_Decretos_Portaria_E_Atos_Do_Prefeito.objects.count(),
            'cadastros_almoxarifado_total': Cadastro_de_Almoxarifado.objects.count(),
            'solicitacao_email_institucional_total': SolicitacaoEmailInstitucional.objects.count(),
            'processo_digital_total': ProcessoDigitalInscricao.objects.count(),
            'padronizacao_pagamento_total': PadronizacaoPagamentoInscricao.objects.count(),
            'sistema_GPI_contadores_total': SistemaGPIparaContadores.objects.count()
        }
    }
    return render(request, 'formfacil/index.html', context)

def form_augusto(request):
    # formulario solicitado pel secretaria de habitação
    return render(request, 'formfacil/form_augusto.html', {})
