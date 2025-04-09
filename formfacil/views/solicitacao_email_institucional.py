from django.shortcuts import render
from ..forms import SolicitacaoEmailInstitucionalForm
from ..models import SolicitacaoEmailInstitucional
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from openpyxl import Workbook

@login_required
def cadastro_solicitacao_email_institucional(request):
    if request.method == 'POST':
        form = SolicitacaoEmailInstitucionalForm(request.POST)
        if form.is_valid():
            form.save()
            context = {
                'titulo': 'Cadastro de Solicitação de E-mail Institucional',
                'subtitulo': 'Gerenciamento de solicitações',
                'mensagem': "<span class='text-success'><i class='fa-solid fa-circle-check me-2'></i>Formulário enviado com sucesso!</span>"
            }
            return render(request, 'formfacil/formfacil_success.html', context)
    else:
        form = SolicitacaoEmailInstitucionalForm()

    context = {
        'form': form,
        'titulo': 'Cadastro de Solicitação de E-mail Institucional',
        'subtitulo': 'Subsecretaria de Tecnologia da Informação',
        'mensagem': 'Prezados, solicitamos o preenchimento do formulário abaixo para levantamento dos servidores que necessitarão de e-mail institucional. As informações serão utilizadas para a criação e organização das contas de e-mail oficiais da prefeitura. Importante: Evite abreviações no nome. O e-mail sugerido poderá ser ajustado conforme disponibilidade e padronização. Esse formulário deverá ser preenchido para cada servidor que precisará de e-mail institucional. Agradecemos pela colaboração!'
        
    }
    return render(request, 'formfacil/formfacil_form.html', context)

@login_required
def visualizar_cadastros_solicitacao_email_institucional(request):
    cadastros = SolicitacaoEmailInstitucional.objects.all()
    context = {
        'cadastros': cadastros,
        'titulo': 'Visualizar Solicitações de E-mail Institucional',
        'subtitulo': 'Lista de solicitações registradas'
    }
    return render(request, 'formfacil/visualizar_cadastros_email_institucional.html', context)

@login_required
def exportar_cadastros_solicitacao_email_institucional(request):
    cadastros = SolicitacaoEmailInstitucional.objects.all()

    # Criação do arquivo Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Solicitações de E-mail Institucional"

    # Cabeçalhos
    ws.append([
        "Nome", "Matrícula", "CPF", "Secretaria",
        "E-mail Institucional Sugerido", "Data de Registro"
    ])

    # Dados
    for cadastro in cadastros:
        ws.append([
            cadastro.nome,
            cadastro.matricula,
            cadastro.cpf,
            cadastro.secretaria,
            cadastro.email_institucional,
            cadastro.dt_registro.strftime('%d/%m/%Y %H:%M')
        ])

    # Configuração da resposta HTTP
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="solicitacoes_email_institucional.xlsx"'
    wb.save(response)
    return response
