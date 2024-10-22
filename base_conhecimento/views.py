from django.shortcuts import render, get_object_or_404, redirect
from .models import Topico, Subtopico, Arquivo_GoogleDrive, Arquivo_Texto, Arquivo_PDF
from django.contrib.auth.decorators import login_required
import requests
from django.http import StreamingHttpResponse, HttpResponse
import re

# Create your views here.
@login_required
def index(request):
    topicos = Topico.objects.filter(ativo= True)
    context = {
        'topicos': topicos
    }
    return render(request, 'base_conhecimento/index.html', context)

@login_required
def subtopicos(request, topico_id):
    # Obter o tópico selecionado ou retornar um erro 404 se não existir
    topico = get_object_or_404(Topico, id=topico_id, ativo=True)
    
    # Filtrar os subtopicos associados ao tópico selecionado
    subtopicos = Subtopico.objects.filter(topico_id=topico)
    
    context = {
        'topico': topico,
        'subtopicos': subtopicos
    }
    return render(request, 'base_conhecimento/subtopicos.html', context)

@login_required
def display(request, topico_id, subtopico_id):
    # Obter o tópico e o subtopico selecionados ou retornar um erro 404 se não existirem
    topico = get_object_or_404(Topico, id=topico_id, ativo=True)
    subtopico = get_object_or_404(Subtopico, id=subtopico_id, topico=topico)
    
    tipo_subtopico = subtopico.tipo

    if(tipo_subtopico == 'ytb'):
        # Filtrar o vídeo associado ao subtopico
        video = Arquivo_GoogleDrive.objects.filter(subtopico=subtopico).first()

        iframe_html = video.iframe
        download_url = extract_video_url_from_iframe(iframe_html)

        context = {
            'topico': topico,
            'subtopico': subtopico,
            'video': video,
            'download_url': download_url
        }
        return render(request, 'base_conhecimento/display_video.html', context)
    elif(tipo_subtopico== 'txt'):
        texto = Arquivo_Texto.objects.filter(subtopico=subtopico).first()
        
        if texto:
            # Substituir múltiplos espaços por uma quebra de linha
            texto_formatado = re.sub(r'\s{2,}', '<br><br>', texto.texto)
            context = {
            'topico': topico,
            'subtopico': subtopico,
            'texto': texto_formatado,
        }
        return render(request, 'base_conhecimento/display_texto.html', context)
    elif (tipo_subtopico=='pdf'):
        pdf = Arquivo_PDF.objects.filter(subtopico=subtopico).first()
        context = {
                'topico': topico,
                'subtopico': subtopico,
                'pdf': pdf,
        }
        return render(request, 'base_conhecimento/display_pdf.html', context)

def extract_video_url_from_iframe(iframe_html):
    """
    Extrai a URL do vídeo do HTML do iframe e converte o link de preview
    do Google Drive para um link de download direto.
    """
    match = re.search(r'src="([^"]+)"', iframe_html)
    if match:
        preview_url = match.group(1)
        return convert_to_download_url(preview_url)
    return None

def convert_to_download_url(preview_url):
    """
    Converte a URL de preview do Google Drive para um link de download direto.
    """
    # Extraia o ID do arquivo do URL de preview
    file_id = re.search(r'/d/([^/]+)/', preview_url)
    if file_id:
        return f'https://drive.google.com/uc?export=download&id={file_id.group(1)}'
    return None

    