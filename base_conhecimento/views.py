from django.shortcuts import render, get_object_or_404
from .models import Topico, Subtopico

# Create your views here.
def index(request):
    topicos = Topico.objects.filter(ativo= True)
    context = {
        'topicos': topicos
    }
    return render(request, 'base_conhecimento/index.html', context)

def subtopicos(request, topico_id):
    # Obter o tópico selecionado ou retornar um erro 404 se não existir
    topico = get_object_or_404(Topico, id=topico_id, ativo=True)
    
    # Filtrar os subtopicos associados ao tópico selecionado
    subtopicos = Subtopico.objects.filter(topico_id=topico)
    
    context = {
        'topico': topico,
        'subtopicos': subtopicos
    }
    return render(request, 'base_conhecimento/subtopicos.html', context)