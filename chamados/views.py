from django.shortcuts import render, redirect
from django.views.decorators.clickjacking import xframe_options_exempt
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from .models import TipoChamado, Secretaria, Setor, Servidor, Chamado, OSImpressora, OSInternet, OSSistemas, Atendente, Mensagem, OSTelefonia, PeriodoPreferencial, Pausas_Execucao_do_Chamado
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
    if request.user.is_superuser:
        template_name = 'chamados/chamado-criar-ti.html'
        servidor = Servidor.objects.get(user=request.user)
        tipo = TipoChamado.objects.get(sigla=sigla)
        initial_data = {
            'tipo': tipo,
            'user_inclusao': servidor.id
        }
    else:
        template_name = 'chamados/chamado-criar-servidor.html'
        servidor = Servidor.objects.get(user=request.user)
        tipo = TipoChamado.objects.get(sigla=sigla)
        telefone_formatado = itel(servidor.telefone)  # Formata o telefone
        initial_data = {
            'secretaria': servidor.setor.secretaria.id,
            'setor': servidor.setor.id,
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
            
            # Salva o telefone sem formatação
            chamado.telefone = clear_tel(form.cleaned_data['telefone'])  # Aplica clear_tel
            
            chamado.save()
            chamado.gerar_hash()
            chamado.gerar_protocolo()

            message.success(request, 'Chamado criado com sucesso! Seu protocolo é {}'.format(chamado.n_protocolo))
            mensagem, status = Email_Chamado(chamado).chamado_criado()
            if status == 400:
                message.error(request, mensagem)
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
            message.success(request, 'Mensagem enviada com sucesso!')
        # else:
        #     print(form.errors)

    # extensoes = {
    #     'IMP': OSImpressora,
    #     'INT': OSInternet,
    #     'SIS': OSSistemas,
    #     'TEL': OSTelefonia,
    # }


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
        'tipos_chamados': tipos_chamados
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
    chamado.status = '3'
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
    if request.user.is_superuser or servidor in Atendente.objects.all():
        pass
    else:
        return JsonResponse({'status': 403, 'message': 'Acesso negado!'})
    if request.method == 'POST':
        data = request.POST
        try:
            chamado = Chamado.objects.get(hash=data['hash'])
            chamado.status = data['status']
            chamado.save()
            return JsonResponse({'status': 200, 'message': 'Status atualizado com sucesso!', 'display_status': chamado.get_status_display(), 'id': chamado.id})
        except:
            return JsonResponse({'status': 400, 'message': 'Erro ao atualizar status!'})
    return JsonResponse({'status': 400, 'message': 'Método não permitido!'})

@login_required
def api_mudar_prioridade(request):
    servidor = Servidor.objects.filter(user=request.user).last()
    if request.user.is_superuser or servidor in Atendente.objects.all():
        pass
    else:
        return JsonResponse({'status': 403, 'message': 'Acesso negado!'})
    if request.method == 'POST':
        data = request.POST
        try:            
            chamado = Chamado.objects.get(hash=data['hash'])
            chamado.prioridade = data['prioridade']
            chamado.save()
            return JsonResponse({'status': 200, 'message': 'Prioridade atualizada com sucesso!', 'display_prioridade': chamado.get_prioridade_display(), 'id': chamado.id})
        except Exception as E:
            print(E)
            return JsonResponse({'status': 400, 'message': 'Erro ao atualizar prioridade!'})
    return JsonResponse({'status': 400, 'message': 'Método não permitido!'})

@login_required
def api_mudar_atendente(request):
    servidor = Servidor.objects.filter(user=request.user).last()
    if request.user.is_superuser or servidor in Atendente.objects.all():
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
            chamado.save()
            print("Chamado id", chamado.id)
            return JsonResponse({
                'status': 200,
                'message': 'Atendente atualizado com sucesso!',
                'display_atendente':  chamado.profissional_designado.nome_servidor,  # Exibir o nome do atendente no retorno
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
    if request.method == 'POST':
        carregar_novos_filtros(request)

    # Recupera os chamados, que é uma lista
    chamados = filtrar_chamados(request)

    
   # Filtros adicionais da URL
    status = request.GET.get('status')
    tipo = request.GET.get('tipo')

    # Depuração: Mostrar a URL e os parâmetros recebidos
    print("URL recebida:", request.get_full_path())  # Mostra a URL completa
    print("Status recebido:", status)
    print("Tipo recebido:", tipo)  # Deve mostrar o ID do tipo

    # Filtra os chamados por tipo e status se apropriado
    if tipo:
        if status:  # Se o status também for passado
            chamados = [chamado for chamado in chamados if chamado.tipo_id == int(tipo) and chamado.status == str(status)]
            print("Chamados filtrados por tipo e status:", [(chamado.id, chamado.tipo_id, chamado.status) for chamado in chamados])
        else:  # Se apenas o tipo foi passado
            chamados = [chamado for chamado in chamados if chamado.tipo_id == int(tipo)]
            print("Chamados filtrados apenas por tipo:", [(chamado.id, chamado.tipo_id, chamado.status) for chamado in chamados])
    elif status:  # Se apenas o status for passado
        chamados = [chamado for chamado in chamados if chamado.status == str(status)]
        print("Chamados filtrados apenas por status:", [(chamado.id, chamado.tipo_id, chamado.status) for chamado in chamados])

    secretarias = Secretaria.objects.all()
    atendentes = Atendente.objects.all()
    tipos_chamados = TipoChamado.objects.all()

    # Paginação
    paginator = Paginator(chamados, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'tipos': tipos_chamados,
        'chamados': page_obj,
        'secretarias': secretarias,
        'atendentes': atendentes,
        'tipos_chamados': tipos_chamados,
    }

    return render(request, 'chamados/tickets.html', context)


@xframe_options_exempt
@login_required
def painel_controle(request):
    chamados = Chamado.objects.all()
    total_chamados = chamados.count()
    chamados_abertos_30dias = chamados.filter(dt_inclusao__gte=datetime.now() - timedelta(days=30)).count()
    chamados_fechados_30dias = chamados.filter(dt_execucao__gte=datetime.now() - timedelta(days=30)).count()
    media_diaria = total_chamados / 30
    data_atual = datetime.now()
    tipos_chamados = TipoChamado.objects.all()
    
    tres_meses_atras = data_atual - timedelta(days=90)
    count_abertos = chamados.filter(status='0').count()
    count_em_atendimento = chamados.filter(status='1').count()
    count_pendentes = chamados.filter(status='2').count()
    count_fechados = chamados.filter(status='3').count()

    # Preparando dados para o gráfico de barras
    chamados_por_tipo = [{'tipo': tipo.nome, 'quantidade': chamados.filter(tipo=tipo).count()} for tipo in tipos_chamados]
    # Criando dicionário para armazenar quantidades de chamados abertos por tipo
    chamados_abertos_por_tipo = {
        tipo.nome: chamados.filter(tipo=tipo, status='0').count() for tipo in tipos_chamados
    }
    data_atual = datetime.now()
    tres_meses_atras = data_atual - timedelta(days=90)

    semanas = []
    dados_abertos = []
    dados_fechados = []

    while tres_meses_atras < data_atual:
        semana_inicio = tres_meses_atras.strftime('%d/%m/%y')        
        label_semana = f'{semana_inicio}'

        chamados_semana = chamados.filter(dt_inclusao__gte=tres_meses_atras, dt_inclusao__lt=tres_meses_atras + timedelta(days=7))
        chamados_abertos_semana = chamados_semana.filter(status='0').count()
        chamados_fechados_semana = chamados_semana.filter(status='3').count()

        semanas.append(label_semana)
        dados_abertos.append(chamados_abertos_semana)
        dados_fechados.append(chamados_fechados_semana)

        tres_meses_atras += timedelta(days=7)


    context = {               
        'tipos': TipoChamado.objects.all(),
        'count_abertos': count_abertos,
        'count_em_atendimento': count_em_atendimento,
        'count_pendentes': count_pendentes,
        'count_fechados': count_fechados,
        'chamados_por_tipo': chamados_por_tipo,
        'semanas': semanas,
        'dados_abertos': dados_abertos,
        'dados_fechados': dados_fechados,
        'total_chamados': total_chamados,
        'chamados_abertos_30dias': chamados_abertos_30dias-chamados_fechados_30dias,
        'chamados_fechados_30dias': chamados_fechados_30dias,
        'media_diaria': "{:.1f}".format(media_diaria),
        'chamados_abertos_por_tipo': chamados_abertos_por_tipo,
        'chamado': chamados.first()
    }
    return render(request, 'chamados/painel_controle.html', context)

@login_required
def ver_detalhes_tickets_nao_resolvidos(request):
    chamados = (
        TipoChamado.objects.annotate(
            aberto=Count('chamado', filter=Q(chamado__status='0')),
            pendente=Count('chamado', filter=Q(chamado__status='2')),
        )
        .annotate(total=Count('chamado'))
        .values('id','nome')  # Aqui você está selecionando o nome do tipo
        .annotate(aberto=Count('chamado', filter=Q(chamado__status='0')),
                  pendente=Count('chamado', filter=Q(chamado__status='2')),
                  total=Count('chamado'))  # Total de chamados por tipo
        .order_by('nome')  # Ordena pela coluna nome do TipoChamado
    )

    context = {
        'chamados': chamados
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