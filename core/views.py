from django.shortcuts import render, redirect
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import login_required
from chamados.models import Chamado, TipoChamado, chamadoSatisfacao, Atendente
from datetime import datetime, timedelta
from instituicoes.models import Servidor
from noticias.models import Carrousell, Noticias
from notificacoes.models import Notificacao

@login_required
def admin(request):
    print(request.user.id)
    if request.user.is_superuser and request.user.id == 5:
        return render(request, '403.html', status=403)
    return redirect('/dj-admin/')

@xframe_options_exempt
@login_required
def index(request):
    # chamados = Chamado.objects.all()
    # total_chamados = chamados.count()
    # chamados_abertos_30dias = chamados.filter(dt_inclusao__gte=datetime.now() - timedelta(days=30)).count()
    # chamados_fechados_30dias = chamados.filter(dt_execucao__gte=datetime.now() - timedelta(days=30)).count()
    # media_diaria = total_chamados / 30
    # data_atual = datetime.now()
    
    # tres_meses_atras = data_atual - timedelta(days=90)
    # count_abertos = chamados.filter(status='0').count()
    # count_em_atendimento = chamados.filter(status='1').count()
    # count_pendentes = chamados.filter(status='2').count()
    # count_fechados = chamados.filter(status='3').count()

    # # Preparando dados para o gráfico de barras
    # tipos_chamados = TipoChamado.objects.all()
    # chamados_por_tipo = [{'tipo': tipo.nome, 'quantidade': chamados.filter(tipo=tipo).count()} for tipo in tipos_chamados]

    # data_atual = datetime.now()
    # tres_meses_atras = data_atual - timedelta(days=90)

    # semanas = []
    # dados_abertos = []
    # dados_fechados = []

    # while tres_meses_atras < data_atual:
    #     semana_inicio = tres_meses_atras.strftime('%d/%m/%y')        
    #     label_semana = f'{semana_inicio}'

    #     chamados_semana = chamados.filter(dt_inclusao__gte=tres_meses_atras, dt_inclusao__lt=tres_meses_atras + timedelta(days=7))
    #     chamados_abertos_semana = chamados_semana.filter(status='0').count()
    #     chamados_fechados_semana = chamados_semana.filter(status='3').count()

    #     semanas.append(label_semana)
    #     dados_abertos.append(chamados_abertos_semana)
    #     dados_fechados.append(chamados_fechados_semana)

    #     tres_meses_atras += timedelta(days=7)

    atendente = Atendente.objects.filter(servidor=request.servidor)
    is_atendente = atendente.exists()
    if is_atendente:
        chamados_abertos_ou_pendentes = Chamado.objects.filter(
            profissional_designado=atendente.first(),
            status__in=['0', '2']
        ).order_by('dt_inclusao')
        
    context = {                
        'carrousel': Carrousell.objects.all(),
        'destaques': Noticias.objects.filter(destaque=True, ativo=True).order_by('-dt_inclusao')[:4],
        'noticias': Noticias.objects.filter(ativo=True).order_by('-dt_inclusao')[:15],
        # 'count_abertos': count_abertos,
        # 'count_em_atendimento': count_em_atendimento,
        # 'count_pendentes': count_pendentes,
        # 'count_fechados': count_fechados,
        # 'chamados_por_tipo': chamados_por_tipo,
        # 'semanas': semanas,
        # 'dados_abertos': dados_abertos,
        # 'dados_fechados': dados_fechados,
        # 'total_chamados': total_chamados,
        # 'chamados_abertos_30dias': chamados_abertos_30dias-chamados_fechados_30dias,
        # 'chamados_fechados_30dias': chamados_fechados_30dias,
        # 'media_diaria': "{:.1f}".format(media_diaria),
        'notifications': Notificacao.objects.filter(user=Servidor.objects.get(user=request.user)).order_by('-data')[:2],
        'chamados_abertos_ou_pendentes': chamados_abertos_ou_pendentes if is_atendente else None,
    }
    return render(request, 'index.html', context)

from django.http import JsonResponse
import json

def post_satisfacao(request):
    if request.method == 'POST':
        try:
            # Parse o corpo da requisição
            data = json.loads(request.body)
            print(data)
            # Obtenha o chamado correspondente
            chamado = Chamado.objects.get(id=data['chamado_id'])
            
            # Crie o registro de satisfação
            satisfacao = chamadoSatisfacao.objects.create(
                chamado=chamado,
                avaliacao=data.get('nivel_satisfacao'),
                avaliacao_justificativa=data.get('satisfacao_justificativa'),
                cordialidade=data.get('nivel_cordialidade'),
                cordialidade_justificativa=data.get('cordialidade_justificativa'),
                resolucao=data.get('satisfacao_resolucao'),
                receberia_novamente_o_tecnico=data.get('receberia_novamente_o_tecnico'),
                tempo_espera = data.get('tempo_espera'),
                comentario=data.get('comentario')
            )
            
            # Atualize o campo de pesquisa de satisfação no chamado
            chamado.pesquisa_satisfacao = True
            chamado.save()

            return JsonResponse({'status': 'success', 'message': 'Satisfação registrada com sucesso'})
        
        except Chamado.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Chamado não encontrado'}, status=404)
        
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'JSON inválido'}, status=400)
        
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)

def termos_de_uso(request):
    return render(request, 'termos_de_uso.html')

def swot(request):
    if request.user.is_superuser:
        return render(request, 'swot.html')
    return render(request, '403.html', status=403)

import requests
from django.http import JsonResponse
import xml.etree.ElementTree as ET
import json

def api_prefeitura_nf(request, ano, mes):
    url = f"https://novafriburgo-rj.portaltp.com.br/api/transparencia.asmx/json_servidores?ano={ano}&mes={mes}"
    try:
        response = requests.get(url)
        response.raise_for_status()

        # Parse do XML
        root = ET.fromstring(response.content)

        # O conteúdo que queremos está dentro da tag <string>
        json_text = root.text

        # Agora convertemos o texto JSON para objeto Python
        data = json.loads(json_text)

        return JsonResponse(data, safe=False)

    except ET.ParseError:
        return JsonResponse({'error': 'Resposta da API externa não está no formato XML válido'}, status=500)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Erro ao decodificar JSON dentro do XML'}, status=500)
    except requests.RequestException as e:
        return JsonResponse({'error': 'Erro ao buscar dados da API externa', 'details': str(e)}, status=500)
