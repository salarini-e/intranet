from django.shortcuts import render, redirect
from .models import PlanejamentoAcao, Responsavel
from django.http import JsonResponse
# Create your views here.

def index(request):
    context = {
        'planejamento_acoes': PlanejamentoAcao.objects.all(),
    }
    return render(request, 'gestao_acao/index.html', context)

def index2(request):
    context = {
        'planejamento_acoes': PlanejamentoAcao.objects.all(),
    }
    return render(request, 'gestao_acao/index2.html', context)


def adicionar_acao(request):
    if request.method == 'POST':
        descricao = request.POST['descricao']
        data = request.POST['data']
        horario = request.POST['horario']
        local = request.POST['local']
        responsavel_id = request.POST['responsavel']
        status = request.POST['status']
        responsavel = Responsavel.objects.get(id=responsavel_id)
        PlanejamentoAcao.objects.create(
            descricao=descricao,
            data=data,
            horario=horario,
            local=local,
            responsavel=responsavel,
            status=status
        )
        return redirect('gestao_acao:index')
    context = {
        'responsaveis': Responsavel.objects.all(),
    }
    return render(request, 'gestao_acao/adicionar_acao.html', context)

import json
def atualizar_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        PlanejamentoAcao.objects.filter(id=data['id']).update(data=data['data'])
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    
