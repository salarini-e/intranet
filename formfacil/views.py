from django.shortcuts import render
from .forms import *

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


def IndicacaoComitePSP(request):
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
                'mensagem': "<span class='text-success'>Formulário enviado com sucesso!</span>"
        }
    return render(request, 'formfacil/formfacil_form.html', context)

