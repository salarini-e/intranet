from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from instituicoes.models import Secretaria, Setor, Servidor
from .models import Ramal, Telefonista
from .forms import RamalForm
from django.http import HttpResponseForbidden
from django.contrib import messages

@login_required
def index(request):
    ramais = Ramal.objects.all()
    context={
        'ramais': ramais,
        'secretarias': Secretaria.objects.all(),
        'telefonista': Telefonista.objects.filter(servidor = Servidor.objects.get(user=request.user))
    }
    return render(request, 'telefonia/index.html', context)

@login_required
def getSetores(request, id):
    secretaria = Secretaria.objects.get(id=id)
    setores = Setor.objects.filter(secretaria=secretaria)
    setores = [{'id': setor.id, 'nome': setor.nome} for setor in setores]
    return JsonResponse({'setores': setores})
                        
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
                                           'responsavel': form.cleaned_data['responsavel'], 
                                           'numero': form.cleaned_data['numero'],                                            
                                           }
                                })
        
        else:
            print(form.errors)
            return JsonResponse({'status': 400, 'message': 'Erro ao cadastrar ramal!'})
        return JsonResponse({'status': 200})
    else:
        return JsonResponse({'status': 403})
    
@login_required
def editar_ramal(request, ramal_id):
    #apenas telefonista pode usar essa função
    #fazer um decorator para isso
    telefonista = Telefonista.objects.filter(servidor = Servidor.objects.get(user=request.user))
    if not telefonista.exists() or not request.user.is_superuser:
        return HttpResponseForbidden('Você não tem permissão para acessar essa página!')
    if request.method == 'POST': 
        ramal = Ramal.objects.get(id=ramal_id)
        form = RamalForm(request.POST, instance=ramal)                
        if form.is_valid():
            ramal=form.save()
            messages.success(request, f'Ramal {ramal.numero} editado com sucesso!')
            return redirect('telefonia:index')                    
    else:
        ramal = Ramal.objects.get(id=ramal_id)
        form = RamalForm(instance=ramal)
    conetxt = {
            'form': form,
            'title': 'Editar ramal'
    }
    return render(request, 'telefonia/editar_ramal.html', conetxt)
