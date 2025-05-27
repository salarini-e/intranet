from django.shortcuts import render
from ..forms import PadronizacaoPagamentoInscricaoForm
from ..models import PadronizacaoPagamentoInscricao

def cadastro_padronizacao_pagamento(request):
    if request.method == 'POST':
        form = PadronizacaoPagamentoInscricaoForm(request.POST)
        if form.is_valid():
            if PadronizacaoPagamentoInscricao.objects.filter(turma=form.cleaned_data['turma']).count() >= 28:
                context = {
                    'form': form,
                    'titulo': 'Padronização do Processo de Pagamento',
                    'subtitulo': 'Inscrição',
                    'mensagem': '<span class="text-danger">Limite de vagas atingido para esta turma.</span>'
                }
                return render(request, 'formfacil/formfacil_form.html', context)
            form.save()
            context = {
                'titulo': 'Padronização do Processo de Pagamento',
                'subtitulo': 'Inscrição',
                'mensagem': "<span class='text-success'><i class='fa-solid fa-circle-check me-2'></i>Formulário enviado com sucesso!</span>"
            }
            return render(request, 'formfacil/formfacil_success.html', context)
    else:
        form = PadronizacaoPagamentoInscricaoForm()
    context = {
        'form': form,
        'titulo': 'Padronização do Processo de Pagamento',
        'subtitulo': 'Inscrição',
        'mensagem': (
            'Data: 04/06/2025<br>'
            'Turma 1: 10h às 12h<br>'
            'Turma 2: 14h às 16h<br>'
            'Local: Sala de treinamento da secretaria de ciência e tecnologia, inovação e desenvolvimento econômico - Av. Alberto Braune, 223 - 2º andar.'
        )
    }
    return render(request, 'formfacil/formfacil_form.html', context)

def visualizar_padronizacao_pagamento(request):
    turmas = dict(PadronizacaoPagamentoInscricao.TURMAS)
    registros = {turma: PadronizacaoPagamentoInscricao.objects.filter(turma=key) for key, turma in turmas.items()}
    return render(request, 'formfacil/visualizar_padronizacao_pagamento.html', {'registros': registros, 'turmas': turmas})
