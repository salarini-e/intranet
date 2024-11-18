from django.shortcuts import render
# from .graficos import (graf_total_atendimentos_realizados, graf_percentual_chamados_por_servico, graf_evolucao_chamados_por_tipo,
#                        graf_percentual_chamados_por_secretaria)

from .graficos import *

def index(request):
    # grafico_total = graf_total_atendimentos_realizados()

    context = {
        'total': Chamado.objects.all().count(),
        'total_resolvidos': Chamado.objects.filter(status='4').count(),
        # 'grafico_percentual': graf_percentual_chamados_por_servico(),
        # 'grafico_evolucao': graf_evolucao_chamados_por_tipo(),
        # 'grafico_secretaria': graf_percentual_chamados_por_secretaria()
        }
    return render(request, 'dashboards/index.html', context)


from django.http import JsonResponse

def api_graf_total_atendimentos_realizados(request):
    data = dados_total_atendimentos_realizados()
    return JsonResponse(data)

def api_graf_tipo_servico(request):
    data = dados_percentual_chamados_por_servico()
    return JsonResponse(data)


def api_graf_evolucao_chamados(request):
    data = dados_evolucao_chamados_internet()
    return JsonResponse(data)

def api_graf_evolucao_chamados_impressora(request):
    data = dados_evolucao_chamados_impressora()
    return JsonResponse(data)

def api_graf_evolucao_chamados_computadores(request):
    data = dados_evolucao_chamados_computadores()
    return JsonResponse(data)

def api_graf_evolucao_chamados_sistemas(request):
    data = dados_evolucao_chamados_sistemas()
    return JsonResponse(data)

def api_graf_evolucao_chamados_telefonia(request):
    data = dados_evolucao_chamados_telefonia()
    return JsonResponse(data)

def api_graf_evolucao_atendimentos(request):
    data = dados_evolucao_atendimentos()
    return JsonResponse(data)

def api_graf_chamados_secretaria(request):
    data = dados_chamados_por_secretaria()
    return JsonResponse(data)

