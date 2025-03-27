from django.shortcuts import render, redirect
from ..models import AvaliacaoSistemaEL
from ..forms import AvaliacaoSistemaELForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
@login_required
def avaliacao_sistemas_el(request):
    print("Request method:", request.method)    
    sistemas = [
        {'nome': 'Protocolo', 'slug': slugify('Protocolo')},
        {'nome': 'Tributário', 'slug': slugify('Tributário')},
        {'nome': 'GMA', 'slug': slugify('GMA')}
    ]  # List of systems with slugs
    errors = []

    if request.method == 'POST':
        print("POST data:", request.POST)
        try:
            usuario_nome = request.POST.get('usuario_nome')
            usuario_matricula = request.POST.get('usuario_matricula')

            for sistema in sistemas:
                if request.POST.get(f'{sistema["slug"]}_usa_sistema') == 'Não':
                    continue
                slug = sistema['slug']
                form_data = {
                    'sistema': sistema['slug'],
                    'usuario_nome': usuario_nome,
                    'usuario_matricula': usuario_matricula,
                    'satisfacao': request.POST.get(f'{slug}_satisfacao'),
                    'houve_lentidao': request.POST.get(f'{slug}_tempo_resposta'),
                    'sugestao': request.POST.get(f'{slug}_sugestao'),
                    'usuario_inclusao': User.objects.get(username=request.user.username)  # Assuming you want to save the user who submitted the form,
                }
                print("Form data:", form_data)
                form = AvaliacaoSistemaELForm(form_data)
                if form.is_valid():
                    print("Form is valid")
                    form.save()
                else:
                    print("Form errors:", form.errors)
                    errors.append((sistema['nome'], form.errors))  # Collect errors for each system
        except Exception as e:
            print(f"Error: {e}")
        if not errors:
            print("Redirecting to avaliacao_sistemas_el")
            return redirect('formfacil:avaliacao_sistemas_el')

    return render(request, 'formfacil/formfacil_form_el.html', {'sistemas': sistemas, 'errors': errors})
