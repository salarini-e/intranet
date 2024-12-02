from django.shortcuts import render, redirect
from django.views.decorators.clickjacking import xframe_options_exempt
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from .models import (TipoChamado, Secretaria, Setor, Servidor, Chamado, OSImpressora, OSInternet, OSSistemas, Atendente, Mensagem, OSTelefonia, 
                     PeriodoPreferencial, Pausas_Execucao_do_Chamado, Historico_Designados)
from .forms import (CriarChamadoForm, OSInternetForm, OSImpressoraForm, OSSistemasForm, ServidorForm,
                    MensagemForm, AtendenteForm, TipoChamadoForm, OSTelefoniaForm, CriarSetorForm, Form_Agendar_Atendimento,
                    Form_Motivo_Pausa)
from django.contrib.auth.decorators import login_required
from django.contrib import messages as message
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from .functions import enviar_email_atendente, Email_Chamado
from django.urls import reverse
from .functions import obter_filtros, verificar_filtrado, obter_chamados, obter_atendente, obter_opcoes_filtros, paginar_chamados, verificar_chamados_atrasados
from django.core.paginator import Paginator
from autenticacao.functions import clear_tel
import re
from django.db.models import Count, Q
from dateutil.relativedelta import relativedelta
import locale
from django.views.decorators.http import require_POST


# Define a localidade para português (Brasil)
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

@login_required
def pagina_inicial(request):
    atendentes = Atendente.objects.filter(servidor__user=request.user, ativo=True)
    if atendentes.exists():
        atendente = atendentes.first()
        if atendente.nivel in ['1', '2']:
            return redirect('chamados:tickets')
        elif atendente.nivel=='0':
            return redirect('chamados:criar_chamado_escolher')            
        return redirect('chamados:tickets')
    return redirect('chamados:criar_chamado_escolher')

@login_required
def ordenarPorNaoFechados(request):
    if 'ordenacao' in request.session:
        if request.session['ordenacao'] == True:
            request.session['ordenacao'] = False
        else:
            request.session['ordenacao'] = True
    return redirect('chamados:tickets')

@login_required
def criarChamadoEscolher(request):    
    context = {
               'tipos': TipoChamado.objects.all(),
               }
    return render(request, 'chamados/criar-chamado-escolher.html', context)

@login_required
def index(request):
    filtros = obter_filtros(request)
    filtrado = verificar_filtrado(request, filtros)
    chamados = obter_chamados(request, filtros)
    atendente = obter_atendente(request)
    paginacao = paginar_chamados(request, chamados)
    chamados_atrasados_data_agendada, chamados_atrasados_trinta_dias = verificar_chamados_atrasados()

    kpi = {
        'total': chamados.count(),
        'abertos': chamados.filter(status='1').count(),
        'pendentes': chamados.filter(status='2').count(),
        'fechados_finalizados': chamados.filter(status__in=['3', '4']).count()
    }
    
    context = {
        'tipos': TipoChamado.objects.all(),
        'filtrado': filtrado,
        'filtros': obter_opcoes_filtros(),
        'chamados': paginacao,
        'atendente': atendente,        
        'chamados_atrasados': {
                                'exists': any([chamados_atrasados_data_agendada, chamados_atrasados_data_agendada]),
                                'trintadias': chamados_atrasados_trinta_dias, 
                                'agendado': chamados_atrasados_data_agendada
                                },
        'kpi':  kpi
    }
    return render(request, 'chamados/index.html', context)

def zerar_filtros(request):
    if 'filtros' in request.session:
        del request.session['filtros']
    return redirect('chamados:index')  # Redireciona de volta para a página inicial onde os filtros são aplicados

@login_required
def criarChamado(request, sigla):
    atendentes = Atendente.objects.filter(servidor__user=request.user, ativo=True)
    if atendentes.exists():
        atendente = atendentes.first()
        if atendente.nivel == '1':
            return redirect('chamados:tickets')

    def itel(v):
        # Remove todos os caracteres que não são dígitos
        v = re.sub(r'\D', '', v)

        # Adiciona parênteses e espaço para o DDD
        v = re.sub(r'^(\d{2})(\d)', r'(\1) \2', v)

        # Verifica o comprimento da string para formatar o número corretamente
        if len(v) == 14:  # Formato DDD + 9 dígitos (celular)
            v = re.sub(r'(\d{5})(\d)', r'\1-\2', v)  # Coloca hífen entre o 5º e 6º dígitos
        else:  # Formato DDD + 8 dígitos (fixo)
            v = re.sub(r'(\d{4})(\d)', r'\1-\2', v)  # Coloca hífen entre o 4º e 5º dígitos

        return v
    # try:
    #     servidor = Servidor.objects.get(user=request.user)
    # except Servidor.DoesNotExist:
    #     servidor = None
    is_atendente = Atendente.objects.filter(servidor__user=request.user, ativo = True).exists() 

    if request.user.is_superuser or is_atendente:
        template_name = 'chamados/chamado-criar-ti.html'
        servidor = Servidor.objects.get(user=request.user)
        tipo = TipoChamado.objects.get(sigla=sigla)
        initial_data = {
            'tipo': tipo,
            'user_inclusao': servidor.id,
            'setor_id': '-',
        }
    else:
        template_name = 'chamados/chamado-criar-servidor.html'
        servidor = Servidor.objects.get(user=request.user)
        tipo = TipoChamado.objects.get(sigla=sigla)
        telefone_formatado = itel(servidor.telefone)  # Formata o telefone
        initial_data = {
            'secretaria': servidor.setor.secretaria.id,
            'setor': '-',
            'telefone': telefone_formatado,  # Usa o telefone formatado
            'tipo': tipo,
            'requisitante': servidor.id, 
            'user_inclusao': servidor.id
        }

    if request.POST:
        form = CriarChamadoForm(request.POST, request.FILES, user=request.user)

        if form.is_valid():
            chamado = form.save(commit=False)
            chamado.user_inclusao = servidor

            chamado.telefone = clear_tel(form.cleaned_data['telefone'])
            chamado.profissional_designado = form.cleaned_data.get('profissional_designado')
            
            chamado.save()
            chamado.gerar_hash()
            chamado.gerar_protocolo()

            message.success(request, 'Chamado criado com sucesso! Seu protocolo é {}'.format(chamado.n_protocolo))
            mensagem, status = Email_Chamado(chamado).chamado_criado()
            if status == 400:
                message.error(request, mensagem)

            try:
                chamado.gerar_notificacoes()
            except ValueError as e:
                message.error(request, str(e))
            return redirect('chamados:tickets')
        

    else:
        form = CriarChamadoForm(initial=initial_data, user=request.user)

    context = {
        'tipos': TipoChamado.objects.all(),
        'form': form,
        'form_setor': CriarSetorForm(prefix='setor', initial={'user_inclusao': request.user.id}),
        'form_user': ServidorForm(prefix='servidor', initial={'user_inclusao': request.user.id})
    }

    return render(request, template_name, context)

