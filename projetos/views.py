import os
import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Projetos, Fases, Tarefas, Atividades, Prioridade, Grupo, Comentarios, Demandas, Painel_Acompanhamento_Demandas
from .forms import ProjetosForm
from django.http import JsonResponse, HttpResponse
from instituicoes.models import Servidor
import json

@login_required
def menu_acompanhar_demandas(request):
    if not request.user.is_superuser:
        return HttpResponse('Acesso negado')
    
    paineis = Painel_Acompanhamento_Demandas.objects.all().order_by('titulo')

    context = {
        'paineis': paineis,        
    }
    return render(request, 'tarefas/acompanhar_menu.html', context  )

@login_required
def api_ver_demandas_por_painel_em_andamento(request):
    """
    Retorna demandas em andamento (status='e') dos últimos 31 dias para todos os servidores de um painel.
    """
    painel_hash = request.GET.get('painel_hash')
    if not painel_hash:
        return JsonResponse({'status': 400, 'error': 'Parâmetro painel_hash obrigatório'})
    try:
        painel = Painel_Acompanhamento_Demandas.objects.get(hash=painel_hash)
    except Painel_Acompanhamento_Demandas.DoesNotExist:
        return JsonResponse({'status': 404, 'error': 'Painel não encontrado'})
    from datetime import date, timedelta
    hoje = date.today()
    limite = hoje - timedelta(days=31)
    servidores = painel.servidores.all()
    resultado = []
    for servidor in servidores:
        demandas = Demandas.objects.filter(
            atribuicao=servidor,
            status='e',
            data_prevista_execucao__gte=limite,
            data_prevista_execucao__lte=hoje
        ).order_by('-data_prevista_execucao')[:50]
        resultado.append({
            'servidor': {'id': servidor.id, 'nome': servidor.nome},
            'demandas': [
                {
                    'id': d.id,
                    'nome': d.nome,
                    'descricao': d.descricao,
                    'prioridade': d.prioridade,
                    'data_prevista_execucao': d.data_prevista_execucao.strftime('%Y-%m-%d') if d.data_prevista_execucao else '',
                    'status': d.status,
                }
                for d in demandas
            ]
        })
    return JsonResponse({'status': 200, 'painel': painel.titulo, 'dados': resultado})

@login_required
def api_ver_demandas_por_painel_em_aberto(request):
    """
    Retorna demandas em aberto (status='p') dos últimos 31 dias para todos os servidores de um painel.
    """
    painel_hash = request.GET.get('painel_hash')
    if not painel_hash:
        return JsonResponse({'status': 400, 'error': 'Parâmetro painel_hash obrigatório'})
    try:
        painel = Painel_Acompanhamento_Demandas.objects.get(hash=painel_hash)
    except Painel_Acompanhamento_Demandas.DoesNotExist:
        return JsonResponse({'status': 404, 'error': 'Painel não encontrado'})
    from datetime import date, timedelta
    hoje = date.today()
    limite = hoje - timedelta(days=31)
    servidores = painel.servidores.all()
    resultado = []
    for servidor in servidores:
        demandas = Demandas.objects.filter(
            atribuicao=servidor,
            status='p',
            data_prevista_execucao__gte=limite,
            data_prevista_execucao__lte=hoje
        ).order_by('-data_prevista_execucao')[:50]
        resultado.append({
            'servidor': {'id': servidor.id, 'nome': servidor.nome},
            'demandas': [
                {
                    'id': d.id,
                    'nome': d.nome,
                    'descricao': d.descricao,
                    'prioridade': d.prioridade,
                    'data_prevista_execucao': d.data_prevista_execucao.strftime('%Y-%m-%d') if d.data_prevista_execucao else '',
                    'status': d.status,
                }
                for d in demandas
            ]
        })
    return JsonResponse({'status': 200, 'painel': painel.titulo, 'dados': resultado})

@login_required
def api_ver_demandas_por_painel_concluidas(request):
    """
    Retorna demandas concluídas (status='c') dos últimos 31 dias para todos os servidores de um painel.
    """
    painel_hash = request.GET.get('painel_hash')
    if not painel_hash:
        return JsonResponse({'status': 400, 'error': 'Parâmetro painel_hash obrigatório'})
    try:
        painel = Painel_Acompanhamento_Demandas.objects.get(hash=painel_hash)
    except Painel_Acompanhamento_Demandas.DoesNotExist:
        return JsonResponse({'status': 404, 'error': 'Painel não encontrado'})
    from datetime import date, timedelta
    hoje = date.today()
    limite = hoje - timedelta(days=31)
    servidores = painel.servidores.all()
    resultado = []
    for servidor in servidores:
        demandas = Demandas.objects.filter(
            atribuicao=servidor,
            status='c',
            dt_concluido__gte=limite,
            dt_concluido__lte=hoje
        ).order_by('-dt_concluido')[:50]
        resultado.append({
            'servidor': {'id': servidor.id, 'nome': servidor.nome},
            'demandas': [
                {
                    'id': d.id,
                    'nome': d.nome,
                    'descricao': d.descricao,
                    'prioridade': d.prioridade,
                    'data_prevista_execucao': d.data_prevista_execucao.strftime('%Y-%m-%d') if d.data_prevista_execucao else '',
                    'dt_concluido': d.dt_concluido.strftime('%Y-%m-%d') if d.dt_concluido else '',
                    'status': d.status,
                }
                for d in demandas
            ]
        })
    return JsonResponse({'status': 200, 'painel': painel.titulo, 'dados': resultado})

