from django.shortcuts import render
from ..forms import CadastroDeAlmoxarifadoForm
from ..models import Cadastro_de_Almoxarifado
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from openpyxl import Workbook

@login_required
def cadastro_de_almoxarifado(request):
    if request.method == 'POST':
        form = CadastroDeAlmoxarifadoForm(request.POST)
        if form.is_valid():
            form.save()
            context = {
                'titulo': 'Cadastro de Almoxarifado',
                'subtitulo': 'Gerenciamento de solicitações',
                'mensagem': "<span class='text-success'><i class='fa-solid fa-circle-check me-2'></i>Formulário enviado com sucesso!</span>"
            }
            return render(request, 'formfacil/formfacil_success.html', context)
    else:
        form = CadastroDeAlmoxarifadoForm()

    context = {
        'form': form,
        'titulo': 'Cadastro de Almoxarifado',
        'subtitulo': 'Gerenciamento de solicitações',
        'mensagem': ''
    }
    return render(request, 'formfacil/formfacil_form.html', context)

@login_required
def visualizar_cadastros_almoxarifado(request):
    cadastros = Cadastro_de_Almoxarifado.objects.all()
    context = {
        'cadastros': cadastros,
        'titulo': 'Visualizar Cadastros de Almoxarifado',
        'subtitulo': 'Lista de solicitações registradas'
    }
    return render(request, 'formfacil/visualizar_cadastros_almoxarifado.html', context)

@login_required
def exportar_cadastros_almoxarifado(request):
    cadastros = Cadastro_de_Almoxarifado.objects.all()

    # Criação do arquivo Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Cadastros Almoxarifado"

    # Cabeçalhos
    ws.append([
        "Nome do Requisitante", "Matrícula", "CPF", "Secretaria",
        "Autorizador", "Responsável pelo Material", "Data de Registro"
    ])

    # Dados
    for cadastro in cadastros:
        ws.append([
            cadastro.nome_requisitante,
            cadastro.matricula,
            cadastro.cpf,
            cadastro.secretaria,
            cadastro.autorizador,
            cadastro.responsavel_material,
            cadastro.dt_registro.strftime('%d/%m/%Y %H:%M')
        ])

    # Configuração da resposta HTTP
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="cadastros_almoxarifado.xlsx"'
    wb.save(response)
    return response
