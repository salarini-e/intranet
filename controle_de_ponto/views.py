from django.shortcuts import render, redirect
from .models import Registro, Responsavel, Log_Alteracao
from instituicoes.models import Servidor, Setor
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

from .functions import obter_ip_cliente

from calendar import monthrange
from datetime import date

# Obtém os dias do mês
def obter_dias_do_mes(mes, ano):
    return [date(ano, mes, dia) for dia in range(1, monthrange(ano, mes)[1] + 1)]

@login_required
def index(request):
    agora = datetime.now()

    registros = Registro.objects.filter(user=request.user, data_registro__month=agora.month, data_registro__year=agora.year).order_by('-data_registro', '-id')
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
        dict_meses = { # Dicionário para converter o mês de número para nome
            '1': 'Janeiro', '2': 'Fevereiro', '3': 'Março', '4': 'Abril',
            '5': 'Maio', '6': 'Junho', '7': 'Julho', '8': 'Agosto',
            '9': 'Setembro', '10': 'Outubro', '11': 'Novembro', '12': 'Dezembro'
        }
        # Obtem os valores do formulário
        arquivo = request.POST.get("arquivo")
        mes = request.POST.get("mes")
        ano = request.POST.get("ano", now().year)  # Ano atual como padrão

        if not mes:
            return render(request, "erro.html", {'mensagem': 'DATA INVÁLIDA',"submensagem": "Por favor, selecione um mês."})
        elif arquivo == 'PDF':
            registros = Registro.objects.filter(
                data_registro__month=mes, data_registro__year=ano, 
                setor=responsavel.setor
            ).order_by('nome', 'data_registro')  # Ordenar por nome e data
            funcionarios = {}
            for registro in registros:
                if registro.nome not in funcionarios:
                    funcionarios[registro.nome] = []
                funcionarios[registro.nome].append(registro)

            context = {
                'mes': dict_meses[mes],
                'ano': ano,
                'dias_do_mes': obter_dias_do_mes(int(mes), int(ano)),
                'funcionarios': funcionarios  # Dicionário de funcionários com seus registros
            }
            return render(request, 'controle_de_ponto/relatorio_pdf.html', context)
        elif arquivo == 'Excel':
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

from django.http import JsonResponse

# @staff_member_required
@login_required
def api_detalhes_registro(request, matricula):    
    if not Responsavel.is_responsavel(request.user):        
        return render(request, "erro.html", {"mensagem": "Acesso negado."})
    
    agora = datetime.now()
    print(agora.month)
    print(agora.year)
    registros = Registro.objects.filter(matricula=matricula, data_registro__month=agora.month, data_registro__year=agora.year).order_by('-data_registro', '-id')
    response = []
    for registro in registros:
        total_horas = registro.total_horas()
        data = registro.data_registro.strftime('%d/%m/%Y')
        entrada1 = registro.entrada1.strftime('%H:%M') if registro.entrada1 else '-'
        saida1 = registro.saida1.strftime('%H:%M') if registro.saida1 else '-'
        entrada2 = registro.entrada2.strftime('%H:%M') if registro.entrada2 else '-'
        saida2 = registro.saida2.strftime('%H:%M') if registro.saida2 else '-'

        response.append({
            'data': data,
            'entrada1': entrada1,
            'saida1': saida1,
            'entrada2': entrada2,
            'saida2': saida2,
            'total_horas': str(total_horas)
        })

    return JsonResponse(list(response), safe=False)

