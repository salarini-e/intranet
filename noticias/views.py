from django.shortcuts import render
from .models import Noticias
def detalhe(request, noticia_id):
    noticia = Noticias.objects.get(id=noticia_id)
    context = {
        'noticia': noticia
    }
    return render(request, 'noticias/detalhe.html', context)