from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Projetos, Fases, Tarefas, Atividades, Prioridade
from .forms import ProjetosForm
from django.http import JsonResponse
from instituicoes.models import Servidor

@login_required
def index(request):
    context={
        'projetos': Projetos.objects.all(),
        'form_projetos': ProjetosForm(initial={'user_inclusao': request.user})
    }
    return render(request, 'projetos/index.html', context)

@login_required
def kanbanboard(request, id):
    projeto = Projetos.objects.get(id=id)
    fases = Fases.objects.filter(projeto=projeto).order_by('ordem')
    context = {
        'projeto': projeto,
        'fases': fases,        
    }
    print(context)
    return render(request, 'projetos/kanban.html', context)

@login_required
def api_criar_projeto(request):
    if request.method == 'POST':
        form = ProjetosForm(request.POST)
        print(request.POST)
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
        card_id = dados['card_id']
        tarefa = Tarefas.objects.get(id=card_id)
        tarefa.nome = dados['nome'] if dados['nome'] else None
        tarefa.descricao = dados['descricao'] if dados['descricao'] else None
        tarefa.data_inicio = dados['data_inicio'] if dados['data_inicio'] else None
        tarefa.data_fim = dados['data_fim'] if dados['data_fim'] else None
        # tarefa.prioridade = Prioridade.objects.get(id=dados['prioridade'])
        tarefa.save()
        return JsonResponse({'status': 200, 'card': {'id': tarefa.id,'nome': tarefa.nome, 'descricao': tarefa.descricao, 'data_inicio': tarefa.data_inicio, 'data_fim': tarefa.data_fim}})
    return JsonResponse({'status': 403, 'error': 'Método inválido'})