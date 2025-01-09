from django.shortcuts import render

# Create your views here.
def kanbanboard(request):
    return render(request, 'gestao_de_projetos/kanban.html')