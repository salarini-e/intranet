from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from .functions import store

def sistemas(request):

    store = store()
                 
    softwares = store.glob("/TI/DOWNLOADS_INTRANET/")
    softwares_ = []
    
    for software in softwares:        
        softwares_.append({'name': software[0].replace('  N', '').replace(' ', ''), 'file': f'{software[0]}', 'size': round((int(software[2])/(1024 * 1024)),1), 'date': software[3].strftime('%d/%m/%Y %H:%M:%S')})
    return render(request, 'softwares/sistemas/index.html', context={'softwares': softwares_})

def downloads(request):

    store = store()
                 
    softwares = store.glob("/TI/DOWNLOADS_INTRANET/")
    softwares_ = []
    
    for software in softwares:        
        softwares_.append({'name': software[0].replace('  N', '').replace(' ', ''), 'file': f'{software[0]}', 'size': round((int(software[2])/(1024 * 1024)),1), 'date': software[3].strftime('%d/%m/%Y %H:%M:%S')})
    return render(request, 'softwares/downloads/index.html', context={'softwares': softwares_})

def download_file(request, filename):
    print(filename)
    try:        
        store = store()
        file_path = f"/TI/DOWNLOADS_INTRANET/{filename}"
        # print(store.exists(file_path), file_path)
        if store.exists(file_path):
            with store.open(file_path, 'rb') as f:
                response = FileResponse(f)
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                return response
        else:
            return HttpResponse("File not found", status=404)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)