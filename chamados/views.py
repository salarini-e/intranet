from django.shortcuts import render
from .models import TipoChamado, Servidor, Chamado, OSImpressora, OSInternet, OSSistemas, Atendente
from .forms import (CriarChamadoForm, OSInternetForm, OSImpressoraForm, OSSistemasForm,
                    MensagemForm, AtendenteForm, TipoChamadoForm)
from django.contrib.auth.decorators import login_required
from django.contrib import messages as message

# Create your views here.
@login_required
def index(request):
    chamados = {
        'todos': Chamado.objects.all(),
        'abertos': Chamado.objects.filter(status='0'),
        'em_atendimento': Chamado.objects.filter(status='1'),
        'pendentes': Chamado.objects.filter(status='2'),
        'fechados': Chamado.objects.filter(status='3'),        
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
            if sigla in forms:                
                if form_ext.is_valid():
                    ext = form_ext.save(commit=False)
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
def detalhes(request, id):
    
    chamado = Chamado.objects.get(id=id)
    servidor = Servidor.objects.get(user=request.user)
    
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
        'atendentes': Atendente.objects.filter(ativo=True),
        'atendente': Atendente.objects.filter(servidor=servidor),
        'form': MensagemForm()
    }
    return render(request, 'chamados/detalhes.html', context)