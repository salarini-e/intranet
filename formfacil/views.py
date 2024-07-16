from django.shortcuts import render
from .forms import *
import pandas as pd
from django.http import HttpResponse
from .models import FormSugestaoSemanaNacionalCET2024
from django.contrib.auth.decorators import login_required

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


def Webex(request):
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

def Snct2024(request):
    if request.method == 'POST':
        form = FormSugestaoSemanaNacionalCET2024(request.POST)
        if form.is_valid():
            form.save()
            context = {
                'titulo': 'Formulário para sugestões de atividades para a Semana Nacional de Ciência e Tecnologia 2024',    
                'subtitulo': 'Secretaria Municipal de Ciência, Tecnologia, Inovação e Educação Profissionalizante Superior',
                'mensagem': "<span class='text-success'><i class='fa-solid fa-circle-check me-2'></i>Formulário enviado com sucesso!</span>"
            }
            return render(request, 'formfacil/formfacil_success.html', context)
    else:
        form = FormSugestaoSemanaNacionalCET2024()
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
            'Data de Inclusão': suggestion.dt_inclusao,
        })

    df = pd.DataFrame(data)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=sugestoes_snct2024.xlsx'

    df.to_excel(response, index=False, engine='openpyxl')

    return response
