from django.shortcuts import render
from .models import Registro

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Registro
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


@login_required
def index(request):
    agora = datetime.now()

    registros = Registro.objects.filter(user=request.user).order_by('data_registro', '-id')[:30]    
    registro_do_dia = Registro.objects.filter(user=request.user, data_registro=agora.date()).order_by('-id').first() if registros.exists() else None

    context = {
        'estado': 'entrada1' if registro_do_dia and registro_do_dia.entrada1 and not registro_do_dia.saida1 else 'saida1' if registro_do_dia and registro_do_dia.entrada1 and registro_do_dia.saida1 and not registro_do_dia.entrada2 else 'entrada2' if registro_do_dia and registro_do_dia.entrada1 and registro_do_dia.saida1 and registro_do_dia.entrada2 and not registro_do_dia.saida2 else 'saida2' if registro_do_dia and registro_do_dia.entrada1 and registro_do_dia.saida1 and registro_do_dia.entrada2 and registro_do_dia.saida2 else 'entrada1',
        'registro_do_dia': registro_do_dia,  # Registro específico do dia atual (ou None se não houver)
        'registros': registros        # Últimos 30 registros para exibição no histórico
    }
    return render(request, 'controle_de_ponto/index.html', context)

@staff_member_required
def painel(request):
    registros = Registro.objects.all().order_by('-data_registro','-id')
    context = {
        'registros': registros
    }
    return render(request, 'controle_de_ponto/painel.html', context)


@csrf_exempt
def api_registrar_ponto(request):
    if request.method == "POST":
        try:
            dados = json.loads(request.body)

            horario_registro = datetime.strptime(dados.get('registro'), '%H:%M:%S').time()
            data_registro = datetime.strptime(dados.get('data_registro'), '%d/%m/%Y').date()

            registro = Registro.objects.filter(user=request.user, data_registro=data_registro)
            if registro.exists():
                registro = registro.first()
                if registro.entrada1 is None:
                    registro.entrada1 = horario_registro
                    estado = 'entrada1'
                elif registro.saida1 is None:
                    registro.saida1 = horario_registro
                    estado = 'saida1'
                elif registro.entrada2 is None:
                    registro.entrada2 = horario_registro
                    estado = 'entrada2'                    
                elif registro.saida2 is None:
                    registro.saida2 = horario_registro
                    estado = 'saida2'
                else:
                    return JsonResponse({'success': False, 'message': 'Ponto do dia já finalizado.'}, status=400)
            else:
                registro = Registro(
                    user=request.user,
                    data_registro=data_registro,
                    entrada1=horario_registro
                )
                estado = 'entrada1'

            # Salvar o registro
            registro.save()
            return JsonResponse({
                'success': True,
                'message': 'Ponto registrado com sucesso.',
                'estado': estado,
                'hora': horario_registro.strftime('%H:%M'),
                'registro': {
                    'data': data_registro.strftime('%d/%m/%Y'),
                    'entrada1': registro.entrada1.strftime('%H:%M:%S') if registro.entrada1 else None,
                    'saida1': registro.saida1.strftime('%H:%M:%S') if registro.saida1 else None,
                    'entrada2': registro.entrada2.strftime('%H:%M:%S') if registro.entrada2 else None,
                    'saida2': registro.saida2.strftime('%H:%M:%S') if registro.saida2 else None,
                },
                'totalHoras': registro.total_horas()
            }, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Formato JSON inválido.'}, status=400)
        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Método não permitido.'}, status=405)