@staff_member_required
def painel(request):
    if not Responsavel.is_responsavel(request.user):
        return render(request, "erro.html", {"mensagem": "Acesso negado."})

    responsavel = Responsavel.objects.get(user=request.user)
    
    # Filtrar servidores conforme o nível de responsabilidade
    if responsavel.geral:
        servidores = Servidor.objects.filter(
            user__is_active=True,
            setor__secretaria=responsavel.secretaria
        ).order_by('setor', 'nome')
    else:
        servidores = Servidor.objects.filter(
            setor=responsavel.setor, ativo=True
        ).order_by('setor', 'nome')
    
    anos_possiveis = (
        Registro.objects.filter(user=request.user)
        .values_list('data_registro__year', flat=True)
        .distinct()
        .order_by('data_registro__year')
    )
    
    context = {
        'servidores': servidores,
        'ano_atual': datetime.now().year,
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

            ip_cliente = obter_ip_cliente(request)
            if ip_cliente != '192.168.6.1':
                return JsonResponse({'success': False, 'message': 'Ponto somente dentro da rede da prefeitura.'}, status=403)

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
                    entrada1=horario_registro,
                    ip_inclusao=ip_cliente
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
from .forms import SearchServidorForm
from django.contrib import messages

def alocar_servidor(request):
    context = {}
    if not Responsavel.is_responsavel(request.user):
        return render(request, "erro.html", {"mensagem": "Acesso negado."})

    responsavel = Responsavel.objects.get(user=request.user)

    if request.method == "POST":
        form = SearchServidorForm(request.POST)
        form.fields["setor"].queryset = Setor.objects.filter(secretaria=responsavel.setor.secretaria)

        if form.is_valid():
            servidor = form.cleaned_data["servidor"]
            if responsavel.geral and form.cleaned_data["setor"]:    
                setor = form.cleaned_data["setor"]
                servidor.setor = setor
            else:
                servidor.setor = responsavel.setor
            servidor.save()

            context = {
                'mensagem': 'Usuário alocado com sucesso.',
                'submensagem': f'<strong>{servidor.nome} </strong>({servidor.matricula}) no setor: <br><strong>{servidor.setor}</strong>',  
            }
        else:
            context = {
                "mensagem": "Dados inválidos.",
                "submensagem": "Por favor, corrija os erros abaixo.",
                "form": form
            }
    else:
        form = SearchServidorForm()
        form.fields["setor"].queryset = Setor.objects.filter(secretaria=responsavel.secretaria)
    context["form"] = form
    context['responsavel'] = responsavel
    if responsavel.geral:
        context['servidores'] = Servidor.objects.filter(user__is_active=True,setor__secretaria=responsavel.secretaria).order_by('setor', 'nome')
    else:
        context['servidores'] = Servidor.objects.filter(user__is_active=True,setor=responsavel.setor).order_by('setor', 'nome')

    anos_possiveis = (
        Registro.objects.filter(user=request.user)
        .values_list('data_registro__year', flat=True)
        .distinct()
        .order_by('data_registro__year')
    )

    agora = datetime.now()
    context['mes_atual'] = agora.month
    context['ano_atual'] = agora.year
    context['anos_possiveis'] = anos_possiveis
    return render(request, "controle_de_ponto/alocar_servidor.html", context)

# def gambiarra(request):
#     registros = Registro.objects.all()
#     responsavel = Responsavel.objects.get(user=request.user)
#     for registro in registros:
#         registro.secretaria = responsavel.secretaria
#         registro.setor = responsavel.setor
#         registro.save()
#     return render(request, "erro.html", {"mensagem": "Feito.", "submensagem": "Gambiarra aplicada."})

from core.templatetags.custom_filters import acessoPonto
def menu_acertar_ponto(request):
    if not Responsavel.is_responsavel(request.user):
        return render(request, "erro.html", {"mensagem": "Acesso negado."})
    responsavel = Responsavel.objects.get(user=request.user)
    context = {
        'responsavel': responsavel,
    }
    if request.method == "POST":
        
        not_responsavel_geral = not responsavel.geral
        not_responsavel_secretaria = not responsavel.secretaria == Servidor.objects.filter(matricula = request.POST.get("matricula")).first().setor.secretaria
        not_responsavel_do_setor = not responsavel.setor == Servidor.objects.filter(matricula = request.POST.get("matricula")).first().setor
        
        if not_responsavel_geral and not_responsavel_secretaria:
                return render(request, "erro.html", {"mensagem": "Acesso negado.", "submensagem": "Você não tem autorização para alterar os registros desse servidor."})
        elif not_responsavel_do_setor:
            return render(request, "erro.html", {"mensagem": "Acesso negado.", "submensagem": "Você não tem autorização para alterar os registros desse servidor."})
        matricula = request.POST.get("matricula")
        data = request.POST.get("data")            
        registros = Registro.objects.filter(matricula=matricula, data_registro=data)
        if not registros.exists():
            messages.error(request, 'Nenhum registro encontrado.')
            return redirect('controle_de_ponto:menu_acertar_ponto')

        registro = registros.first()
        print(registro)
        context = {
            'data': datetime.strptime(data, '%Y-%m-%d').date(),
            'matricula': registro.matricula,
            'registros': [{
                'matricula': registro.matricula,
                'nome': registro.nome,
                'data': registro.data_registro.strftime('%d/%m/%Y'),
                'entrada1': f'<input type="time" name="entrada1" class="form-control" value="{registro.entrada1.strftime("%H:%M") if registro.entrada1 else ""}">',
                'saida1': f'<input type="time" name="saida1" class="form-control" value="{registro.saida1.strftime("%H:%M") if registro.saida1 else ""}">',
                'entrada2': f'<input type="time" name="entrada2" class="form-control" value="{registro.entrada2.strftime("%H:%M") if registro.entrada2 else ""}">',
                'saida2': f'<input type="time" name="saida2" class="form-control" value="{registro.saida2.strftime("%H:%M") if registro.saida2 else ""}">',
                'total_horas': str(registro.total_horas())
            }],    
            'responsavel': responsavel,        
        }
   
    return render(request, "controle_de_ponto/menu_acertar_ponto.html", context)

def menu_acertar_ponto_update(request):
    if not Responsavel.is_responsavel(request.user):
        return render(request, "erro.html", {"mensagem": "Acesso negado."})
    if request.method == "POST":
        try:
            matricula = request.POST.get("matricula")
            data = request.POST.get("data")
            entrada1 = request.POST.get("entrada1")
            saida1 = request.POST.get("saida1")
            entrada2 = request.POST.get("entrada2")
            saida2 = request.POST.get("saida2")

            registros = Registro.objects.filter(matricula=matricula, data_registro=data)
            log = Log_Alteracao(
                registro=registros.first(),            
                responsavel=Responsavel.objects.get(user=request.user),            
                entrada1_old=registros.first().entrada1,
                entrada1 = datetime.strptime(entrada1, '%H:%M').time() if entrada1 else None,
                saida1_old=registros.first().saida1,
                saida1 = datetime.strptime(saida1, '%H:%M').time() if saida1 else None,
                entrada2_old=registros.first().entrada2,
                entrada2 = datetime.strptime(entrada2, '%H:%M').time() if entrada2 else None,
                saida2_old=registros.first().saida2,            
                saida2 = datetime.strptime(saida2, '%H:%M').time() if saida2 else None,            
            )
            registro = registros.first()
            registro.entrada1 = datetime.strptime(entrada1, '%H:%M').time() if entrada1 else None
            registro.saida1 = datetime.strptime(saida1, '%H:%M').time() if saida1 else None
            registro.entrada2 = datetime.strptime(entrada2, '%H:%M').time() if entrada2 else None
            registro.saida2 = datetime.strptime(saida2, '%H:%M').time() if saida2 else None
            registro.save()
            log.save()
            messages.success(request, 'Registro atualizado com sucesso.')
            return redirect('controle_de_ponto:menu_acertar_ponto')
        except Exception as e:
            print(e)
            messages.error(request, f'Erro ao atualizar o registro: {e}')
            return redirect('controle_de_ponto:menu_acertar_ponto')
    return render(request, "erro.html", {"mensagem": "Método inválido."})