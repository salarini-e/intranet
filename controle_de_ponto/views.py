from django.shortcuts import render
from .models import Registro, Responsavel

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Registro
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

import openpyxl
from openpyxl.styles import Alignment, Font
from django.utils.timezone import now


@login_required
def index(request):
    agora = datetime.now()

    registros = Registro.objects.filter(user=request.user).order_by('data_registro', '-id')[:30]    
    registro_do_dia = Registro.objects.filter(user=request.user, data_registro=agora.date()).order_by('-id').first() if registros.exists() else None

    context = {
        'estado': 'entrada1' if registro_do_dia and registro_do_dia.entrada1 and not registro_do_dia.saida1 else 'saida1' if registro_do_dia and registro_do_dia.entrada1 and registro_do_dia.saida1 and not registro_do_dia.entrada2 else 'entrada2' if registro_do_dia and registro_do_dia.entrada1 and registro_do_dia.saida1 and registro_do_dia.entrada2 and not registro_do_dia.saida2 else 'saida2' if registro_do_dia and registro_do_dia.entrada1 and registro_do_dia.saida1 and registro_do_dia.entrada2 and registro_do_dia.saida2 else 'entrada1',
        'registro_do_dia': registro_do_dia,  # Registro específico do dia atual (ou None se não houver)
        'registros': registros,        # Últimos 30 registros para exibição no histórico     
        'responsavel': Responsavel.is_responsavel(request.user),
    }
    return render(request, 'controle_de_ponto/index.html', context)


def exportar_excel(request):
    if not Responsavel.is_responsavel(request.user):
        return render(request, "erro.html", {"mensagem": "Acesso negado."})
    responsavel = Responsavel.objects.get(user=request.user)
    if request.method == "POST":
        # Obtem os valores do formulário
        mes = request.POST.get("mes")
        ano = request.POST.get("ano", now().year)  # Ano atual como padrão

        if not mes:
            return render(request, "erro.html", {"mensagem": "Por favor, selecione um mês."})

        # Filtra os registros pelo mês e ano
        if responsavel.geral:
            registros = Registro.objects.filter(
                secretaria=responsavel.secretaria,            
                data_registro__month=mes,
                data_registro__year=ano
            )
        else:
            registros = Registro.objects.filter(
                setor=responsavel.setor,            
                data_registro__month=mes,
                data_registro__year=ano
            )

        # Cria um workbook e uma worksheet
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = f"Registros {mes}-{ano}"

        # Cabeçalhos
        headers = [
            "Matrícula", "Nome", "Secretaria", "Setor", "Data do Registro",
            "Entrada 1", "Saída 1", "Entrada 2", "Saída 2", "Total de Horas"
        ]
        ws.append(headers)

        # Aplica estilos aos cabeçalhos
        for col in ws.iter_cols(min_row=1, max_row=1, min_col=1, max_col=len(headers)):
            for cell in col:
                cell.font = Font(bold=True)
                cell.alignment = Alignment(horizontal="center", vertical="center")

        # Adiciona os dados à planilha
        for registro in registros:
            ws.append([
                registro.matricula,
                registro.nome,
                registro.secretaria.nome if registro.secretaria else "",
                registro.setor.nome if registro.setor else "",
                registro.data_registro.strftime("%d/%m/%Y"),
                registro.entrada1.strftime("%H:%M") if registro.entrada1 else "",
                registro.saida1.strftime("%H:%M") if registro.saida1 else "",
                registro.entrada2.strftime("%H:%M") if registro.entrada2 else "",
                registro.saida2.strftime("%H:%M") if registro.saida2 else "",
                registro.total_horas(),
            ])

        # Ajusta o tamanho das colunas
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter  # Obtem a letra da coluna
            for cell in column:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass
            ws.column_dimensions[column_letter].width = max_length + 2

        # Cria o arquivo de resposta HTTP
        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = f'attachment; filename="registros_{mes}_{ano}.xlsx"'

        # Salva o workbook no response
        wb.save(response)
        return response

    return render(request, "erro.html", {"mensagem": "Método inválido."})


@staff_member_required
def painel(request):
    if not Responsavel.is_responsavel(request.user):
        return render(request, "erro.html", {"mensagem": "Acesso negado."})
    responsavel = Responsavel.objects.get(user=request.user)
    agora = datetime.now()
    if responsavel.geral:
        registros = Registro.objects.filter(secretaria=responsavel.secretaria).order_by('-data_registro','-id')
    else:
        registros = Registro.objects.filter(setor=responsavel.setor).order_by('-data_registro','-id')

    anos_possiveis = (
        Registro.objects.filter(user=request.user)
        .values_list('data_registro__year', flat=True)
        .distinct()
        .order_by('data_registro__year')
    )

    context = {
        'registros': registros,
        'ano_atual': agora.year,
        'anos_possiveis': anos_possiveis,
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
                    secretaria = request.servidor.setor.secretaria,
                    setor = request.servidor.setor,
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

def gambiarra(request):
    registros = Registro.objects.all()
    responsavel = Responsavel.objects.get(user=request.user)
    for registro in registros:
        registro.secretaria = responsavel.secretaria
        registro.setor = responsavel.setor
        registro.save()
    return render(request, "erro.html", {"mensagem": "Feito.", "submensagem": "Gambiarra aplicada."})