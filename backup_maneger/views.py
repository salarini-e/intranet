import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
import subprocess
from django.contrib.auth.decorators import login_required

# dir_backups = '/home/eduardo/Documentos/Backups_db'
dir_backups = '/home/sistemas/db_backup'
log_file_path = f'{dir_backups}/backup_log.txt'

# Create your views here.
@login_required
def index(request):
    if not request.user.is_superuser:
        return HttpResponse("Apenas administradores podem acessar os backups.")
    
    list_folders = []
    logs = []

    # Read backup folders
    for folder in os.listdir(dir_backups):
        if os.path.isdir(os.path.join(dir_backups, folder)):
            list_folders.append(folder)
    list_folders.sort(reverse=True)

    # Read and process log file
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as log_file:
            log_lines = log_file.readlines()
            current_log = {}
            for line in log_lines:
                line = line.strip()
                if line.startswith('[') and ']' in line:
                    if current_log:
                        logs.append(current_log)    
                        current_log = {}
                    current_log['date'], current_log['status'] = line[1:].split('] ')
                elif line.startswith('Iniciado em:'):
                    current_log['start_time'] = line.split(': ', 1)[1]
                elif line.startswith('Backup finalizado em:') or line.startswith('Finalizado em:'):
                    current_log['end_time'] = line.split(': ', 1)[1]
                elif line.startswith('Falhas:'):
                    failures = line.split(': ', 1)[1]
                    current_log['failures'] = failures.split()  # Pre-split failures into a list
            if current_log:
                logs.append(current_log)
    
    from datetime import datetime
    logs.sort(key=lambda x: datetime.strptime(x['date'] + ' ' + x['start_time'], '%d/%m/%Y %H:%M:%S'), reverse=True)
    
    context = {
        'list_folders': list_folders,
        'logs': logs,
    }
    return render(request, 'backup_maneger/index.html', context)

@login_required
def list_db_files(request, subdir):
    if not request.user.is_superuser:
        return HttpResponse("Apenas administradores podem acessar os backups.")
    list_files = []
    path = os.path.join(dir_backups, subdir)
    
    if os.path.exists(path):
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                list_files.append(file)
        list_files.sort(reverse=True)
    
    context = {
        'list_files': list_files,
        'subdir': subdir,
    }
    return render(request, 'backup_maneger/list_db_files.html', context)
    
@login_required    
def download_file(request, subdir, file_name):
    if not request.user.is_superuser:
        return HttpResponse("Apenas administradores podem baixar os backups.")
    file_path = os.path.join(dir_backups, subdir, file_name)
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response
    
    return HttpResponse("File not found.")

@login_required    
def novo_backup(request):
    if not request.user.is_superuser:
        return HttpResponse("Apenas administradores podem disparar o backup.")
    # Caminho absoluto para o script
    # projeto_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    caminho_script = '/home/sistemas/intranet/site/intranet/mk_backup.sh'
    # Disparar o script sem esperar resposta
    try:
        subprocess.Popen(
            f'nohup bash {caminho_script} &',
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as e:
        return HttpResponse(f"Erro ao tentar disparar backup: {e}")



    return redirect('backup_maneger:index')
