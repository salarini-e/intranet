from django.shortcuts import render, redirect
from .models import TipoChamado, Secretaria, Setor, Servidor, Chamado, OSImpressora, OSInternet, OSSistemas, Atendente, Mensagem, OSTelefonia, PeriodoPreferencial
from .forms import (CriarChamadoForm, OSInternetForm, OSImpressoraForm, OSSistemasForm, ServidorForm,
                    MensagemForm, AtendenteForm, TipoChamadoForm, OSTelefoniaForm, CriarSetorForm, Form_Agendar_Atendimento)
from django.contrib.auth.decorators import login_required
from django.contrib import messages as message
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from .functions import enviar_email_atendente
from django.contrib.auth.models import User
# Create your views here.

@login_required
def index(request):
    servidor = Servidor.objects.get(user=request.user)
    atendente = Atendente.objects.filter(servidor=servidor)
    if atendente.exists():
        chamados = Chamado.objects.all().order_by('-dt_inclusao')
        atendente = atendente.first()
        designados = chamados.filter(profissional_designado=atendente)
    else:
        chamados = Chamado.objects.filter(requisitante=servidor).order_by('-dt_inclusao')
        atendente = None
        designados = []
    
    chamados = {
        'todos': chamados,
        'abertos':chamados.filter(status='0'),
        'em_atendimento':chamados.filter(status='1'),
        'pendentes':chamados.filter(status='2'),
        'fechados':chamados.filter(status='3'),        
        'designados': designados
    }
    context={
        'tipos': TipoChamado.objects.all(),
        'chamados': chamados,
        'atendente': atendente
    }
    return render(request, 'chamados/index.html', context)

@login_required
def criarChamado(request, sigla):
    forms ={
        'IMP': OSImpressoraForm,
        'INT': OSInternetForm,
        'SIS': OSSistemasForm,
        'TEL': OSTelefoniaForm,
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
            if sigla in forms:                
                if form_ext.is_valid():
                    ext = form_ext.save()
                    ext.chamado = chamado
                    ext.save()
            
            message.success(request, 'Chamado criado com sucesso! Seu protocolo é {}'.format(chamado.n_protocolo))            
            return redirect('chamados:index')
    else:
        form = CriarChamadoForm(initial={'secretaria': servidor.setor.secretaria.id, 'setor': servidor.setor.id, 'telefone': servidor.telefone, 'tipo': tipo, 'requisitante': servidor.id, 'user_inclusao': servidor.id})
        form_ext = None
        if sigla in forms:
            form_ext = forms[sigla]()
            

    context={
        'form': form,
        'form_ext': form_ext,
        'form_setor': CriarSetorForm(prefix='setor', initial={'user_inclusao': request.user.id}),
        'form_user': ServidorForm(prefix='servidor', initial={'user_inclusao': request.user.id})
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
        'SIS': OSSistemas,
        'TEL': OSTelefonia,
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
def detalhes_imprimir(request, hash):
    
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
        'SIS': OSSistemas,
        'TEL': OSTelefonia,
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
    return render(request, 'chamados/detalhes-imprimir.html', context)

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
                if request.POST['valor'] == '4':
                    chamado.dt_fechamento = timezone.now()             
            elif atributo == 'prioridade':
                chamado.prioridade = request.POST['valor']
            elif atributo == 'atendente':
                chamado.profissional_designado = Atendente.objects.get(id=request.POST['valor'])                
                msg, status = enviar_email_atendente(chamado.profissional_designado.servidor, chamado)
                if status == 200:
                    message.success(request, msg)
                else:
                    message.success(request, msg)
                
            else:                
                return JsonResponse({'status': 400})
            chamado.save()  
            message.success(request, f'{atributo.capitalize()} atualizado com sucesso!')
            return JsonResponse({'status': 200})    
    return JsonResponse({'status': 403})

def iniciar_atendimento(request, hash):
    chamado = Chamado.objects.get(hash=hash)
    chamado.dt_inicio_execucao = timezone.now()
    chamado.status = '1'
    chamado.save()
    message.success(request, f'Atendimento iniciado ao chamado {chamado.n_protocolo}!')
    return redirect('chamados:index')

def finalizar_atendimento(request, hash):
    chamado = Chamado.objects.get(hash=hash)
    chamado.dt_execucao = timezone.now()
    chamado.status = '3'
    chamado.save()
    message.success(request, f'Atendimento finalizado ao chamado {chamado.n_protocolo}!')
    return redirect('chamados:index')

#criar periodos
def criar_periodos(request):
    if PeriodoPreferencial.objects.all().exists():
        return HttpResponse("OK. Periodos já criados.")

    PeriodoPreferencial.objects.create(nome="Manhã")
    PeriodoPreferencial.objects.create(nome="Tarde")    
    return HttpResponse("OK. Periodos criados com sucesso!")

def api_criar_setor(request):
    if request.method == 'POST':
        print(request.POST)
        data = request.POST
        setor = Setor.objects.create(
            nome=data['nome'],
            apelido=data['apelido'],
            sigla=data['sigla'],
            cep=data['cep'],
            bairro=data['bairro'],
            endereco=data['endereco'],
            secretaria=Secretaria.objects.get(id=data['secretaria']),
        )
        return JsonResponse({'status': 200, 'message': 'Setor criado com sucesso!'})
    return JsonResponse({'status': 400, 'message': 'Erro ao criar setor!'})



def api_criar_servidor(request):
    if request.method == 'POST':
        print(request.POST)
        form = ServidorForm(request.POST)                    
        if form.is_valid():
            servidor = form.save()    
            servidor.user = form.create_user()
            servidor.user_inclusao = request.user
            servidor.save()
        else:
            print(form.errors)
            return JsonResponse({'status': 400, 'message': 'Erro ao criar usuário!'})
        
        return JsonResponse({'status': 200, 'message': 'Usuário criado com sucesso!'})        
    return JsonResponse({'status': 400})

def agendar_atendimento(request, hash):
    instance = Chamado.objects.get(hash=hash)
    if request.method == 'POST':
        form = Form_Agendar_Atendimento(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            message.success(request, 'Atendimento agendado com sucesso!')
            return redirect('chamados:detalhes', hash=hash)
    else:
        form = Form_Agendar_Atendimento()
    return render(request, 'chamados/generic_form.html', {'form': form, 'titulo': 'Agendar Atendimento', 'chamado': instance})