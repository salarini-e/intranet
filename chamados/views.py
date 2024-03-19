from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.db import connection
from django.urls import reverse
from .forms import *
from .models import *
from django.http import JsonResponse
from django.core.serializers import serialize
import websockets
import asyncio
import json

# Create your views here

@login_required
def mainPage(request):
    tipos = Tipo.objects.all()    
    try:
        atendente = Atendente.objects.get(user=request.user)
    except:
        atendente = False
            
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            chamados = filtraChamado(request, form, atendente)   
    else:
        form = SearchForm()    
        
        if atendente:
            chamados = Chamado.objects.all()
        else:
            servidor = Servidor.objects.get(user=request.user)
            chamados = Chamado.objects.filter(requisitante=servidor)
            
    chamados = chamados.order_by('-numero')
    
    context = {
        'chamados': chamados,
        'form': form,
        'tipos': tipos,
        'atendente': atendente
    }
    
    return render(request, '_pages_/mainPage.html', context)

@login_required
def abrirChamado(request, tipo):
    servidor = Servidor.objects.get(user=request.user)
    form = Chamado_Form()
    tipo = Tipo.objects.get(sigla=tipo)
    
    if request.method=='POST':
        form = Chamado_Form(request.POST, request.FILES)
        if form.is_valid():
            chamado=form.save(commit=False)
            chamado.requisitante = servidor
            chamado.secretaria = chamado.setor.secretaria
            # chamado.setor = servidor.setor
            chamado.tipo = tipo
            chamado.setNumero()
            chamado.notificaAtendente()
            
            try:
                asyncio.run(send_message(chamado))
            except:
                pass
            
            return render(request, '_pages_/chamado.html', {'chamado': chamado})
    
    context={
        'form': form,
        'servidor': servidor,
    }
            
    
    return render(request, '_pages_/abrirChamado.html', context)

@login_required
def abrirChamadoInternet(request):
    servidor = Servidor.objects.get(user=request.user)
    form = OSInternet_Form()
    tipo = Tipo.objects.get(sigla='INT')
    
    if request.method=='POST':
        form = OSInternet_Form(request.POST, request.FILES)
        if form.is_valid():
            chamado=form.save(commit=False)
            chamado.requisitante = servidor
            chamado.secretaria = chamado.setor.secretaria
            # chamado.setor = servidor.setor
            chamado.tipo = tipo
            chamado.setNumero()
            chamado.notificaAtendente()
            
            asyncio.run(send_message(chamado))
            
            return render(request, '_pages_/chamado.html', {'chamado': chamado})
    
    context={
        'form': form,
        'servidor': servidor,
    }
    return render(request, '_pages_/abrirChamado.html', context)
        
@login_required
def abrirChamadoSistema(request):
    servidor = Servidor.objects.get(user=request.user)
    form = OSSistema_Form()
    tipo = Tipo.objects.get(sigla='SGP')
    
    if request.method=='POST':
        form = OSSistema_Form(request.POST, request.FILES)
        if form.is_valid():
            chamado=form.save(commit=False)
            chamado.requisitante = servidor
            chamado.secretaria = chamado.setor.secretaria
            # chamado.setor = servidor.setor
            chamado.tipo = tipo
            chamado.setNumero()
            chamado.notificaAtendente()
            
            asyncio.run(send_message(chamado))
            
            return render(request, '_pages_/chamado.html', {'chamado': chamado})
    
    context={
        'form': form,
        'servidor': servidor,
    }
    
    return render(request, '_pages_/abrirChamado.html', context)
            
@login_required
def abrirChamadoImpressora(request):
    servidor = Servidor.objects.get(user=request.user)
    form = OSImpressora_Form()
    tipo = Tipo.objects.get(sigla='IMP')
    
    if request.method=='POST':
        form = OSImpressora_Form(request.POST, request.FILES)
        if form.is_valid():
            chamado=form.save(commit=False)
            chamado.requisitante = servidor
            chamado.secretaria = chamado.setor.secretaria
            # chamado.setor = servidor.setor
            chamado.tipo = tipo
            chamado.setNumero()
            chamado.notificaAtendente()
            
            asyncio.run(send_message(chamado))
            
            return render(request, '_pages_/chamado.html', {'chamado': chamado})
    
    context={
        'form': form,
        'servidor': servidor,
    }
    
    return render(request, '_pages_/abrirChamado.html', context)
            
    
