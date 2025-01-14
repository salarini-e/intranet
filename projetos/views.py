from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Projetos, Fases, Tarefas, Atividades
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