@login_required
def api_ver_demandas_em_andamento(request):
    """
    Retorna demandas em andamento (status='e') dos últimos 31 dias para um usuário (servidor_id).
    """
    servidor_id = request.GET.get('servidor_id')
    if not servidor_id:
        return JsonResponse({'status': 400, 'error': 'Parâmetro servidor_id obrigatório'})
    from datetime import date, timedelta
    hoje = date.today()
    limite = hoje - timedelta(days=31)
    demandas = Demandas.objects.filter(
        atribuicao_id=servidor_id,
        status='e',
        data_prevista_execucao__gte=limite,
        data_prevista_execucao__lte=hoje
    ).order_by('-data_prevista_execucao')[:50]
    data = [
        {
            'id': d.id,
            'nome': d.nome,
            'descricao': d.descricao,
            'prioridade': d.prioridade,
            'data_prevista_execucao': d.data_prevista_execucao.strftime('%Y-%m-%d') if d.data_prevista_execucao else '',
            'status': d.status,
        }
        for d in demandas
    ]
    return JsonResponse({'status': 200, 'demandas': data})

@login_required
def api_ver_demandas_em_aberto(request):
    """
    Retorna demandas em aberto (status='p') dos últimos 31 dias para um usuário (servidor_id).
    """
    servidor_id = request.GET.get('servidor_id')
    if not servidor_id:
        return JsonResponse({'status': 400, 'error': 'Parâmetro servidor_id obrigatório'})
    from datetime import date, timedelta
    hoje = date.today()
    limite = hoje - timedelta(days=31)
    demandas = Demandas.objects.filter(
        atribuicao_id=servidor_id,
        status='p',
        data_prevista_execucao__gte=limite,
        data_prevista_execucao__lte=hoje
    ).order_by('-data_prevista_execucao')[:50]
    data = [
        {
            'id': d.id,
            'nome': d.nome,
            'descricao': d.descricao,
            'prioridade': d.prioridade,
            'data_prevista_execucao': d.data_prevista_execucao.strftime('%Y-%m-%d') if d.data_prevista_execucao else '',
            'status': d.status,
        }
        for d in demandas
    ]
    return JsonResponse({'status': 200, 'demandas': data})

@login_required
def api_ver_demandas_concluidas(request):
    """
    Retorna demandas concluídas (status='c') dos últimos 31 dias para um usuário (servidor_id).
    """
    servidor_id = request.GET.get('servidor_id')
    if not servidor_id:
        return JsonResponse({'status': 400, 'error': 'Parâmetro servidor_id obrigatório'})
    from datetime import date, timedelta
    hoje = date.today()
    limite = hoje - timedelta(days=31)
    demandas = Demandas.objects.filter(
        atribuicao_id=servidor_id,
        status='c',
        dt_concluido__gte=limite,
        dt_concluido__lte=hoje
    ).order_by('-dt_concluido')[:50]
    data = [
        {
            'id': d.id,
            'nome': d.nome,
            'descricao': d.descricao,
            'prioridade': d.prioridade,
            'data_prevista_execucao': d.data_prevista_execucao.strftime('%Y-%m-%d') if d.data_prevista_execucao else '',
            'dt_concluido': d.dt_concluido.strftime('%Y-%m-%d') if d.dt_concluido else '',
            'status': d.status,
        }
        for d in demandas
    ]
    return JsonResponse({'status': 200, 'demandas': data})

@login_required
def demandas_gerar_relatorio(request):
    # Recebe datas via GET
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    demandas = []

    if data_inicio and data_fim and request.user.is_authenticated:
        try:
            data_inicio_dt = datetime.datetime.strptime(data_inicio, "%Y-%m-%d").date()
            data_fim_dt = datetime.datetime.strptime(data_fim, "%Y-%m-%d").date()
            demandas = Demandas.objects.filter(
                atribuicao__user=request.user,
                data_prevista_execucao__gte=data_inicio_dt,
                data_prevista_execucao__lte=data_fim_dt
            ).order_by('data_prevista_execucao', 'ordem_dia', 'nome')
        except Exception as e:
            demandas = []
    else:
        # Se não há datas, só renderiza o formulário
        return render(request, 'tarefas/gerar_relatorio.html')

    context = {
        'demandas': demandas,
        'data_inicio': data_inicio_dt.strftime('%d/%m/%Y') if data_inicio else '',
        'data_fim': data_fim_dt.strftime('%d/%m/%Y') if data_fim else '',        
        'now': datetime.datetime.now().strftime('%d/%m/%Y %H:%M'),
        'servidor': Servidor.objects.filter(user=request.user).first(),
    }
    return render(request, 'tarefas/relatorio.html', context)