@login_required
def chamado(request, idChamado):
    chamado = Chamado.objects.get(id=idChamado)

    try:
        chamadoInt = OSInternet.objects.get(id=idChamado)
    except OSInternet.DoesNotExist:
        chamadoInt = None
    try:
        chamadoSis = OSSistema.objects.get(id=idChamado)
    except OSSistema.DoesNotExist:
        chamadoSis = None
    try:
        chamadoImp = OSImpressora.objects.get(id=idChamado)
    except OSImpressora.DoesNotExist:
        chamadoImp = None
    
    atendentes = Atendente.objects.all()
    comentarios = Comentario.objects.filter(chamado=chamado).order_by('dataHora')

    context = {
        'chamado': chamado,
        'chamadoInt': chamadoInt,
        'chamadoImp': chamadoImp,
        'chamadoSis': chamadoSis,
        'atendentes': atendentes,
        'comentarios': comentarios,
    }

    return render(request, '_pages_/chamado.html', context)

def loginView(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username = username, password = password)
                if user is not None:
                    login(request, user)
                    return redirect('/')
        else:
            form =  AuthenticationForm()
        
        return render(request, '_pages_/login.html', {'form': form})
    
def cadastroView(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            formUser = UserCreationForm(data=request.POST)
            formServidor = ServidorForm(data=request.POST)
            if formUser.is_valid() and formServidor.is_valid():
                print('formulário válido')
                user = formUser.save()
                servidor = formServidor.save(commit=False)
                servidor.user = user
                user.email = servidor.email
                user.save()
                servidor.save()
                login(request, user)
                return redirect('/')
                
        else:
            formUser = UserCreationForm()
            formServidor = ServidorForm()
               
        return render(request, '_pages_/cadastro.html', {'formUser': formUser, 'formServidor': formServidor})
    
@login_required
def sairFunc(request):
    logout(request)
    return redirect('/login/')
    
@login_required
def filtraChamado(request, form, atendente):
    
    if not atendente:
        servidor = Servidor.objects.get(user=request.user)
    else:
        servidor = False
    
    numero = form.cleaned_data['numero']
    assunto = form.cleaned_data['assunto']
    requisitante = form.cleaned_data['requisitante']
    tipo = form.cleaned_data['tipo']
    prioridade = form.cleaned_data['prioridade']
    setor = form.cleaned_data['setor']
    dataInicio = form.cleaned_data['dataInicio']
    dataFim = form.cleaned_data['dataFim']
    status = form.cleaned_data['status']
    
    
    sql = "SELECT id FROM chamados_chamado WHERE "
    
    params = []

    if status:
        if status != '3':
            sql += " status LIKE %s"
            params.append(f'%{status}%')
        else:
            sql += " status IS NOT NULL"
    if numero:
        sql += " AND numero LIKE %s"
        params.append(f'%{numero}%')
    if assunto:
        sql += " AND assunto LIKE %s"
        params.append(f'%{assunto}%')
    if requisitante:
        sql += " AND requisitante_id LIKE %s"
        params.append(f'%{requisitante}%')
    if tipo:
        sql += " AND tipo_id LIKE %s"
        params.append(f'%{tipo}%')
    if prioridade:
        if prioridade != '3':
            sql += "AND prioridade LIKE %s"
            params.append(f'%{prioridade}%')
        else:
            sql += "AND prioridade IS NOT NULL"
    if setor:
        sql += " AND setor_id LIKE %s"
        params.append(f'%{setor}%')


    
    if dataInicio and dataFim:
        sql+= " AND DATE(dataAbertura) BETWEEN %s AND %s"
        params.append(dataInicio)
        params.append(dataFim)
    elif dataInicio:
        sql+= " AND DATE(dataAbertura) >= %s"
        params.append(dataInicio)
    elif dataFim:
        sql+= " AND DATE(dataAbertura) <= %s"
        params.append(dataFim)
        
    if servidor:
        sql+= " AND requisitante_id LIKE %s"
        params.append(servidor.id)
        
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        query = cursor.fetchall()
    
    print(sql)
    print(dataInicio)
    print(dataFim)
    
    idList = [idTuple[0] for idTuple in query]
    chamados = Chamado.objects.filter(id__in=idList)
    

        
    return chamados
    

def atualizaChamado(request, idChamado):
    chamado = Chamado.objects.get(id=idChamado)
    if request.method == 'POST':
        newPrioridade = request.POST.get('prioridade')
        newStatus = request.POST.get('status')
        
        newAtendente = request.POST.get('atendente')
        try:
            newAtendente = Atendente.objects.get(id=newAtendente)
        except:
            newAtendente = None
        
        chamado.prioridade = newPrioridade
        chamado.status = newStatus
        chamado.atendente = newAtendente
        
        chamado.save()
        
    return redirect(reverse('chamados:chamado', args=[chamado.id]))


@login_required
def editaChamado(request, idChamado):
    chamado = Chamado.objects.get(id=idChamado)
    
    if request.method == 'POST':
        form = editaChamadoForm(request.POST, instance=chamado)
        if form.is_valid():
            form.save()
            return redirect(reverse('chamados:chamado', args=[chamado.id]))
    else:
        form = editaChamadoForm(instance=chamado)        
    
    return render(request, '_pages_/editaChamado.html', {'form': form, 'chamado': chamado})


@login_required
def indicadores(request):
    setores = Setor.objects.all()
    secretarias = Secretaria.objects.all()

    if request.method == 'POST':
        selectSetor = request.POST.get('setor')
        selectSecretaria = request.POST.get('secretaria')
        setoresSearch = Setor.objects.filter(nome=selectSetor)
        secretariasSearch = Secretaria.objects.filter(nome=selectSecretaria)
    else:
        secretariasSearch = secretarias
        setoresSearch = setores

    context = {
        'setores': setores,
        'secretarias': secretarias,
        'setoresSearch': setoresSearch,
        'secretariasSearch': secretariasSearch
    }
    return render(request, '_pages_/indicadores.html', context)

@login_required
def atendentes(request):
    atendentes = Atendente.objects.all()
    servidores = Servidor.objects.all()
    tipos = Tipo.objects.all()
    context = {
        'atendentes': atendentes,
        'servidores': servidores,
        'tipos': tipos
    }
    return render(request, '_pages_/atendentes.html', context)

def addSetor(request):
    if request.method == 'POST':
        form = SetorForm(data=request.POST)
        if form.is_valid():
            setor = form.save()
            return redirect('chamados:cadastro')
    else:
        form = SetorForm()
        
    return render(request, '_pages_/addSetor.html', {'form': form})    

def addComentario(request, idChamado):
    chamado = Chamado.objects.get(id=idChamado)
    if request.method == 'POST':
        form = ComentarioForm(data=request.POST)
        if form.is_valid():
            servidor = Servidor.objects.get(user = request.user)
            comentario = form.save(commit=False)
            comentario.quemComentou = servidor
            comentario.chamado = chamado
            
            comentario.save()
            comentario.notificaEnvolvidos()
            
    return redirect(reverse('chamados:chamado', args=[chamado.id]))

@login_required
def transformaParaAtendente(request):
    
    servidor = request.POST.get('servidor')
    try:
        atendente = Atendente.objects.get(id=servidor)
    except:
        servidor = Servidor.objects.get(id=servidor)
        idTipos = request.POST.getlist('tipo')
        
        
        atendente = Atendente(
            user = servidor.user,
            nome = servidor.nome,
            email = servidor.email,
            contato = servidor.contato,
            setor = servidor.setor,
        )
        
        atendente.save()
        
        for id in idTipos:
            atendente.tipo.add(id)
        
        atendente.user.is_staff = True
        atendente.user.save()
        
        atendente.save()
        servidor.delete()

    return redirect('chamados:atendentes')
    
@login_required
def transformaParaServidor(request, atendente):
    atendente = Atendente.objects.get(id=atendente)
        
        
    servidor = Servidor(
        user = atendente.user,
        nome = atendente.nome,
        email = atendente.email,
        contato = atendente.contato,
        setor = atendente.setor,
    )
    
    servidor.user.is_staff = False
    servidor.user.save()
    
    servidor.save()
    atendente.delete()

    return redirect('chamados:atendentes')

def listaServidores(request):
    servidores = Servidor.objects.all()
    
    return render(request, '_pages_/listaServidores.html', {'servidores': servidores})

def servidor(request, idServidor):
    servidor = Servidor.objects.get(id=idServidor)
    
    return render(request, '_pages_/servidor.html', {'servidor': servidor})

def apagaServidor(request, idServidor):
    servidor = Servidor.objects.get(id=idServidor)
    user = servidor.user
    servidor.delete()
    user.delete()
    
    return redirect('chamados:servidores')

def passwordEmail(request, idChamado):
   chamado = Chamado.objects.get(id=idChamado)

   context = {
    'chamado': chamado,
   }

   return render(request, 'registration/password_reset_email.html', context)

def userIsStaff(request):
    return JsonResponse(request.user.is_staff, safe=False)
    
async def send_message(chamado):
    uri = "ws://localhost:8000/ws/"
    
    dictChamado = {
        'numero': chamado.numero,
        'requisitante': chamado.requisitante.nome,
        'prioridade': chamado.get_prioridade_display(),
        'setor': chamado.setor.nome,
        'status': chamado.get_status_display(),
        'tipo': chamado.tipo.sigla,
        'assunto': chamado.assunto,
        'dataAbertura': chamado.dataAbertura.strftime('%d/%m/%Y %H:%M:%S'),
        'id': chamado.id
    }
    
    jsonChamado = json.dumps(dictChamado)
    
    async with websockets.connect(uri) as websocket:
        message = jsonChamado
        await websocket.send(message)
        

