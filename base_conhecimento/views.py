from django.shortcuts import render, get_object_or_404, redirect
from .models import Topico, Subtopico, Arquivo_GoogleDrive
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
def displayVideo(request, topico_id, subtopico_id):
    # Obter o tópico e o subtopico selecionados ou retornar um erro 404 se não existirem
    topico = get_object_or_404(Topico, id=topico_id, ativo=True)
    subtopico = get_object_or_404(Subtopico, id=subtopico_id, topico=topico)
    
    # Filtrar o vídeo associado ao subtopico
    video = Arquivo_GoogleDrive.objects.filter(subtopico=subtopico).first()

    context = {
        'topico': topico,
        'subtopico': subtopico,
        'video': video,
    }
    return render(request, 'base_conhecimento/display_video.html', context)

@login_required
def download_video(request, topico_id, subtopico_id):
    # Obter o tópico e o subtopico selecionados ou retornar um erro 404 se não existirem
    topico = get_object_or_404(Topico, id=topico_id, ativo=True)
    subtopico = get_object_or_404(Subtopico, id=subtopico_id, topico=topico)
    
    # Filtrar o vídeo associado ao subtopico
    video = get_object_or_404(Arquivo_GoogleDrive, subtopico=subtopico)
    
    # Extrair a URL do iframe HTML
    iframe_html = video.iframe
    download_url = extract_video_url_from_iframe(iframe_html)
    
    if not download_url:
        return HttpResponse("Não foi possível encontrar a URL do vídeo.", status=404)

    return redirect(download_url)


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