@login_required
def index(request):
    projetos_grupo_membro = Projetos.objects.filter(grupos__membros__user=request.user).exclude(status="A")
    projetos_grupo_responsavel = Projetos.objects.filter(grupos__responsavel__user=request.user).exclude(status="A")
    projetos_autorizado = projetos_grupo_membro | projetos_grupo_responsavel
    projetos_responsavel = Projetos.objects.filter(responsavel__user=request.user).exclude(status="A")
    projetos = projetos_responsavel | projetos_autorizado
    projetos = projetos.distinct()  
    context={
        'projetos': projetos,
        'form_projetos': ProjetosForm(initial={'user_inclusao': request.user})
    }
    return render(request, 'projetos/index.html', context)


@login_required
def todos_projetos(request):
    if not request.user.is_superuser:
        return HttpResponse('Acesso negado')
    projetos = Projetos.objects.all().exclude(status="A")
    context={
        'projetos': projetos,
        'form_projetos': ProjetosForm(initial={'user_inclusao': request.user})
    }
    return render(request, 'projetos/index.html', context)

@login_required
def kanbanboard(request, id):
    
    projeto = Projetos.objects.get(id=id)
    fases = Fases.objects.filter(projeto=projeto).order_by('ordem')
    # servidores = [servidor for grupo in projeto.grupos.all() for servidor in grupo.membros.all()]    
    from collections import OrderedDict
    servidores = sorted(
        OrderedDict.fromkeys(
            servidor for grupo in projeto.grupos.all() for servidor in [grupo.responsavel] + list(grupo.membros.all())  
        ), 
        key=lambda servidor: servidor.nome
    )

    prioridades = Prioridade.objects.all()

    context = {
        'projeto': projeto,
        'fases': fases,     
        'servidores': servidores,
        'prioridades': prioridades,
    }
    # print(context)
    return render(request, 'projetos/kanban.html', context)

@login_required
def api_criar_projeto(request):
    if request.method == 'POST':
        form = ProjetosForm(request.POST)
        # print(request.POST)
        if form.is_valid():
            projeto = form.save()
            return JsonResponse({'status': 200, 'message': 'Projeto criado com sucesso', 'projeto': {
                'id': projeto.id,
                'nome': projeto.nome,
                'responsavel': Servidor.objects.filter(user=projeto.user_inclusao).first().nome.title(),
                'data_fim': projeto.data_fim.strftime('%d/%m/%Y') if projeto.data_fim else '',
                'descricao': projeto.descricao,                
                'status': projeto.status,
            }})
        else:
            return JsonResponse({'status': False, 'erros': form.errors})
    else:
        return JsonResponse({'status': False, 'erros': 'Método inválido'})

import json
@login_required
def api_criar_coluna(request):
    if request.method == 'POST':
        dados = json.loads(request.body)
        nome = dados['nome']
        projeto_id = dados['projeto_id']
        ordem = Fases.objects.filter(projeto__id=projeto_id).count() + 1

        if nome and projeto_id and ordem:
            projeto = Projetos.objects.get(id=projeto_id)
            nova_fase = Fases.objects.create(status='at', projeto=projeto, ordem=ordem, nome=nome, descricao='n/h', user_inclusao=request.user)
            return JsonResponse({'status': 200, 'message': 'Coluna criada com sucesso', 'coluna': {
                'id': nova_fase.id,
                'nome': nova_fase.nome,
                'ordem': nova_fase.ordem,
            }})
        else:
            return JsonResponse({'status': False, 'error': 'Dados incompletos'})
    else:
        return JsonResponse({'status': False, 'error': 'Método inválido'})
    
@login_required
def api_criar_card(request):
    if request.method == 'POST':
        dados = json.loads(request.body)
        nome = dados['nome']
        fase_id = dados['fase_id']
        ordem = Tarefas.objects.filter(fase__id=fase_id).count() + 1

        if nome and fase_id and ordem:
            fase = Fases.objects.get(id=fase_id)
            nova_tarefa = Tarefas.objects.create(fase=fase, orderm=ordem, nome=nome, descricao='n/h', user_inclusao=request.user)
            return JsonResponse({'status': 200, 'message': 'Card criada com sucesso', 'card': {
                'column_id': fase_id,
                'id': nova_tarefa.id,
                'nome': nova_tarefa.nome,
            }})
        else:
            return JsonResponse({'status': 400, 'error': 'Dados incompletos'})
    else:
        return JsonResponse({'status': 403, 'error': 'Método inválido'})
    
