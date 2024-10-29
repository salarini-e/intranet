from django.shortcuts import render, redirect
from .models import Equipamento
from .forms import EquipamentoForm
from barcode import Code128
from barcode.writer import ImageWriter
from io import BytesIO
import base64
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    equipamentos = Equipamento.objects.all()
    context = {
        'equipamentos': equipamentos,
    }
    return render(request, 'agricultura_codigobarras/index.html', context)

def ler_codido(request):
    if request.method == 'POST':
        codigo_barra = request.POST['codigo']
        try:
            equipamento = Equipamento.objects.get(codigo_barra=codigo_barra)
            return redirect('agricultura_codigobarras:visualizar_equipamento', codigo_barra=equipamento.codigo_barra)
        except:
            pass
    return render(request, 'agricultura_codigobarras/ler_codigo_de_barra.html')

@login_required
def cadastrar_equipamento(request):
    if request.method == 'POST':
        form = EquipamentoForm(request.POST)
        if form.is_valid():
            equipamento = form.save()

            # Gerar a imagem do código de barras com configurações ajustadas
            barcode_image = BytesIO()
            writer = ImageWriter()

            # Configurando altura e margens do código de barras
            options = {
                'module_width': 0.2,       # Largura de cada barra
                'module_height': 15.0,     # Altura das barras
                'font_size': 10,           # Tamanho da fonte dos números
                'text_distance': 4,        # Distância entre barras e números
                'quiet_zone': 10           # Espaço em branco ao redor
            }

            Code128(equipamento.codigo_barra, writer=writer).write(barcode_image, options)
            barcode_base64 = base64.b64encode(barcode_image.getvalue()).decode('utf-8')

            return render(request, 'agricultura_codigobarras/equipamento_sucesso.html', {
                'equipamento': equipamento,
                'barcode_base64': barcode_base64,
            })
    else:
        form = EquipamentoForm()
    
    return render(request, 'agricultura_codigobarras/equipamento_form.html', {'form': form})

@login_required
def visualizar_equipamento(request, codigo_barra):
    equipamento = Equipamento.objects.get(codigo_barra=codigo_barra)
    barcode_image = BytesIO()
    writer = ImageWriter()

    # Configurando altura e margens do código de barras
    options = {
        'module_width': 0.2,       # Largura de cada barra
        'module_height': 15.0,     # Altura das barras
        'font_size': 10,           # Tamanho da fonte dos números
        'text_distance': 5.5,        # Distância entre barras e números
        'quiet_zone': 10           # Espaço em branco ao redor
    }

    Code128(equipamento.codigo_barra, writer=writer).write(barcode_image, options)
    barcode_base64 = base64.b64encode(barcode_image.getvalue()).decode('utf-8')

    return render(request, 'agricultura_codigobarras/ler_codigo_de_barra_sucesso.html', {
        'equipamento': equipamento,
        'barcode_base64': barcode_base64,
    })

@login_required
def visualizar_equipamento_hash(request, hash):
    equipamento = Equipamento.objects.get(id=hash)
    barcode_image = BytesIO()
    writer = ImageWriter()

    # Configurando altura e margens do código de barras
    options = {
        'module_width': 0.2,       # Largura de cada barra
        'module_height': 15.0,     # Altura das barras
        'font_size': 10,           # Tamanho da fonte dos números
        'text_distance': 5.5,        # Distância entre barras e números
        'quiet_zone': 10           # Espaço em branco ao redor
    }

    Code128(equipamento.codigo_barra, writer=writer).write(barcode_image, options)
    barcode_base64 = base64.b64encode(barcode_image.getvalue()).decode('utf-8')

    return render(request, 'agricultura_codigobarras/visualizar_codigo_barras.html', {
        'equipamento': equipamento,
        'barcode_base64': barcode_base64,
    })

@login_required
def detalhes_imprimir_agricultura(request, hash):
    equipamento = Equipamento.objects.get(codigo_barra=hash)
    print('\n\n\n\n', equipamento.codigo_barra)
    barcode_image = BytesIO()
    writer = ImageWriter()
    options = {
        'module_width': 0.2,       # Largura de cada barra
        'module_height': 15.0,     # Altura das barras
        'font_size': 10,           # Tamanho da fonte dos números
        'text_distance': 5.5,      # Distância entre barras e números
        'quiet_zone': 10           # Espaço em branco ao redor
    }

    Code128(equipamento.codigo_barra, writer=writer).write(barcode_image, options)
    barcode_base64 = base64.b64encode(barcode_image.getvalue()).decode('utf-8')

    # Passar o código de barras em Base64 e o equipamento para o template
    context = {
       'equipamentos': equipamento,
       'barcode_base64': barcode_base64,  # Código de barras em Base64
    }
    return render(request, 'agricultura_codigobarras/detalhes-imprimir.html', context)