from django.shortcuts import render
from .models import TipoChamado, Servidor, Chamado, OSImpressora, OSInternet, OSSistemas, Atendente, Mensagem
from .forms import (CriarChamadoForm, OSInternetForm, OSImpressoraForm, OSSistemasForm,
                    MensagemForm, AtendenteForm, TipoChamadoForm)
from django.contrib.auth.decorators import login_required
from django.contrib import messages as message
from django.http import JsonResponse
# Create your views here.
@login_required
def index(request):
    servidor = Servidor.objects.get(user=request.user)
    atendente = Atendente.objects.filter(servidor=servidor)
    if atendente.exists():
        chamados = Chamado.objects.all()
    else:
        chamados = Chamado.objects.filter(requisitante=servidor)
    
    chamados = {
        'todos': chamados,
        'abertos':chamados.filter(status='0'),
        'em_atendimento':chamados.filter(status='1'),
        'pendentes':chamados.filter(status='2'),
        'fechados':chamados.filter(status='3'),        
    }
    context={
        'tipos': TipoChamado.objects.all(),
        'chamados': chamados
    }
    return render(request, 'chamados/index.html', context)


@login_required
def criarChamado(request, sigla):
    forms ={
        'IMP': OSImpressoraForm,
        'INT': OSInternetForm,
        'SIS': OSSistemasForm
    }
    servidor = Servidor.objects.get(user=request.user)
    tipo = TipoChamado.objects.get(sigla=sigla)
    if request.POST:
        form = CriarChamadoForm(request.POST, request.FILES)
        if sigla in forms:
            form_ext = forms[sigla](request.POST, request.FILES)
        else:
            form_ext = None
        if form.is_valid():
            chamado = form.save()
            chamado.user_inclusao = servidor
            chamado.save()
            chamado.gerar_hash()
            chamado.gerar_protocolo()
            print('Opa')
            if sigla in forms:                
                print('Uhul!')
                if form_ext.is_valid():
                    print('Yha!')
                    ext = form_ext.save()
                    ext.chamado = chamado
                    ext.save()
            
            message.success(request, 'Chamado criado com sucesso! Seu protocolo é {}'.format(chamado.n_protocolo))            
            form = CriarChamadoForm(initial={'secretaria': servidor.setor.secretaria.id, 'setor': servidor.setor.id, 'telefone': servidor.telefone, 'tipo': tipo, 'requisitante': servidor.id, 'user_inclusao': request.user})
    else:
        form = CriarChamadoForm(initial={'secretaria': servidor.setor.secretaria.id, 'setor': servidor.setor.id, 'telefone': servidor.telefone, 'tipo': tipo, 'requisitante': servidor.id, 'user_inclusao': request.user})
        form_ext = None
        if sigla in forms:
            form_ext = forms[sigla]()
            

    context={
        'form': form,
        'form_ext': form_ext
    }
    return render(request, 'chamados/chamado-criar.html', context)

@login_required
def detalhes(request, hash):
    
    chamado = Chamado.objects.get(hash=hash)
    servidor = Servidor.objects.get(user=request.user)
    if request.method == 'POST':
        print(request.POST)
        form = MensagemForm(request.POST, request.FILES)
        if form.is_valid():
            mensagem = form.save(commit=False)
            mensagem.chamado = chamado
            mensagem.user_inclusao = servidor
            mensagem.save()            
            message.success(request, 'Mensagem enviada com sucesso!')
        else:
            print(form.errors)

    extensoes = {
        'IMP': OSImpressora,
        'INT': OSInternet,
        'SIS': OSSistemas
    }
    if chamado.tipo.sigla in extensoes:
        extensao = extensoes[chamado.tipo.sigla].objects.get(chamado=chamado)
    else:
        extensao = None

    context = {
        'chamado': chamado,
        'ext': extensao,    
        'servidor': servidor,    
        'atendentes': Atendente.objects.filter(ativo=True),
        'atendente': Atendente.objects.filter(servidor=servidor),   
        'mensagens': Mensagem.objects.filter(chamado=chamado),   
        'prioridades': chamado.PRIORIDADE_CHOICES,
        'status': chamado.STATUS_CHOICES,         
    }
    return render(request, 'chamados/detalhes.html', context)

@login_required
def attChamado(request, hash):
    servidor = Servidor.objects.get(user=request.user)
    atendente = Atendente.objects.filter(servidor=servidor)
    if atendente.exists():
        chamado = Chamado.objects.get(hash=hash)
        if request.POST:
            print(request.POST)
            atributo = request.POST['atributo']
            if atributo == 'status':
                chamado.status = request.POST['valor']                
            elif atributo == 'prioridade':
                chamado.prioridade = request.POST['valor']
            elif atributo == 'atendente':
                chamado.atendente = Atendente.objects.get(id=request.POST['valor'])                
            else:                
                return JsonResponse({'status': 400})
            chamado.save()  
            message.success(request, f'{atributo.capitalize()} atualizado com sucesso!')
            return JsonResponse({'status': 200})    
    return JsonResponse({'status': 403})