@login_required
def api_remover_card(request):
    if request.method == 'POST':
        dados = json.loads(request.body)
        card_id = dados['card_id']
        try:
            Tarefas.objects.get(id=card_id).delete()
            return JsonResponse({'status': 200, 'message': 'Card removido com sucesso', 'card_id': card_id})
        except:
            return JsonResponse({'status': 400, 'error': 'Card não encontrado'})
    else:
        return JsonResponse({'status': 403, 'error': 'Método inválido'})
    

@login_required
def api_mover_card_coluna(request):
    if request.method == 'POST':
        dados = json.loads(request.body)
        card_id = dados['card_id']
        tarefa = Tarefas.objects.get(id=card_id)
        tarefa.fase = Fases.objects.get(id=dados['new_column_id'])
        tarefa.save()
        return JsonResponse({'status': 200, 'message': 'Card movido com sucesso', 'dados': dados})
        # try:
        #     Tarefas.objects.get(id=card_id).delete()
        #     return JsonResponse({'status': 200, 'message': 'Card removido com sucesso', 'card_id': card_id})
        # except:
        #     return JsonResponse({'status': 400, 'error': 'Card não encontrado'})
    else:
        return JsonResponse({'status': 403, 'error': 'Método inválido'})
    

@login_required
def api_mover_card_linha(request):
    if request.method == 'POST':
        dados = json.loads(request.body)
        card_id = dados['card_id']
        tarefa = Tarefas.objects.get(id=card_id)
        tarefa.fase = Fases.objects.get(id=dados['new_column_id'])  
        tarefa.orderm = dados['new_index']
        tarefa.save()
        return JsonResponse({'status': 200, 'message': 'Card movido com sucesso', 'dados': dados})
        # try:
        #     Tarefas.objects.get(id=card_id).delete()
        #     return JsonResponse({'status': 200, 'message': 'Card removido com sucesso', 'card_id': card_id})
        # except:
        #     return JsonResponse({'status': 400, 'error': 'Card não encontrado'})
    else:
        return JsonResponse({'status': 403, 'error': 'Método inválido'})
    
def api_check_card(request):
    if request.method == 'POST':
        dados = json.loads(request.body)
        card_id = dados['card_id']
        tarefa = Tarefas.objects.get(id=card_id)
        tarefa.concluido = True if not tarefa.concluido else False
        tarefa.save()
        return JsonResponse({'status': 200, 'concluida': tarefa.concluido})
    return JsonResponse({'status': 403, 'error': 'Método inválido'})

def api_editar_tarefa(request):
    if request.method == 'POST':
        dados = json.loads(request.body)
        # print(dados)
        card_id = dados['card_id']
        tarefa = Tarefas.objects.get(id=card_id)
        tarefa.nome = dados['nome'] if dados['nome'] else None
        tarefa.descricao = dados['descricao'] if dados['descricao'] else None
        tarefa.data_inicio = dados['data_inicio'] if dados['data_inicio'] else None
        tarefa.data_fim = dados['data_fim'] if dados['data_fim'] else None
        tarefa.atribuicao = Servidor.objects.get(id=dados['atribuicao']) if dados['atribuicao'] else None
        tarefa.prioridade = Prioridade.objects.get(id=dados['prioridade']) if dados['prioridade'] else None
        tarefa.save()
        return JsonResponse({'status': 200, 'card': {'id': tarefa.id,'nome': tarefa.nome, 'descricao': tarefa.descricao, 'data_inicio': tarefa.data_inicio, 'data_fim': tarefa.data_fim, 'atribuicao': tarefa.atribuicao.id if tarefa.atribuicao else '', 'prioridade': tarefa.prioridade.id if tarefa.prioridade else ''}})
    return JsonResponse({'status': 403, 'error': 'Método inválido'})

def api_get_detalhes_projeto(request, id):
        
    projeto = Projetos.objects.get(id=id)
    fases = Fases.objects.filter(projeto=projeto).order_by('ordem')
    tarefas = Tarefas.objects.filter(fase__projeto=projeto).order_by('orderm')
    return JsonResponse({'status': 200, 'projeto': {        
        'nome': projeto.nome,
        'descricao': projeto.descricao,
        'data_inicio': projeto.data_inicio.strftime('%d/%m/%Y') if projeto.data_inicio else '',
        'data_fim': projeto.data_fim.strftime('%d/%m/%Y') if projeto.data_fim else '',
        'status': projeto.status,
        'fases': [{'id': fase.id, 'nome': fase.nome, 'ordem': fase.ordem} for fase in fases],
        'tarefas': [{'id': tarefa.id, 'nome': tarefa.nome, 'concluido': tarefa.concluido, 'fase_id': tarefa.fase.id, 'orderm': tarefa.orderm} for tarefa in tarefas],
        'grupos': [{'id': grupo.id, 'nome': grupo.nome, 'responsavel': {'id': grupo.responsavel.id, 'nome': grupo.responsavel.nome, 'img': grupo.responsavel.get_avatar()}, 'membros': [{'id': membro.id, 'nome': membro.nome, 'img': membro.get_avatar()} for membro in grupo.membros.all()]} for grupo in projeto.grupos.all()]
    }})
    # return JsonResponse({'status': 403, 'error': 'Método inválido'})

