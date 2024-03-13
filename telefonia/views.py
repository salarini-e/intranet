from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from .models import Ramal
from .forms import RamalForm

@login_required
def index(request):
    ramais = Ramal.objects.all()
    context={
        'ramais': ramais
    }
    return render(request, 'telefonia/index.html', context)

@login_required
def criarRamal(request):
    #apenas telefonista pode usar essa função
    #fazer um decorator para isso
    if request.method == 'POST': 
              
        for i in request.POST:
            if request.POST[i] == '' and i != 'webex':
                return JsonResponse({'status': 400, 'message': 'Preencha todos os campos!'})
        
        form = RamalForm(request.POST)                
        if form.is_valid():
            ramal=form.save()
            return JsonResponse({'status': 200, 
                                 'message': f'Ramal {ramal.numero} cadastrado com sucesso!',
                                 'ramal': {'secretaria': form.cleaned_data['secretaria'].nome, 
                                           'setor': form.cleaned_data['setor'].nome, 
                                           'referencia': form.cleaned_data['referencia'], 
                                           'numero': form.cleaned_data['numero'], 
                                           'webex': form.cleaned_data['webex']
                                           }
                                })
        
        else:
            print(form.errors)
            return JsonResponse({'status': 400, 'message': 'Erro ao cadastrar ramal!'})
        return JsonResponse({'status': 200})
    else:
        return JsonResponse({'status': 403})