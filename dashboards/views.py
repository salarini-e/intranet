from django.shortcuts import render
# from .graficos import (graf_total_atendimentos_realizados, graf_percentual_chamados_por_servico, graf_evolucao_chamados_por_tipo,
#                        graf_percentual_chamados_por_secretaria)

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from .graficos import *

from django.utils.timezone import localtime, now

@login_required
@staff_member_required
def index(request):
    # grafico_total = graf_total_atendimentos_realizados()
    total = Chamado.objects.all().count()
    total_resolvidos = Chamado.objects.filter(status='4').count()
    context = {
        'chamados_abertos': Chamado.objects.filter(status='0').count(),
        'chamados_pendentes': Chamado.objects.filter(status='2').count(),
        'chamados_criados_hoje': Chamado.chamados_criados_hoje(),
        'media_diaria': Chamado.calcular_media_diaria(),
        'chamados_criados_mes': Chamado.chamados_criados_mes(),
        'media_mensal': Chamado.calcular_media_mensal(),
        'total': total,
        'total_resolvidos': total_resolvidos,
        'total_pendentes': total - total_resolvidos,
        'eficiencia': str(int((total_resolvidos/(total))*100))+'%',
        # 'grafico_percentual': graf_percentual_chamados_por_servico(),
        # 'grafico_evolucao': graf_evolucao_chamados_por_tipo(),
        # 'grafico_secretaria': graf_percentual_chamados_por_secretaria()
        }
    return render(request, 'dashboards/index.html', context)

@login_required
@staff_member_required
def api_valores_dashboard(request):
    total = Chamado.objects.all().count()
    total_resolvidos = Chamado.objects.filter(status='4').count()
    data = {
        'chamados_abertos': Chamado.objects.filter(status='0').count(),
        'chamados_pendentes': Chamado.objects.filter(status='2').count(),
        'chamados_criados_hoje': Chamado.chamados_criados_hoje(),
        'media_diaria': Chamado.calcular_media_diaria(),
        'chamados_criados_mes': Chamado.chamados_criados_mes(),
        'media_mensal': Chamado.calcular_media_mensal(),
        'total': total,
        'total_resolvidos': total_resolvidos,
        'total_pendentes': total - total_resolvidos,
        'eficiencia': str(int((total_resolvidos/(total))*100))+'%',

    }
    return JsonResponse(data)

@login_required
@staff_member_required
def api_graf_total_atendimentos_realizados(request):
    data = dados_total_atendimentos_realizados()
    return JsonResponse(data)

@login_required
@staff_member_required
def api_graf_tipo_servico(request):
    data = dados_percentual_chamados_por_servico()
    return JsonResponse(data)

@login_required
@staff_member_required
def api_graf_evolucao_chamados(request):
    periodo = request.GET.get('periodo')
    data = dados_evolucao_chamados_internet(periodo)
    return JsonResponse(data)

@login_required
@staff_member_required
def api_graf_evolucao_chamados_impressora(request):
    periodo = request.GET.get('periodo')
    data = dados_evolucao_chamados_impressora(periodo)
    return JsonResponse(data)

@login_required
@staff_member_required
def api_graf_evolucao_chamados_computadores(request):
    periodo = request.GET.get('periodo')
    data = dados_evolucao_chamados_computadores(periodo)
    return JsonResponse(data)

@login_required
@staff_member_required
def api_graf_evolucao_chamados_sistemas(request):
    periodo = request.GET.get('periodo')
    data = dados_evolucao_chamados_sistemas(periodo)
    return JsonResponse(data)

@login_required
@staff_member_required
def api_graf_evolucao_chamados_telefonia(request):
    periodo = request.GET.get('periodo')
    data = dados_evolucao_chamados_telefonia(periodo)
    return JsonResponse(data)

@login_required
@staff_member_required
def api_graf_evolucao_atendimentos(request):
    data = dados_evolucao_atendimentos()
    return JsonResponse(data)

@login_required
@staff_member_required
def api_total_atendimentos_por_atendente(request):
    data = dados_total_atendimentos_por_atendente()
    return JsonResponse(data)

@login_required
@staff_member_required
def api_graf_chamados_secretaria(request):
    data = dados_chamados_por_secretaria()
    return JsonResponse(data)

