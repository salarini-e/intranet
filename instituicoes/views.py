from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import *

@login_required
def api(request):
    return JsonResponse({'status': 200})

@login_required
def criar_instituicao(request):
    if request.method == 'POST':
        print(request.POST)
        return JsonResponse({'result': True})
    else:
        return JsonResponse({'result': False})

@login_required    
def criar_setor(request):
    if request.method == 'POST':
        print(request.POST)
        return JsonResponse({'status': 200})
    else:
        return JsonResponse({'status': 403})
    
@login_required 
def getSetores(request, id):
    setores = Setor.objects.filter(secretaria=id).values('id', 'nome')
    return JsonResponse({'setores': list(setores)})