def api_busca_membros(request):
    search = request.GET.get('search')
    membros = Servidor.objects.filter(nome__icontains=search)
    return JsonResponse({'status': 200, 'membros': [{'id': membro.id, 'nome': membro.nome, 'img': membro.get_avatar()} for membro in membros]})

def api_criar_grupo(request):
    if request.method == 'POST':
        dados = request.POST
        # print(request.POST)
        nome = dados['nome']
        responsavel = Servidor.objects.get(user = request.user)
        membros = dados['membros'].split(',')
        grupo = Grupo.objects.create(responsavel=responsavel ,nome=nome, user_inclusao=request.user)
        for membro in membros:
            grupo.membros.add(Servidor.objects.get(id=membro))
        return JsonResponse({'status': 200, 'message': 'Grupo criado com sucesso'})
    return JsonResponse({'status': 403, 'error': 'Método inválido'})

def api_meus_grupos(request):
    grupos_1 = Grupo.objects.filter(responsavel__user=request.user)
    grupos_2 = Grupo.objects.filter(membros__user__in=[request.user])
    grupos = grupos_1 | grupos_2
    return JsonResponse({'status': 200, 'grupos': [{'id': grupo.id, 'nome': grupo.nome, 'responsavel': {'id': grupo.responsavel.id, 'nome': grupo.responsavel.nome, 'img': grupo.responsavel.get_avatar()}, 'membros': [{'id': membro.id, 'nome': membro.nome, 'img': membro.get_avatar()} for membro in grupo.membros.all()]} for grupo in grupos]})

def api_editar_projeto(request):
    '''<QueryDict: 
    {'csrfmiddlewaretoken': ['ulOfkecky5hILN9TPBbVcGOKDgvCGswJzwWrdALq2iXdD4EzG9vQAgrhi4VzCr19'], 
    'id': ['1'], 'status': ['E'], 
    'nome_ed': ['Desenvolve NF'], 
    'responsavel': [''], 
    'id_responsavel': [''], 
    'descricao': ['Lorem ipsum dolor sit amet...'], 
    'data_inicio': ['2025-01-14'], 
    'data_fim': ['2025-01-31']}>
'''
    if request.method == 'POST':
        dados = request.POST
        # print(dados)
        projeto = Projetos.objects.get(id=dados['id'])
        projeto.nome = dados['nome_ed']
        projeto.descricao = dados['descricao']
        projeto.data_inicio = dados['data_inicio']
        projeto.data_fim = dados['data_fim']
        projeto.status = dados['status']
        projeto.responsavel = Servidor.objects.get(id=dados['responsavel']) if dados['responsavel'] else projeto.responsavel
        projeto.save()
        projeto_dict = {
            'id': projeto.id,
            'nome': projeto.nome,
            'descricao': projeto.descricao,
            'data_inicio': projeto.data_inicio if projeto.data_inicio is not None else '',
            'data_fim': projeto.data_fim if projeto.data_fim is not None else '',
            'status': projeto.status,
            'status_display': projeto.get_status_display(),
            'responsavel': {'id': projeto.responsavel.id, 'nome': projeto.responsavel.nome, 'img': projeto.responsavel.get_avatar()}
        }
        return JsonResponse({'status': 200, 'message': 'Projeto editado com sucesso', 'projeto': projeto_dict})
    return JsonResponse({'status': 403, 'error': 'Método inválido'})

def api_editar_nome_coluna(request):
    if request.method == 'POST':        
        dados = json.loads(request.body)        
        coluna = Fases.objects.get(id=dados['column_id'])
        coluna.nome = dados['nome']        
        coluna.save()
        return JsonResponse({'status': 200, 'message': 'Coluna editada com sucesso', 'coluna': {'id': coluna.id, 'nome': coluna.nome}})
    return JsonResponse({'status': 403, 'error': 'Método inválido'})

def api_mover_coluna(request):
    if request.method == 'POST':        
        dados = json.loads(request.body)   
        for dado in dados:
            coluna = Fases.objects.get(id=dado['id'])
            coluna.ordem = dado['ordem']
            coluna.save()        
        return JsonResponse({'status': 200, 'message': 'Colunas alteradas'})
    return JsonResponse({'status': 403, 'error': 'Método inválido'})

