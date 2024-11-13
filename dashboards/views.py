from django.shortcuts import render
from .graficos import (graf_total_atendimentos_realizados, graf_percentual_chamados_por_servico, graf_evolucao_chamados_por_tipo,
                       graf_percentual_chamados_por_secretaria)

def index(request):
    grafico_total = graf_total_atendimentos_realizados()

    context = {
        'grafico_total': grafico_total,
        'grafico_percentual': graf_percentual_chamados_por_servico(),
        'grafico_evolucao': graf_evolucao_chamados_por_tipo(),
        'grafico_secretaria': graf_percentual_chamados_por_secretaria()
        }
    return render(request, 'dashboards/index.html', context)
