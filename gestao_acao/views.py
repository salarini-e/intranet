from django.shortcuts import render, redirect
from .models import PlanejamentoAcao, Responsavel
from django.http import JsonResponse
from projetos.models import Demandas
from django.contrib.auth.decorators import login_required
from .forms import PlanejamentoAcaoForm

@login_required
def index(request):
    context = {
        'planejamento_acoes': PlanejamentoAcao.objects.filter(user_inclusao=request.user).order_by('data', 'horario'),
    }
    return render(request, 'gestao_acao/index.html', context)


# def index2(request):
#     context = {
#         'planejamento_acoes': PlanejamentoAcao.objects.all(),
#     }
#     return render(request, 'gestao_acao/index2.html', context)

@login_required
def adicionar_acao(request):
    if request.method == 'POST':
        form = PlanejamentoAcaoForm(request.POST)
        if form.is_valid():
            acao = form.save(commit=False)
            acao.user_inclusao = request.user
            acao.save()
            Demandas.objects.create(
                nome=acao.descricao,
                descricao=f'{acao.horario} {acao.local} - Ação planejada e atribuída a ' + acao.responsavel.nome,
                referencia='p',
                data_inicio=acao.data,
                atribuicao=acao.responsavel,
            )
            return redirect('gestao_acao:index')
    else:
        form = PlanejamentoAcaoForm()
    context = {
        'form': form,
    }
    return render(request, 'gestao_acao/adicionar_acao.html', context)

import json
@login_required
def atualizar_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            acao = PlanejamentoAcao.objects.get(id=data['id'])
            acao.data = data['data']
            acao.save()
            return JsonResponse({'status': 'success', 'data': acao.data})
        except PlanejamentoAcao.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Ação não encontrada'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
def excluir_acao(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        PlanejamentoAcao.objects.filter(id=data['id']).delete()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
def atualizar_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        PlanejamentoAcao.objects.filter(id=data['id']).update(status=data['status'])
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

