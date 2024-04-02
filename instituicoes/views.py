from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib import messages
from .functions.scrapping import df_servidores, save_servidores

from .models import Meta_Servidores
from datetime import datetime
import pandas as pd

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
            secretaria.user_inclusao = request.user
            secretaria.save()
            messages.success(request, f'Secretaria {secretaria.nome} cadastrada com sucesso!')
            return redirect('ins:index')            
    else:
        form = SecretariaForm(initial={'user_inclusao': request.user.id})
    context = {
        'form': form,
        'title': 'Adicionar secretaria',
        'url_back': redirect('ins:index').url
    }
    return render(request, 'instituicoes/form.html', context)

@login_required
def editar_secretaria(request, id):
    secretaria = Secretaria.objects.get(id=id)
    if request.method == 'POST':
        form = SecretariaForm(request.POST, instance=secretaria)        
        if form.is_valid():
            secretaria = form.save()
            secretaria.user_inclusao = request.user
            secretaria.save()
            messages.success(request, f'Secretaria {secretaria.nome} cadastrada com sucesso!')
            return redirect('ins:index')            
    else:
        form = SecretariaForm(instance=secretaria)
    context = {
        'form': form,
        'title': 'Editar secretaria'
    }
    return render(request, 'instituicoes/form.html', context)

@login_required
def setores(request, id):    
    secretaria = Secretaria.objects.get(id=id)
    setores = Setor.objects.filter(secretaria = secretaria)
    context = {        
        'secretaria': secretaria,
        'setores': setores
    }
    return render(request, 'instituicoes/setores.html', context)

@login_required
def criar_setor(request, id):
    secretaria = Secretaria.objects.get(id=id)
    if request.method == 'POST':
        form = SetorForm(request.POST)        
        if form.is_valid():
            setor = form.save()
            setor.user_inclusao = request.user
            setor.save()
            messages.success(request, f'Setor {setor.nome} cadastrada com sucesso!')
            return redirect('ins:setores', id=secretaria.id)            
    else:
        form = SetorForm(initial={'secretaria': secretaria.id ,'user_inclusao': request.user.id})
    context = {
        'form': form,
        'secretaria': secretaria,
        'title': f'Adicionar setor a {secretaria.apelido}',
        'url_back': redirect('ins:setores', id=secretaria.id).url
    }
    return render(request, 'instituicoes/form.html', context)

@login_required
def editar_setor(request, id):
    setor = Setor.objects.get(id=id)
    secretaria = setor.secretaria
    if request.method == 'POST':
        form = SetorForm(request.POST, instance=setor)        
        if form.is_valid():
            setor = form.save()
            setor.user_inclusao = request.user
            setor.save()
            messages.success(request, f'Setor {setor.nome} cadastrada com sucesso!')
            return redirect('ins:setores')            
    else:
        form = SetorForm(instance=setor)
    context = {
        'form': form,
        'title': f'Editar {setor.nome}',
        'url_back': redirect('ins:setores', id=secretaria.id).url
    }
    return render(request, 'instituicoes/form.html', context)

@login_required
def adicionar_servidor(request, id, id_setor):
    setor = Setor.objects.get(id=id_setor)
    if request.method == 'POST':
        form = ServidorForm(request.POST)        
        if form.is_valid():
            servidor = form.save()
            servidor.setor = setor
            servidor.user = form.create_user()
            servidor.user_inclusao = request.user
            servidor.save()
            messages.success(request, f'Servidor {servidor.nome} cadastrada com sucesso!')
            return redirect('ins:setores', setor.secretaria.id)            
    else:
        form = ServidorForm(initial={'setor': setor.id, 'user_inclusao': request.user.id})
    context = {
        'form': form,
        'title': 'Adicionar servidor',
        'url_back': redirect('ins:setores', setor.secretaria.id).url
    }
    return render(request, 'instituicoes/form.html', context)

@login_required 
def getSetores(request, id):
    setores = Setor.objects.filter(secretaria=id).values('id', 'nome')
    return JsonResponse({'setores': list(setores)})

@login_required
def get_servidores_from_site(request):
   
    arquivo_excel = '/home/eduardo/Documentos/Github/intranet/grdData.xlsx'    
    df = pd.read_excel(arquivo_excel)
    
    for index, row in df.iterrows():

        nome = row['Nome']
        matricula = row['Matricula']
        lotacao = row['Lotacao']
        cpf = row['CPF']
        

        if Meta_Servidores.objects.filter(matricula=matricula).exists():
            continue

        
        servidor = Meta_Servidores(
            nome=nome,
            matricula=matricula,
            secretaria=lotacao,
            cpf=cpf,
            dt_inclusao=datetime.now()  # Data de inclusão definida como o momento atual
        )
                
        servidor.save()

    return HttpResponse("Dados importados com sucesso!")