@login_required
def detalhes(request, hash):
    chamado = Chamado.objects.get(hash=hash)
    servidor = Servidor.objects.get(user=request.user)
    tipos_chamados = TipoChamado.objects.all()

    if request.method == 'POST':        
        form = MensagemForm(request.POST, request.FILES)
        if form.is_valid():
            mensagem = form.save(commit=False)
            mensagem.chamado = chamado
            mensagem.user_inclusao = servidor
            mensagem.confidencial = request.POST.get('confidencial') == '1'
            mensagem.save()            
            mensagem.notificar_nova_mensagem()
            chamado.dt_atualizacao = timezone.now() 
            chamado.save() 
            message.success(request, 'Mensagem enviada com sucesso!')
        # else:
        #     print(form.errors)

    # extensoes = {
    #     'IMP': OSImpressora,
    #     'INT': OSInternet,
    #     'SIS': OSSistemas,
    #     'TEL': OSTelefonia,
    # }

    # Função para formatar o telefone
    def itel(v):
        v = re.sub(r'\D', '', v)
        v = re.sub(r'^(\d{2})(\d)', r'(\1) \2', v)
        if len(v) == 14:
            v = re.sub(r'(\d{5})(\d)', r'\1-\2', v)
        else:
            v = re.sub(r'(\d{4})(\d)', r'\1-\2', v)
        return v
    
    requisitante_telefone = itel(chamado.requisitante.telefone)

    context = {
        'chamado': chamado,    
        'servidor': servidor,    
        'atendentes': Atendente.objects.filter(ativo=True),
        'atendente': Atendente.objects.filter(servidor=servidor),   
        'mensagens': Mensagem.objects.filter(chamado=chamado),   
        'prioridades': chamado.PRIORIDADE_CHOICES,
        'status': chamado.STATUS_CHOICES,     
        'is_atendente': Atendente.objects.filter(servidor = servidor, ativo = True).exists(),
        'tipos': tipos_chamados,
        'tipos_chamados': tipos_chamados,
        'requisitante_telefone': requisitante_telefone
    }
    return render(request, 'chamados/detalhes.html', context)