def api_get_grupos_projeto(request, id):
    projeto = Projetos.objects.get(id=id)
    grupos_responsavel = Grupo.objects.filter(responsavel__user = request.user)
    grupos_membro = Grupo.objects.filter(membros__user__in=[request.user])
    grupos = grupos_responsavel | grupos_membro
    grupos = grupos.distinct()
    grupos_dict = []
    for grupo in grupos:
        grupos_dict.append({
            'id': grupo.id,
            'nome': grupo.nome,
            'responsavel': {'id': grupo.responsavel.id, 'nome': grupo.responsavel.nome, 'img': grupo.responsavel.get_avatar()},
            'membros': [{'id': membro.id, 'nome': membro.nome, 'img': membro.get_avatar()} for membro in grupo.membros.all()],
            'status': True if grupo in projeto.grupos.all() else False
        })    
    
    return JsonResponse({'status': 200, 'grupos': grupos_dict})

def api_atualizar_autorizacoes(request):
    if request.method == 'POST':        
        dados = json.loads(request.body)   
        projeto = Projetos.objects.get(id=dados['id_projeto'])
        grupos = dados['grupos']
        projeto.grupos.clear()
        for grupo in grupos:
            if grupo['checked']:
                projeto.grupos.add(Grupo.objects.get(id=grupo['id']))
        return JsonResponse({'status': 200, 'message': 'Autorizações atualizadas'})
    return JsonResponse({'status': 403, 'error': 'Método inválido'})

