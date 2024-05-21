from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, HttpResponse
from .models import *

def sistemas(request):
    tipos = TipoSistema.objects.all().order_by('nome')
    return render(request, 'softwares/sistemas/index.html', context={'tipos': tipos})

def sistemas_listar(request, slug):
    tipo = get_object_or_404(TipoSistema, slug=slug)
    sistemas = Sistemas.objects.filter(tipo=tipo).order_by('nome')
    return render(request, 'softwares/sistemas/listar.html', context={'sistemas': sistemas, 'tipo': tipo})
    
def downloads(request):
    softwares = Downloads.objects.all().order_by('nome')
    tipos = TipoDownload.objects.all().order_by('nome')
    return render(request, 'softwares/downloads/index.html', context={'softwares': softwares, 'tipos': tipos})

def download_file(request, software_id):
    software = get_object_or_404(Downloads, id=software_id)
    file_path = software.arquivo.path
    return FileResponse(open(file_path, 'rb'), as_attachment=True)