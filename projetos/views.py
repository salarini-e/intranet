import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Projetos, Fases, Tarefas, Atividades, Prioridade, Grupo
from .forms import ProjetosForm
from django.http import JsonResponse
from instituicoes.models import Servidor

@login_required
def index(request):
    projetos_responsavel = Projetos.objects.filter(responsavel__user=request.user)
    projetos_autorizado = Projetos.objects.filter(grupos__membros__user=request.user)
    projetos = projetos_responsavel | projetos_autorizado
    projetos = projetos.distinct()  
    context={
        'projetos': projetos,
        'form_projetos': ProjetosForm(initial={'user_inclusao': request.user})
    }
    return render(request, 'projetos/index.html', context)

@login_required
def kanbanboard(request, id):
    
    projeto = Projetos.objects.get(id=id)
    fases = Fases.objects.filter(projeto=projeto).order_by('ordem')
    servidores = [servidor for grupo in projeto.grupos.all() for servidor in grupo.membros.all()]
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
        print(dados)
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
        print(request.POST)
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
        print(dados)
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
    grupos = Grupo.objects.filter(responsavel__user = request.user)
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