@login_required
def detalhes_imprimir(request, hash):
    chamado = Chamado.objects.get(hash=hash)
    servidor = Servidor.objects.get(user=request.user)
    if request.method == 'POST':
        
        form = MensagemForm(request.POST, request.FILES)
        if form.is_valid():
            mensagem = form.save(commit=False)
            mensagem.chamado = chamado
            mensagem.user_inclusao = servidor
            mensagem.save()            
            message.success(request, 'Mensagem enviada com sucesso!')
        # else:
        #     print(form.errors)

    # extensoes = {
    #     'IMP': OSImpressora,
    #     'INT': OSInternet,
    #     'SIS': OSSistemas,
    #     'TEL': OSTelefonia,
    # }
    # if chamado.tipo.sigla in extensoes:
    #     extensao = extensoes[chamado.tipo.sigla].objects.get(chamado=chamado)
    # else:
    #     extensao = None

    context = {
        'chamado': chamado,
        # 'ext': extensao,    
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
            atributo = request.POST['atributo']
            if atributo == 'status':
                chamado.status = request.POST['valor']   
                if request.POST['valor'] == '4':
                    chamado.dt_fechamento = timezone.now()             
            elif atributo == 'prioridade':
                chamado.prioridade = request.POST['valor']
            elif atributo == 'atendente':
                chamado.profissional_designado = Atendente.objects.get(id=request.POST['valor'])                
                
                mensagem, status = Email_Chamado(chamado).notificar_solicitante('Seu chamado foi atualizado!')
                if status == 400:
                    message.error(request, mensagem)
                else:
                    message.success(request, mensagem)

                mensagem_atendente, status_atendente = Email_Chamado(chamado).atribuir_atendente('Chamado atribuído a você!')
                if status_atendente == 400:
                    message.error(request, mensagem_atendente)
                    
                elif status_atendente == 200:
                    message.success(request, mensagem_atendente)
                
                
            else:                
                return JsonResponse({'status': 400})
            chamado.save()  
            message.success(request, f'{atributo.capitalize()} atualizado com sucesso!')
            return JsonResponse({'status': 200})    
    return JsonResponse({'status': 403})

@login_required
def iniciar_atendimento(request, hash):    
    chamado = Chamado.objects.get(hash=hash)
    pagina_anterior = request.META.get('HTTP_REFERER', '/')
    if not chamado.dt_agendamento:
        chamado.dt_agendamento =  timezone.now()     
    chamado.dt_inicio_execucao = timezone.now()
    chamado.status = '1'
    chamado.save()
    message.success(request, f'Atendimento iniciado ao chamado {chamado.n_protocolo}!')
    mensagem, status = Email_Chamado(chamado).notificar_solicitante('Seu chamado está em atendimento!')
    if status == 400:
        message.error(request, mensagem)
            
    return redirect(pagina_anterior)

@login_required
def retomar_atendimento(request, hash):
    chamado = Chamado.objects.get(hash=hash)
    intervalo = Pausas_Execucao_do_Chamado.objects.filter(chamado=chamado).last()
    intervalo.dt_fim = timezone.now()
    intervalo.user_fim = Servidor.objects.get(user=request.user)
    intervalo.save()
    chamado.status = '1'
    chamado.save()
    message.success(request, f'Retomado o atendimento do chamado {chamado.n_protocolo}!')
    mensagem, status = Email_Chamado(chamado).notificar_solicitante('Seu chamado está em atendimento!')
    if status == 400:
        message.error(request, mensagem)
        
    return redirect('chamados:index')


@login_required
def pausar_atendimento(request, hash):
    chamado = Chamado.objects.get(hash=hash)
    intervalo = Pausas_Execucao_do_Chamado.objects.create(
        chamado=chamado,
        dt_inicio=timezone.now(),        
        user_inclusao=Servidor.objects.get(user=request.user)
    
    )    
    chamado.status = '2'
    chamado.save()
    message.success(request, f'Atendimento do chamado {chamado.n_protocolo} pausado!')
    mensagem, status = Email_Chamado(chamado).notificar_solicitante('O atendimento do seu chamado foi interrompido!')
    if status == 400:
        message.error(request, mensagem)
    return redirect('chamados:motivo', hash=hash)

@login_required
def declarar_motivo_pausa(request, hash):
    chamado = Chamado.objects.get(hash=hash)
    instance = Pausas_Execucao_do_Chamado.objects.filter(chamado=chamado, user_inclusao=Servidor.objects.get(user=request.user)).last()
    if request.method == 'POST':
        form = Form_Motivo_Pausa(request.POST, instance=instance)
        if form.is_valid():
            form.save()            
            return redirect('chamados:index')
    else:
        form = Form_Motivo_Pausa()
    context = {
        'form': form, 
               'titulo': f'Motivo da paus do chamado {chamado.n_protocolo}', 
               'back_url': reverse('chamados:index'),
               'submit_text': 'Enviar'
               }
    return render(request, 'chamados/generic_form.html', context)

@login_required
def finalizar_atendimento(request, hash):
    chamado = Chamado.objects.get(hash=hash)
    chamado.dt_execucao = timezone.now()
    chamado.status = '4'
    chamado.save()
    message.success(request, f'Atendimento finalizado ao chamado {chamado.n_protocolo}!')
    mensagem, status = Email_Chamado(chamado).notificar_solicitante('Seu chamado foi finalizado!')
    if status == 400:
        message.error(request, mensagem)
    return redirect('chamados:index')

@login_required
def criar_periodos(request):
    if PeriodoPreferencial.objects.all().exists():
        return HttpResponse("OK. Periodos já criados.")

    PeriodoPreferencial.objects.create(nome="Manhã")
    PeriodoPreferencial.objects.create(nome="Tarde")    
    return HttpResponse("OK. Periodos criados com sucesso!")

@login_required
def api_criar_setor(request):
    if request.method == 'POST':
        # print(request.POST)
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

@login_required
def api_mudar_status(request):
    servidor = Servidor.objects.filter(user=request.user).last()
    if request.user.is_superuser or Atendente.objects.filter(servidor=servidor).exists():
        pass
    else:
        return JsonResponse({'status': 403, 'message': 'Acesso negado!'})
    if request.method == 'POST':
        data = request.POST
        try:
            chamado = Chamado.objects.get(hash=data['hash'])
            chamado.status = data['status']
            chamado.dt_atualizacao = timezone.now()
            chamado.save()
            chamado.notificar_status_alterado()
            return JsonResponse({'status': 200, 'message': 'Status atualizado com sucesso!', 'display_status': chamado.get_status_display(), 'id': chamado.id})
        except:
            return JsonResponse({'status': 400, 'message': 'Erro ao atualizar status!'})
    return JsonResponse({'status': 400, 'message': 'Método não permitido!'})

@login_required
def api_mudar_prioridade(request):
    servidor = Servidor.objects.filter(user=request.user).last()
    if request.user.is_superuser or Atendente.objects.filter(servidor=servidor).exists():
        pass
    else:
        return JsonResponse({'status': 403, 'message': 'Acesso negado!'})
    if request.method == 'POST':
        data = request.POST
        try:            
            chamado = Chamado.objects.get(hash=data['hash'])
            chamado.prioridade = data['prioridade']
            chamado.dt_atualizacao = timezone.now()
            chamado.save()
            return JsonResponse({'status': 200, 'message': 'Prioridade atualizada com sucesso!', 'display_prioridade': chamado.get_prioridade_display(), 'id': chamado.id})
        except Exception as E:
            print(E)
            return JsonResponse({'status': 400, 'message': 'Erro ao atualizar prioridade!'})
    return JsonResponse({'status': 400, 'message': 'Método não permitido!'})

@login_required
def api_mudar_atendente(request):
    servidor = Servidor.objects.filter(user=request.user).last()
    if request.user.is_superuser or Atendente.objects.filter(servidor=servidor).exists():
        pass
    else:
        return JsonResponse({'status': 403, 'message': 'Acesso negado!'})
    
    if request.method == 'POST':
        data = request.POST
        try:            
            chamado = Chamado.objects.get(hash=data['hash'])
            
            # Buscar a instância do atendente
            atendente = Atendente.objects.get(id=data['atendente'])
            
            # Atribuir a instância do atendente ao chamado
            chamado.profissional_designado = atendente
            chamado.dt_atualizacao = timezone.now()
            chamado.save()
            chamado.notificar_profissional_designado_alterado()
            Historico_Designados.objects.create(
                chamado=chamado,
                atendente=atendente,
                user_inclusao=request.user
            )
            # print("Chamado id", chamado.id)
            return JsonResponse({
                'status': 200,
                'message': 'Atendente atualizado com sucesso!',
                'display_atendente':  chamado.profissional_designado.nome_servidor,
                'id': chamado.id
            })
        except Exception as E:
            print(E)
            return JsonResponse({'status': 400, 'message': 'Erro ao atualizar atendente!'})
    
    return JsonResponse({'status': 400, 'message': 'Método não permitido!'})

@login_required
def api_criar_servidor(request):
    if request.method == 'POST':
        # print(request.POST)
        form = ServidorForm(request.POST)                    
        if form.is_valid():
            servidor = form.save()    
            servidor.user = form.create_user()
            servidor.user_inclusao = request.user
            servidor.save()
        else:
            # print(form.errors)
            return JsonResponse({'status': 400, 'message': 'Erro ao criar usuário!'})
        
        return JsonResponse({'status': 200, 'message': 'Usuário criado com sucesso!'})        
    return JsonResponse({'status': 400})

@login_required
def agendar_atendimento(request, hash):
    instance = Chamado.objects.get(hash=hash)
    if request.method == 'POST':
        form = Form_Agendar_Atendimento(request.POST, instance=instance)
        if form.is_valid():
            chamado=form.save()
            message.success(request, 'Atendimento agendado com sucesso!')
            mensagem, status = Email_Chamado(chamado).notificar_solicitante('O atendimento do seu chamado foi agendado!')
            if status == 400:
                message.error(request, mensagem)
            return redirect('chamados:detalhes', hash=hash)
    else:
        form = Form_Agendar_Atendimento()
    context = {'form': form, 
               'titulo': f'Chamado {instance.n_protocolo}', 
               'back_url': reverse('chamados:detalhes', args=[instance.hash]),
               'submit_text': 'Agendar'
               }
    return render(request, 'chamados/generic_form.html', context)


from .functions import carregar_novos_filtros, filtrar_chamados

@login_required
def tickets(request):
    if not 'ordenacao' in request.session:
        request.session['ordenacao'] = False

    if request.method == 'POST':
        carregar_novos_filtros(request)

    chamados = filtrar_chamados(request)

    # CONDIÇÃO PARA O PAINEL DE CONTROLE (LISTAR TODOS OS TICKETS QUE NÃO ESTÃO ATRIBUÍDOS)
    if request.GET.get('profissional_designado__isnull') == 'True':
        # Filtra apenas os chamados onde o profissional designado é None
        chamados = [chamado for chamado in chamados if chamado.profissional_designado is None]

    # Filtro para os últimos 30 dias
    if request.GET.get('ultimos_30_dias') == 'True':
        data_limite = timezone.now().replace(tzinfo=None) - timedelta(days=30)
        chamados = [chamado for chamado in chamados if chamado.dt_inclusao >= data_limite]

    if request.GET.get('nao_resolvidos') == 'True':
        chamados = [chamado for chamado in chamados if chamado.status != '4']

    # PARTE PARA LISTAR OS TICKETS NA ABA DE TICKETS NÃO RESOLVIDOS DO PAINEL DE CONTROLE
    status = request.GET.get('status')
    tipo = request.GET.get('tipo')
    profissional_designado = request.GET.get('profissional_designado')
    # CONDIÇÃO PARA O PAINEL DE CONTROLE (LISTAR OS TICKETS DE ACORDO COM O TIPO, STATUS, PROFISSIONAL DESIGINADO) -> TICKETS NÃO RESOLVIDOS
    if tipo:
        if status:
            chamados = [chamado for chamado in chamados if chamado.tipo_id == int(tipo) and chamado.status == str(status)]
        else:
            chamados = [chamado for chamado in chamados if chamado.tipo_id == int(tipo)]
    
    elif profissional_designado:
        if status: 
            chamados = [chamado for chamado in chamados if chamado.profissional_designado_id == int(profissional_designado) and chamado.status == str(status)]
        else: 
            chamados = [chamado for chamado in chamados if chamado.profissional_designado_id == int(profissional_designado)]
    elif status and not tipo and not profissional_designado:
        chamados = [chamado for chamado in chamados if chamado.status == str(status)]
        

    secretarias = Secretaria.objects.all()
    atendentes = Atendente.objects.all()
    tipos_chamados = TipoChamado.objects.all()

    paginator = Paginator(chamados, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # MANTER O FILTRO NA URL MESMO AO TROCAR A PÁGINA DO PAGINATOR
    current_query = request.GET.copy()
    if 'page' in current_query:
        del current_query['page']  # Remover o parâmetro 'page'

    status_choices = Chamado.STATUS_CHOICES
    prioridade_choices = Chamado.PRIORIDADE_CHOICES
    context = {
        'tipos': tipos_chamados,
        'chamados': page_obj,
        'secretarias': secretarias.order_by('apelido'),
        'atendentes': atendentes,
        'tipos_chamados': tipos_chamados,
        'status_choices': status_choices,
        'prioridade_choices': prioridade_choices,
        'current_query': current_query.urlencode(),
        'is_atendente': Atendente.objects.filter(servidor__user=request.user, ativo=True).exists()
    }

    return render(request, 'chamados/tickets.html', context)


def dados_graficos(chamados, data_inicial, data_final, tempo):
    labels=[]
    dados_abertos =[]
    dados_fechados = []
    while data_inicial<= data_final:
        if tempo == 'Hoje':
            label = data_inicial.strftime('%d/%m/%y')
            proximo_periodo = timedelta(days=1)
        elif tempo == 'Uma-semana':
            label = data_inicial.strftime('%d/%m/%y')
            proximo_periodo = timedelta(days=1)
        elif tempo == 'Um-mes':
            label = data_inicial.strftime('%d/%m/%y')
            proximo_periodo = timedelta(days=1)
        elif tempo =='Este-ano':
            label = data_inicial.strftime('%b')
            proximo_periodo = timedelta(days=31)
        elif tempo=='Um-ano':
            label = data_inicial.strftime('%b/%y')
            proximo_periodo = timedelta(days=30)

        if tempo =='Hoje':
            for hour in range(0, 24, 2):
                label= f'{hour:02d}:00'
                labels.append(label)
                
                inicio_hora = data_inicial + timedelta(hours=hour)
                fim_hora = inicio_hora + timedelta(hours=2)
                
                chamados_abertos_intervalo = chamados.filter(dt_inclusao__gte=inicio_hora, dt_inclusao__lt=fim_hora, status='0').count()
                chamados_fechados_intervalo = chamados.filter(dt_inclusao__gte=inicio_hora, dt_inclusao__lt=fim_hora, status='3').count()
                
                dados_abertos.append(chamados_abertos_intervalo)
                dados_fechados.append(chamados_fechados_intervalo)

            dados_abertos.insert(0, chamados_abertos_intervalo) 
            dados_fechados.insert(0, chamados_fechados_intervalo)
        else:
            chamados_periodo = chamados.filter(dt_inclusao__gte=data_inicial, dt_inclusao__lt=data_inicial + proximo_periodo)
            chamados_abertos = chamados_periodo.filter(status='0').count()
            chamados_fechados = chamados_periodo.filter(status='3').count()

            labels.append(label)
            dados_abertos.append(chamados_abertos)
            dados_fechados.append(chamados_fechados)
        data_inicial += proximo_periodo

    return labels, dados_abertos, dados_fechados

def dados_graficos_tipo(chamados, data_inicial, data_final, tempo, tipo):
    labels=[]
    dados_abertos =[]
    dados_fechados = []
    while data_inicial<= data_final:
        if tempo == 'Hoje':
            label = data_inicial.strftime('%d/%m/%y')
            proximo_periodo = timedelta(days=1)
        elif tempo == 'Uma-semana':
            label = data_inicial.strftime('%d/%m/%y')
            proximo_periodo = timedelta(days=1)
        elif tempo == 'Um-mes':
            label = data_inicial.strftime('%d/%m/%y')
            proximo_periodo = timedelta(days=1)
        elif tempo =='Este-ano':
            label = data_inicial.strftime('%b')
            proximo_periodo = timedelta(days=31)
        elif tempo=='Um-ano':
            label = data_inicial.strftime('%b/%y')
            proximo_periodo = timedelta(days=30)

        if tempo =='Hoje':
            for hour in range(0, 24, 2):
                label= f'{hour:02d}:00'
                labels.append(label)
                
                inicio_hora = data_inicial + timedelta(hours=hour)
                fim_hora = inicio_hora + timedelta(hours=2)
                
                chamados_abertos_intervalo = chamados.filter(dt_inclusao__gte=inicio_hora, dt_inclusao__lt=fim_hora, status='0', tipo=tipo).count()
                chamados_fechados_intervalo = chamados.filter(dt_inclusao__gte=inicio_hora, dt_inclusao__lt=fim_hora, status='3', tipo=tipo).count()
                
                dados_abertos.append(chamados_abertos_intervalo)
                dados_fechados.append(chamados_fechados_intervalo)

            dados_abertos.insert(0, chamados_abertos_intervalo) 
            dados_fechados.insert(0, chamados_fechados_intervalo)
        else:
            chamados_periodo = chamados.filter(dt_inclusao__gte=data_inicial, dt_inclusao__lt=data_inicial + proximo_periodo, tipo=tipo)
            chamados_abertos = chamados_periodo.filter(status='0').count()
            chamados_fechados = chamados_periodo.filter(status='3').count()

            labels.append(label)
            dados_abertos.append(chamados_abertos)
            dados_fechados.append(chamados_fechados)
        
        data_inicial += proximo_periodo

    return labels, dados_abertos, dados_fechados

@xframe_options_exempt
@login_required
def painel_controle(request):
    chamados = Chamado.objects.all()
    total_chamados = chamados.count()
    total_chamados_abertos = chamados.filter(status='0').count()
    chamados_abertos_30dias = chamados.filter(dt_inclusao__gte=datetime.now().replace(tzinfo=None) - timedelta(days=30), status='0').count()
    chamados_fechados_30dias = chamados.filter(dt_execucao__gte=datetime.now().replace(tzinfo=None) - timedelta(days=30)).count()
    # chamados_finalizados_30dias =  chamados.filter(dt_execucao__gte=datetime.now().replace(tzinfo=None) - timedelta(days=30), status = '4').count()
    chamados_finalizados_30dias =  chamados.filter(dt_atualizacao__gte=datetime.now().replace(tzinfo=None) - timedelta(days=30), status = '4').count()
    media_diaria = total_chamados / 30
    data_atual = datetime.now()
    tipos_chamados = TipoChamado.objects.all()
    tres_meses_atras = data_atual - timedelta(days=90)
    count_abertos = chamados.filter(status='0').count()
    count_em_atendimento = chamados.filter(status='1').count()
    count_pendentes = chamados.filter(status='2').count()
    count_fechados = chamados.filter(status='3').count()
    count_finalizados = chamados.filter(status='4').count()
    total_nao_resolvidos = total_chamados - count_finalizados
    total_nao_atribuidos = chamados.filter(profissional_designado__isnull=True).count()

    # Calcular a porcentagem de não atribuídos
    porcentagem_nao_atribuidos = (total_nao_atribuidos / total_chamados * 100) if total_chamados > 0 else 0
    # Calcular a porcentagem de não resolvidos
    porcentagem_nao_resolvidos = (total_nao_resolvidos / total_chamados * 100) if total_chamados > 0 else 0
    #Calcular a porcentagem de abertos nos ultimos trinta dias em relação ao total
    # porcentagem_abertos_ultimos_trinta_dias =   (chamados_abertos_30dias / total_chamados * 100) if total_chamados > 0 else 0
    # Preparando dados para o gráfico de barras
    chamados_por_tipo = [{'tipo': tipo.nome, 'quantidade': chamados.filter(tipo=tipo, status='0').count()} for tipo in tipos_chamados]
    # Criando dicionário para armazenar quantidades de chamados abertos por tipo
    chamados_abertos_por_tipo = {
        tipo.nome: chamados.filter(tipo=tipo, status='0').count() for tipo in tipos_chamados
    }
    secretarias = Secretaria.objects.all()
    chamados_abertos_por_secretaria = {}

    for chamado in chamados:
        secretaria = chamado.secretaria
        if secretaria is not None and secretaria != "":
            chamados_abertos_por_secretaria[secretaria.sigla] = chamados.filter(secretaria=secretaria, status='0').count()
        else:
            if 'Sem secretaria definida' not in chamados_abertos_por_secretaria:
                chamados_abertos_por_secretaria['Sem secretaria definida'] = 0
            chamados_abertos_por_secretaria['Sem secretaria definida'] += 1


    # Para incluir o total de chamados sem secretaria, faça uma consulta separada se necessário
    chamados_abertos_por_secretaria['Sem secretaria definida'] = chamados.filter(secretaria=None, status='0').count()
    
    # Chamados criados entre 30 e 60 dias atrás
    chamados_abertos_30_a_60_dias = chamados.filter(
        dt_inclusao__lt=datetime.now().replace(tzinfo=None) - timedelta(days=30),
        dt_inclusao__gte=datetime.now().replace(tzinfo=None) - timedelta(days=60), status='0'
    ).count()

    # Verifica se houve aumento ou diminuição
    aumento_chamados_abertos_30_dias= chamados_abertos_30dias > chamados_abertos_30_a_60_dias

    # Cálculo da porcentagem em relação ao total de chamados
    porcentagem_abertos_30dias = (chamados_abertos_30dias / total_chamados * 100) if total_chamados > 0 else 0
    porcentagem_abertos_30_a_60_dias = (chamados_abertos_30_a_60_dias / total_chamados * 100) if total_chamados > 0 else 0

    variacao_30_a_60_dias = abs(porcentagem_abertos_30dias - porcentagem_abertos_30_a_60_dias)
    

    # DADOS PARA OS GRÁFICOS DE TODOS OS CHAMADOS
    data_atual = datetime.now()
    um_mes_atras = data_atual - timedelta(days=30)
    uma_semana_atras = data_atual - timedelta(days=7)
    um_ano = data_atual - timedelta(days=365)
    inicio_do_ano = datetime(data_atual.year, 1, 1)
    esse_ano = inicio_do_ano

    labels_atendimentos_realizados = []
    dados_abertos_atendimentos_realizados = []
    esse_ano_atendimentos = esse_ano
    while esse_ano_atendimentos <= data_atual:
        # Define o primeiro dia do mês e o primeiro dia do mês seguinte
        proximo_mes = esse_ano_atendimentos + relativedelta(months=1)
        
        # Filtra os chamados do mês atual e com status diferente de 0
        chamados_esse_ano = chamados.filter(
            dt_inclusao__gte=esse_ano_atendimentos,
            dt_inclusao__lt=proximo_mes
        )
        
        # Conta os chamados com status diferente de '0'
        chamados_atendidos_esse_ano = chamados_esse_ano.filter(~Q(status='0')).count()

        # Só adiciona o mês se houver chamados atendidos
        if chamados_atendidos_esse_ano > 0:
            label_atendimento_realizado = esse_ano_atendimentos.strftime('%b')
            labels_atendimentos_realizados.append(label_atendimento_realizado)
            dados_abertos_atendimentos_realizados.append(chamados_atendidos_esse_ano)
        else:
            label_atendimento_realizado = esse_ano_atendimentos.strftime('%b')
            labels_atendimentos_realizados.append(label_atendimento_realizado)
            dados_abertos_atendimentos_realizados.append(0)

        # Avança para o próximo mês
        esse_ano_atendimentos = proximo_mes
    
    semanas_mes, dados_abertos_um_mes,dados_fechados_um_mes = dados_graficos(chamados, um_mes_atras, data_atual, "Um-mes")
    uma_semana, dados_abertos_uma_semana, dados_fechados_uma_semana = dados_graficos(chamados, uma_semana_atras, data_atual, "Uma-semana")
    hoje, dados_abertos_hoje, dados_fechados_hoje = dados_graficos(chamados,datetime.now().replace(hour=0, minute=0, second=0, microsecond=0), datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999), 'Hoje')
    meses_ano, dados_abertos_um_ano, dados_fechados_um_ano = dados_graficos(chamados, um_ano, data_atual,'Um-ano' )
    meses_esse_ano, dados_abertos_esse_ano, dados_fechados_esse_ano = dados_graficos(chamados,esse_ano, data_atual, "Este-ano" )
    
    tipos = TipoChamado.objects.all()

    dados_mes_tipo = {}
    dados_uma_semana_atras_tipo = {}
    dados_hoje_tipo = {}
    dados_este_ano_tipo = {}
    dados_um_ano_tipo = {}
    # Loop para processar cada tipo de chamado
    for tipo in tipos:
        tipo_id = str(tipo.id) 
        # informacoes por tipo
        # um mes atras
        semanas_tipo, dados_abertos_tipo, dados_fechados = dados_graficos_tipo(chamados, um_mes_atras, data_atual, "Um-mes", tipo_id)
        # uma semana atras
        semanas_tipo_uma_semana_atras, dados_abertos_tipo_uma_semana_atras, dados_fechados_uma_semana_atras = dados_graficos_tipo(chamados, uma_semana_atras, data_atual, "Uma-semana", tipo_id)
        #hoje
        semanas_tipo_hoje, dados_abertos_tipo_hoje, dados_fechados_hoje = dados_graficos_tipo(chamados, datetime.now().replace(hour=0, minute=0, second=0, microsecond=0), datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999), "Hoje", tipo_id)
        # este ano
        semanas_tipo_este_ano, dados_abertos_tipo_este_ano, dados_fechados_este_ano = dados_graficos_tipo(chamados,esse_ano , data_atual, "Este-ano", tipo_id)
        # um ano atras ate hoje
        semanas_tipo_um_ano, dados_abertos_tipo_um_ano, dados_fechados_um_ano = dados_graficos_tipo(chamados, um_ano , data_atual, "Um-ano", tipo_id)

        # Adiciona os dados ao dicionário
        dados_mes_tipo[tipo_id] = {
            'semanas': semanas_tipo,
            'dados_abertos': dados_abertos_tipo,
            'dados_fechados': dados_fechados,
        }
        dados_uma_semana_atras_tipo[tipo_id] = {
            'semanas': semanas_tipo_uma_semana_atras,
            'dados_abertos': dados_abertos_tipo_uma_semana_atras,
            'dados_fechados': dados_fechados_uma_semana_atras,
        }
        dados_hoje_tipo[tipo_id] = {
            'semanas': semanas_tipo_hoje,
            'dados_abertos': dados_abertos_tipo_hoje,
            'dados_fechados': dados_fechados_hoje,
        }
        dados_este_ano_tipo[tipo_id] = {
            'semanas': semanas_tipo_este_ano,
            'dados_abertos': dados_abertos_tipo_este_ano,
            'dados_fechados': dados_fechados_este_ano
        }
        dados_um_ano_tipo[tipo_id] = {
            'semanas': semanas_tipo_um_ano,
            'dados_abertos': dados_abertos_tipo_um_ano,
            'dados_fechados': dados_fechados_um_ano
        }

    context = {      
        'dados_mes_tipo': dados_mes_tipo,
        'dados_uma_semana_atras_tipo': dados_uma_semana_atras_tipo,
        'dados_hoje_tipo': dados_hoje_tipo,
        'dados_este_ano_tipo': dados_este_ano_tipo,
        'dados_um_ano_tipo': dados_um_ano_tipo,
        'tipos': tipos,
        'count_abertos': count_abertos,
        'count_em_atendimento': count_em_atendimento,
        'count_pendentes': count_pendentes,
        'count_fechados': count_fechados,
        'count_finalizados': count_finalizados,
        'chamados_por_tipo': chamados_por_tipo,
        'dados_abertos_uma_semana': dados_abertos_uma_semana,
        'dados_fechados_uma_semana': dados_fechados_uma_semana,
        'uma_semana': uma_semana,
        'hoje': hoje,
        'dados_abertos_hoje': dados_abertos_hoje,
        'dados_fechados_hoje': dados_fechados_hoje,
        'um_mes_atras': semanas_mes,
        'dados_abertos_um_mes': dados_abertos_um_mes,
        'dados_fechados_um_mes': dados_fechados_um_mes,
        'meses': meses_ano,
        'dados_abertos_um_ano': dados_abertos_um_ano,
        'dados_fechados_um_ano': dados_fechados_um_ano,
        'meses_esse_ano': meses_esse_ano,
        'dados_abertos_esse_ano': dados_abertos_esse_ano,
        'dados_fechados_esse_ano': dados_fechados_esse_ano,
        'total_chamados': total_chamados,
        'chamados_abertos_30dias': chamados_abertos_30dias,
        'chamados_fechados_30dias': chamados_fechados_30dias,
        'chamados_finalizados_30dias': chamados_finalizados_30dias,
        'media_diaria': "{:.1f}".format(media_diaria),
        'chamados_abertos_por_tipo': chamados_abertos_por_tipo,
        'chamado': chamados.first(),
        'total_nao_atribuidos': total_nao_atribuidos,
        'porcentagem_nao_atribuidos': "{:.1f}".format(porcentagem_nao_atribuidos), 
        'variacao_30_a_60_dias': "{:.1f}".format(variacao_30_a_60_dias),
        'aumento_chamados_abertos_30_dias': aumento_chamados_abertos_30_dias,
        'total_nao_resolvidos':  total_nao_resolvidos,
        'porcentagem_nao_resolvidos': "{:.1f}".format(porcentagem_nao_resolvidos),
        'chamados_abertos_por_secretaria': chamados_abertos_por_secretaria,
        'total_chamados_abertos':total_chamados_abertos,
        'labels_atendimentos_realizados': labels_atendimentos_realizados,
        'dados_abertos_atendimentos_realizados': dados_abertos_atendimentos_realizados
    }
    return render(request, 'chamados/painel_controle.html', context)

