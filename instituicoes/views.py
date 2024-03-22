from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib import messages

@login_required
def index(request):
    secretarias = Secretaria.objects.all()
    context = {
        'secretarias': secretarias
    }
    return render(request, 'instituicoes/index.html', context)

@login_required
def api(request):
    return JsonResponse({'status': 200})

@login_required
def criar_secretaria(request):
    if request.method == 'POST':
        form = SecretariaForm(request.POST)        
        if form.is_valid():
            secretaria = form.save()
            messages.success(request, f'Secretaria {secretaria.nome} cadastrada com sucesso!')
            return redirect('ins:index')            
    else:
        form = SecretariaForm()
    context = {
        'form': form,
        'model_name': 'Secretaria'
    }
    return render(request, 'instituicoes/form.html', context)

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