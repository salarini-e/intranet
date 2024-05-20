from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import login_required
from chamados.models import Chamado, TipoChamado
from datetime import datetime, timedelta
@xframe_options_exempt
@login_required
def index(request):
    chamados = Chamado.objects.all()
    total_chamados = chamados.count()
    chamados_abertos_30dias = chamados.filter(dt_inclusao__gte=datetime.now() - timedelta(days=30)).count()
    chamados_fechados_30dias = chamados.filter(dt_execucao__gte=datetime.now() - timedelta(days=30)).count()
    media_diaria = total_chamados / 30
    data_atual = datetime.now()
    
    tres_meses_atras = data_atual - timedelta(days=90)
    count_abertos = chamados.filter(status='0').count()
    count_em_atendimento = chamados.filter(status='1').count()
    count_pendentes = chamados.filter(status='2').count()
    count_fechados = chamados.filter(status='3').count()

    # Preparando dados para o gráfico de barras
    tipos_chamados = TipoChamado.objects.all()
    chamados_por_tipo = [{'tipo': tipo.nome, 'quantidade': chamados.filter(tipo=tipo).count()} for tipo in tipos_chamados]

    data_atual = datetime.now()
    tres_meses_atras = data_atual - timedelta(days=90)

    semanas = []
    dados_abertos = []
    dados_fechados = []

    while tres_meses_atras < data_atual:
        semana_inicio = tres_meses_atras.strftime('%d/%m/%y')        
        label_semana = f'{semana_inicio}'

        chamados_semana = chamados.filter(dt_inclusao__gte=tres_meses_atras, dt_inclusao__lt=tres_meses_atras + timedelta(days=7))
        chamados_abertos_semana = chamados_semana.filter(status='0').count()
        chamados_fechados_semana = chamados_semana.filter(status='3').count()

        semanas.append(label_semana)
        dados_abertos.append(chamados_abertos_semana)
        dados_fechados.append(chamados_fechados_semana)

        tres_meses_atras += timedelta(days=7)


    context = {                
        'count_abertos': count_abertos,
        'count_em_atendimento': count_em_atendimento,
        'count_pendentes': count_pendentes,
        'count_fechados': count_fechados,
        'chamados_por_tipo': chamados_por_tipo,
        'semanas': semanas,
        'dados_abertos': dados_abertos,
        'dados_fechados': dados_fechados,
        'total_chamados': total_chamados,
        'chamados_abertos_30dias': chamados_abertos_30dias,
        'chamados_fechados_30dias': chamados_fechados_30dias,
        'media_diaria': media_diaria
    }
    return render(request, 'index.html', context)