@login_required
def ver_detalhes_tickets_nao_resolvidos(request):
    chamados_grupos = (
        TipoChamado.objects.annotate(
            aberto=Count('chamado', filter=Q(chamado__status='0')),
            pendente=Count('chamado', filter=Q(chamado__status='2')),
        )
        .annotate(total=Count('chamado'))
        .values('id','nome') 
        .annotate(aberto=Count('chamado', filter=Q(chamado__status='0')),
                  pendente=Count('chamado', filter=Q(chamado__status='2')),
                  total=Count('chamado')) 
        .order_by('nome') 
    )
     # Consulta para profissionais designados
    chamados_profissionais = (
        Atendente.objects.annotate(
            aberto=Count('profissional_designado_chamados', filter=Q(profissional_designado_chamados__status='0')),
            pendente=Count('profissional_designado_chamados', filter=Q(profissional_designado_chamados__status='2')),
            total=Count('profissional_designado_chamados')
        )
        .values('id', 'nome_servidor', 'aberto', 'pendente', 'total')
        .order_by('nome_servidor')
    )

    context = {
        'chamados_grupos': chamados_grupos,
        'chamados_profissionais': chamados_profissionais
    }

    return render(request, 'chamados/verDetalhesTicketsNaoResolvidos.html', context)

@login_required
def ver_perfil(request,matricula):
    is_atendente = Atendente.objects.filter(servidor=Servidor.objects.get(user=request.user)).exists(),
    servidor= get_object_or_404(Servidor, matricula=matricula)

    context = {
        'usuario': servidor,
        'tipos': TipoChamado.objects.all()
    }
    if is_atendente or servidor.user == request.user:
        chamado = Chamado.objects.filter(requisitante = servidor).order_by('-dt_inclusao')
        context['chamado']= chamado
    return render(request, 'chamados/perfil.html', context)

