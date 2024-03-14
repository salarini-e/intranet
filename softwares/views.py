from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, HttpResponse

from .functions import store
from .models import *

def sistemas(request):

    store = store()
                 
    softwares = store.glob("/TI/DOWNLOADS_INTRANET/")
    softwares_ = []
    
    for software in softwares:        
        softwares_.append({'name': software[0].replace('  N', '').replace(' ', ''), 'file': f'{software[0]}', 'size': round((int(software[2])/(1024 * 1024)),1), 'date': software[3].strftime('%d/%m/%Y %H:%M:%S')})
    return render(request, 'softwares/sistemas/index.html', context={'softwares': softwares_})

def downloads(request):
    softwares = Downloads.objects.all()
    tipos = TipoDownload.objects.all()
    return render(request, 'softwares/downloads/index.html', context={'softwares': softwares, 'tipos': tipos})

def download_file(request, software_id):
    software = get_object_or_404(Downloads, id=software_id)
    file_path = software.arquivo.path
    return FileResponse(open(file_path, 'rb'), as_attachment=True)