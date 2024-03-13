from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

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