def api_enviar_anexo(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        dados = request.FILES
        card = Tarefas.objects.get(id=id)
        card.anexo = dados['anexo']
        card.save()
        return JsonResponse({'status': 200, 'anexo': card.anexo.url, 'anexo_url': card.anexo.url})
    
    return JsonResponse({'status': 403, 'error': 'Método inválido'})

# /projetos/api/get-projeto-comentarios/${id}/
def api_get_projeto_comentarios(request, id):
    projeto = Projetos.objects.get(id=id)
    comentarios = Comentarios.objects.filter(projeto=projeto)
    comentarios_dict = []
    for comentario in comentarios:
        comentarios_dict.append({
            'nome': comentario.servidor(),            
            'data': comentario.dt_inclusao.strftime('%d/%m/%Y'),
            'hora': comentario.dt_inclusao.strftime('%H:%M'),
            'comentario': comentario.descricao,            
        })
    return JsonResponse({'status': 200, 'comentarios': comentarios_dict})

def api_enviar_comentario(request):
    if request.method == 'POST':
        dados = json.loads(request.body)
        projeto = Projetos.objects.get(id=dados['projeto_id'])
        Comentarios.objects.create(atribuicao='p', projeto=projeto, descricao=dados['comentario'], user_inclusao=request.user)
        return JsonResponse({'status': 200, 'message': 'Comentário enviado com sucesso'})
    
    return JsonResponse({'status': 403, 'error': 'Método inválido'})

@login_required
def tarefas(request):
    today = datetime.date.today()
    demandas = Demandas.objects.filter(atribuicao__user=request.user).order_by('ordem_dia', 'data_prevista_execucao', 'nome')

    my_day = []
    for demanda in demandas:
        if demanda.rotina or demanda.data_prevista_execucao == today:
            if demanda.data_inicio and demanda.data_fim:
                if demanda.data_fim < today and not demanda.concluido:
                    demanda.status = 'Atrasada'
                elif not demanda.concluido:
                    demanda.status = 'Em andamento'
                else:
                    demanda.status = 'Concluída'
            my_day.append(demanda)

    # Check for demandas without data_prevista_execucao
    has_demandas_without_date = demandas.filter(data_prevista_execucao__isnull=True).exists()

    if request.method == 'POST':
        # Handle new demanda creation
        data = json.loads(request.body)
        nome = data.get('nome')
        descricao = data.get('descricao', '')
        prioridade = data.get('prioridade', 0)
        data_prevista_execucao = data.get('data_prevista_execucao')
        rotina = data.get('rotina', False)
        ordem_dia = data.get('ordem_dia', None)

        if nome and (data_prevista_execucao or rotina):
            Demandas.objects.create(
                nome=nome,
                descricao=descricao,
                prioridade=prioridade,
                data_prevista_execucao=data_prevista_execucao,
                rotina=rotina,
                ordem_dia=ordem_dia,
                atribuicao=request.servidor
            )
            return JsonResponse({'status': 200, 'message': 'Demanda criada com sucesso'})
        else:
            return JsonResponse({'status': 400, 'error': 'Dados incompletos'})

    context = {
        'demandas': demandas,
        'my_day': my_day,
        'has_demandas_without_date': has_demandas_without_date,
    }
    return render(request, 'tarefas/index.html', context)

@login_required
@csrf_exempt
def definir_data_demandas_nao_agendadas(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        demanda_id = data.get('demanda_id')
        data_prevista_execucao = data.get('data_prevista_execucao')

        try:
            demanda = Demandas.objects.get(id=demanda_id, atribuicao__user=request.user)
            demanda.data_prevista_execucao = data_prevista_execucao
            demanda.save()
            return JsonResponse({'status': 200, 'message': 'Data definida com sucesso'})
        except Demandas.DoesNotExist:
            return JsonResponse({'status': 404, 'error': 'Demanda não encontrada'})
        except Exception as e:
            return JsonResponse({'status': 500, 'error': str(e)})

    demandas_nao_agendadas = Demandas.objects.filter(atribuicao__user=request.user, data_prevista_execucao__isnull=True)
    context = {
        'demandas_nao_agendadas': demandas_nao_agendadas,
    }
    return render(request, 'tarefas/definir_data.html', context)

def toggle_task_completion(request):
    if request.method == 'POST':
        tarefa_id = request.POST.get('tarefa_id')
        tarefa = get_object_or_404(Tarefas, id=tarefa_id)
        tarefa.concluido = not tarefa.concluido
        tarefa.save()
        return JsonResponse({'status': 200, 'message': 'Tarefa atualizada com sucesso'})
    return JsonResponse({'status': 400, 'error': 'Método inválido'})

@csrf_exempt
@login_required
def change_demanda_priority(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        task_id = data.get('task_id')
        new_priority = data.get('new_priority')

        try:
            task = Demandas.objects.get(id=task_id, atribuicao__user=request.user)
            task.prioridade = new_priority
            task.save()
            return JsonResponse({'status': 200, 'message': 'Prioridade atualizada com sucesso'})
        except Demandas.DoesNotExist:
            return JsonResponse({'status': 404, 'error': 'Tarefa não encontrada'})
    return JsonResponse({'status': 400, 'error': 'Método inválido'})

@login_required
def atrasados(request):
    has_demandas_without_date = Demandas.objects.filter(atribuicao__user=request.user, data_prevista_execucao__isnull=True).exists()
    today = datetime.date.today()
    overdue_tasks = Demandas.objects.filter(
        atribuicao__user=request.user,
        data_prevista_execucao__lt=today,
        concluido=False  # Exclude completed tasks
    ).order_by('data_prevista_execucao')
    context = {'overdue_tasks': overdue_tasks, 'has_demandas_without_date': has_demandas_without_date}
    return render(request, 'tarefas/atrasados.html', context)

@login_required
def em_breve(request):
    has_demandas_without_date = Demandas.objects.filter(atribuicao__user=request.user, data_prevista_execucao__isnull=True).exists()
    today = datetime.date.today()
    upcoming_tasks = Demandas.objects.filter(
        atribuicao__user=request.user,
        data_prevista_execucao__gt=today
    ).order_by('data_prevista_execucao')
    context = {'upcoming_tasks': upcoming_tasks, 'has_demandas_without_date': has_demandas_without_date,}
    return render(request, 'tarefas/em_breve.html', context)

@login_required
def toggle_demanda_completion(request):
    if request.method == 'POST':
        # print('opa')
        data_json = request.body.decode('utf-8')
        data = json.loads(data_json)
        # print(data)        
        demanda_id = data.get('tarefa_id')
        # print(demanda_id)
        demandas = Demandas.objects.filter(atribuicao__user=request.user, id=demanda_id)
        # for dem in Demandas.objects.all():
            # print(dem.id)
            # print(int(dem.id) == int(demanda_id))
        if not demandas.exists():
            return JsonResponse({'status': 404, 'error': 'Demanda não encontrada'})
        demanda = demandas.first()
        # print(demanda)
        demanda.concluido = not demanda.concluido
        demanda.save()
        return JsonResponse({'status': 200, 'message': 'Tarefa atualizada com sucesso'})
    return JsonResponse({'status': 400, 'error': 'Método inválido'})

@login_required
def toggle_demanda_status(request):
    if request.method == 'POST':
        # print('opa')
        data_json = request.body.decode('utf-8')
        data = json.loads(data_json)
        # print(data)        
        demanda_id = data.get('tarefa_id')
        # print(demanda_id)
        demandas = Demandas.objects.filter(atribuicao__user=request.user, id=demanda_id)
        # for dem in Demandas.objects.all():
            # print(dem.id)
            # print(int(dem.id) == int(demanda_id))
        if not demandas.exists():
            return JsonResponse({'status': 404, 'error': 'Demanda não encontrada'})
        demanda = demandas.first()
        # print(demanda)
        demanda.status = data.get('status')
        demanda.save()
        return JsonResponse({'status': 200, 'message': 'Tarefa atualizada com sucesso'})
    return JsonResponse({'status': 400, 'error': 'Método inválido'})


@login_required
@csrf_exempt
def editar_demanda(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        demanda_id = data.get('demanda_id')
        nome = data.get('nome')
        descricao = data.get('descricao')
        prioridade = data.get('prioridade')
        data_prevista_execucao = data.get('data_prevista_execucao')

        try:
            demanda = Demandas.objects.get(id=demanda_id, atribuicao__user=request.user)
            demanda.nome = nome
            demanda.descricao = descricao
            demanda.prioridade = prioridade
            demanda.data_prevista_execucao = data_prevista_execucao
            demanda.save()
            return JsonResponse({'status': 200, 'message': 'Demanda atualizada com sucesso'})
        except Demandas.DoesNotExist:
            return JsonResponse({'status': 404, 'error': 'Demanda não encontrada'})
    return JsonResponse({'status': 400, 'error': 'Método inválido'})

@login_required
@csrf_exempt
def excluir_demanda(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        demanda_id = data.get('demanda_id')

        try:
            demanda = Demandas.objects.get(id=demanda_id, atribuicao__user=request.user)
            demanda.delete()
            return JsonResponse({'status': 200, 'message': 'Demanda excluída com sucesso'})
        except Demandas.DoesNotExist:
            return JsonResponse({'status': 404, 'error': 'Demanda não encontrada'})
    return JsonResponse({'status': 400, 'error': 'Método inválido'})

def concluidos(request):
    completed_tasks = Demandas.objects.filter(concluido=True, atribuicao__user=request.user ).order_by('-dt_concluido')
    return render(request, 'tarefas/concluidos.html', {'completed_tasks': completed_tasks})

@csrf_exempt
@login_required
def save_task_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            for task_data in data:
                task = Demandas.objects.get(id=task_data['id'], atribuicao__user=request.user)
                task.ordem_dia = task_data['ordem_dia']
                task.save()
            return JsonResponse({'status': 200, 'message': 'Ordenamento salvo com sucesso'})
        except Demandas.DoesNotExist:
            return JsonResponse({'status': 404, 'error': 'Demanda não encontrada'})
        except Exception as e:
            return JsonResponse({'status': 500, 'error': str(e)})
    return JsonResponse({'status': 400, 'error': 'Método inválido'})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import PainelAcompanhamentoDemandasForm

@login_required
def cadastrar_painel_acompanhamento(request):
    if request.method == 'POST':
        print(request.POST)
        # Cria o form sem o campo 'servidores' para evitar erro de validação
        post_data = request.POST.copy()
        if 'servidores' in post_data:
            servidores_ids = request.POST.get('servidores', '')
            ids = [int(s) for s in servidores_ids.split(',') if s.strip().isdigit()]
            post_data.setlist('servidores', ids)            
        form = PainelAcompanhamentoDemandasForm(post_data)
        if form.is_valid():
            painel = form.save(commit=False)
            painel.user_inclusao = request.user
            painel.save()
            # Atualiza os servidores selecionados via campo hidden            
            
            if ids:
                painel.servidores.set(Servidor.objects.filter(id__in=ids))
            else:
                painel.servidores.clear()
            form.save_m2m()
            return redirect('projetos:acompanhar')
        else:
            print(form.errors)
    else:
        form = PainelAcompanhamentoDemandasForm()
    return render(request, 'tarefas/cadastrar_painel_acompanhamento.html', {'form': form})

@login_required
def editar_painel_acompanhamento(request, painel_hash):
    painel = get_object_or_404(Painel_Acompanhamento_Demandas, hash=painel_hash)
    if request.method == 'POST':
        print(request.POST)
        post_data = request.POST.copy()
        if 'servidores' in post_data:
            servidores_ids = request.POST.get('servidores', '')
            ids = [int(s) for s in servidores_ids.split(',') if s.strip().isdigit()]
            post_data.setlist('servidores', ids)
        form = PainelAcompanhamentoDemandasForm(post_data, instance=painel)
        if form.is_valid():
            painel = form.save(commit=False)
            painel.user_inclusao = request.user
            painel.save()
            
            
            if ids:
                print(ids)
                painel.servidores.set(Servidor.objects.filter(id__in=ids))
            else:
                painel.servidores.clear()
            form.save_m2m()
            return redirect('projetos:acompanhar')
        else:
            print(form.errors)
    else:
        form = PainelAcompanhamentoDemandasForm(instance=painel)
    return render(request, 'tarefas/cadastrar_painel_acompanhamento.html', {'form': form, 'painel': painel})

from instituicoes.models import Servidor

@login_required
def api_servidores(request):
    q = request.GET.get('q', '').strip()
    servidores = Servidor.objects.all()
    if q:
        servidores = servidores.filter(nome__icontains=q)
    data = {
        "results": [
            {"id": s.id, "nome": s.nome}
            for s in servidores.order_by('nome')[:20]
        ]
    }
    return JsonResponse(data)

@login_required
def excluir_painel_acompanhamento(request, painel_hash):
    painel = get_object_or_404(Painel_Acompanhamento_Demandas, hash=painel_hash)
    if request.method == 'POST':
        painel.delete()
        return redirect('projetos:acompanhar')
    return render(request, 'tarefas/excluir_painel_acompanhamento.html', {'painel': painel})