# VIEW PARA VERIFICAR ATUALIZAÇÃO OU CRIAÇÃO DOS CHAMADOS
@login_required
def verificar_atualizacoes(request):
    last_check = request.GET.get('last_check')

    if last_check:
        last_check = last_check.replace(' ', '+')
        try:
            last_check = timezone.datetime.fromisoformat(last_check)
        except ValueError as e:
            print(f"Erro ao converter a data: {e}")
            last_check = timezone.now() - timezone.timedelta(seconds=5)
    else:
        last_check = timezone.now() - timezone.timedelta(seconds=5)

    novos_chamados = Chamado.objects.filter(dt_inclusao__gt=last_check).count()
    atualizacoes = Chamado.objects.filter(dt_atualizacao__gt=last_check, dt_inclusao__lte=last_check).count()

    return JsonResponse({
        'novos_chamados': novos_chamados,
        'atualizacoes': atualizacoes,
        'last_check': timezone.now().isoformat()
    })


@login_required
@require_POST
def mesclar_chamados(request):
    try:
        atendente = Atendente.objects.get(servidor__user=request.user, ativo=True)
        if atendente.nivel not in [0, 1]:
            return JsonResponse({'status': 403, 'message': 'Acesso negado!'})
    except Atendente.DoesNotExist:
        return JsonResponse({'status': 403, 'message': 'Acesso negado!'})

    ids = request.POST.getlist('chamados')
    if not ids:
        return JsonResponse({'status': 400, 'message': 'Nenhum chamado fornecido!'})

    ids = ids[0].split(',')
    chamados_mesclados = Chamado.objects.filter(id__in=ids).order_by('dt_inclusao')

    if not chamados_mesclados.exists():
        return JsonResponse({'status': 404, 'message': 'Chamados não encontrados!'})

    try:
        primeiro_chamado = chamados_mesclados.first()
        chamado_resultante = Chamado.objects.create(
            setor=primeiro_chamado.setor,
            secretaria=primeiro_chamado.secretaria,
            telefone=primeiro_chamado.telefone,
            requisitante=primeiro_chamado.requisitante,
            endereco=primeiro_chamado.endereco,
            tipo=primeiro_chamado.tipo,
            assunto=primeiro_chamado.assunto,
            prioridade=primeiro_chamado.prioridade,
            status='0',
            descricao=primeiro_chamado.descricao,
            profissional_designado=primeiro_chamado.profissional_designado,
            user_inclusao=Servidor.objects.get(user=request.user),
            anexo=primeiro_chamado.anexo,
        )
        chamado_resultante.gerar_hash()
        chamado_resultante.gerar_protocolo()

        for chamado in chamados_mesclados:
            Mensagem.objects.filter(chamado=chamado).update(chamado=chamado_resultante)
            chamado.mesclado = True
            chamado.status = '5'
            chamado.save()

        chamado_resultante.dt_atualizacao = timezone.now()
        chamado_resultante.save()

        return JsonResponse({'status': 200, 'message': 'Chamados mesclados com sucesso!'})

    except Exception as e:
        return JsonResponse({'status': 500, 'message': f'Erro interno: {str(e)}'})