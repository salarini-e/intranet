from django.shortcuts import render
from .models import Notificacao
from django.http import JsonResponse
from instituicoes.models import Servidor
from django.utils.timesince import timesince
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json


def get_custom_timesince(notification_time):
    # Calculando a diferença de tempo
    diff = timezone.now() - notification_time

    # Menor que 1 hora - minutos
    if diff.total_seconds() < 3600:
        minutes = int(diff.total_seconds() // 60)
        return f'{minutes} minuto{"s" if minutes > 1 else ""}'

    # Menor que 1 dia - horas
    elif diff.total_seconds() < 86400:
        hours = int(diff.total_seconds() // 3600)
        return f'{hours} hora{"s" if hours > 1 else ""}'

    # Menor que 1 semana - dias
    elif diff.total_seconds() < 604800:
        days = int(diff.total_seconds() // 86400)
        return f'{days} dia{"s" if days > 1 else ""}'

    # Menor que 1 mês - semanas
    elif diff.total_seconds() < 2592000:
        weeks = int(diff.total_seconds() // 604800)
        return f'{weeks} semana{"s" if weeks > 1 else ""}'

    # Maior que 1 mês - meses
    else:
        months = int(diff.total_seconds() // 2592000)
        return f'{months} mês{"es" if months > 1 else ""}'
        
def checkNotificationNew(request):
    servidor = Servidor.objects.get(user=request.user)
    notificacoes = Notificacao.objects.filter(user=servidor, lida=False, new=True)
    if notificacoes.exists():
        notificacoes_json = []
        for notificacao in notificacoes:
            notificacao.new = False
            notificacao.save()
            notificacoes_ = {
                'id': notificacao.id,
                'icone': notificacao.icone,
                'msg': notificacao.msg,
                'link': notificacao.link,
                'data': get_custom_timesince(notificacao.data)
            }
            notificacoes_json.append(notificacoes_)
        data = {
            'status': True,
            'notificacoes': notificacoes_json
        }
    else:
        data = {
            'status': False
        }
    return JsonResponse(data)


@csrf_exempt
def marcar_como_lida(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ids = data.get('ids', [])
        
        # Marcar notificações como lidas
        Notificacao.objects.filter(id__in=ids).update(lida=True)
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)