from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib import messages

from .models import Meta_Servidores
from datetime import datetime
import pandas as pd

from .functions.validation import validate_cpf

@login_required
def index(request):
    secretarias = Secretaria.objects.all()
    context = {
        'secretarias': secretarias
    }
    return render(request, 'instituicoes/index.html', context)

@login_required
def api(request):
    return JsonResponse({'status': 200})

@login_required
def criar_secretaria(request):
    if request.method == 'POST':
        form = SecretariaForm(request.POST)        
        if form.is_valid():
            secretaria = form.save()
            secretaria.user_inclusao = request.user
            secretaria.save()
            messages.success(request, f'Secretaria {secretaria.nome} cadastrada com sucesso!')
            return redirect('ins:index')            
    else:
        form = SecretariaForm(initial={'user_inclusao': request.user.id})
    context = {
        'form': form,
        'title': 'Adicionar secretaria',
        'url_back': redirect('ins:index').url
    }
    return render(request, 'instituicoes/form.html', context)

@login_required
def editar_secretaria(request, id):
    secretaria = Secretaria.objects.get(id=id)
    if request.method == 'POST':
        form = SecretariaForm(request.POST, instance=secretaria)        
        if form.is_valid():
            secretaria = form.save()
            secretaria.user_inclusao = request.user
            secretaria.save()
            messages.success(request, f'Secretaria {secretaria.nome} cadastrada com sucesso!')
            return redirect('ins:index')            
    else:
        form = SecretariaForm(instance=secretaria)
    context = {
        'form': form,
        'title': 'Editar secretaria'
    }
    return render(request, 'instituicoes/form.html', context)

@login_required
def setores(request, id):    
    secretaria = Secretaria.objects.get(id=id)
    setores = Setor.objects.filter(secretaria = secretaria)
    context = {        
        'secretaria': secretaria,
        'setores': setores
    }
    return render(request, 'instituicoes/setores.html', context)

@login_required
def criar_setor(request, id):
    secretaria = Secretaria.objects.get(id=id)
    if request.method == 'POST':
        form = SetorForm(request.POST)        
        if form.is_valid():
            setor = form.save()
            setor.user_inclusao = request.user
            setor.save()
            messages.success(request, f'Setor {setor.nome} cadastrada com sucesso!')
            return redirect('ins:setores', id=secretaria.id)            
    else:
        form = SetorForm(initial={'secretaria': secretaria.id ,'user_inclusao': request.user.id})
    context = {
        'form': form,
        'secretaria': secretaria,
        'title': f'Adicionar setor a {secretaria.apelido}',
        'url_back': redirect('ins:setores', id=secretaria.id).url
    }
    return render(request, 'instituicoes/form.html', context)

@login_required
def editar_setor(request, id):
    setor = Setor.objects.get(id=id)
    secretaria = setor.secretaria
    if request.method == 'POST':
        form = SetorForm(request.POST, instance=setor)        
        if form.is_valid():
            setor = form.save()
            setor.user_inclusao = request.user
            setor.save()
            messages.success(request, f'Setor {setor.nome} cadastrada com sucesso!')
            return redirect('ins:setores')            
    else:
        form = SetorForm(instance=setor)
    context = {
        'form': form,
        'title': f'Editar {setor.nome}',
        'url_back': redirect('ins:setores', id=secretaria.id).url
    }
    return render(request, 'instituicoes/form.html', context)

@login_required
def adicionar_servidor(request, id, id_setor):
    setor = Setor.objects.get(id=id_setor)
    if request.method == 'POST':
        form = ServidorForm(request.POST)        
        if form.is_valid():
            servidor = form.save()
            servidor.setor = setor
            servidor.user = form.create_user()
            servidor.user_inclusao = request.user
            servidor.save()
            messages.success(request, f'Servidor {servidor.nome} cadastrada com sucesso!')
            return redirect('ins:setores', setor.secretaria.id)            
    else:
        form = ServidorForm(initial={'setor': setor.id, 'user_inclusao': request.user.id})
    context = {
        'form': form,
        'title': 'Adicionar servidor',
        'url_back': redirect('ins:setores', setor.secretaria.id).url
    }
    return render(request, 'instituicoes/form.html', context)

@login_required 
def getSetores(request, id):
    setores = Setor.objects.filter(secretaria=id).values('id', 'nome')
    return JsonResponse({'setores': list(setores)})

@login_required
def get_servidores_from_site(request):
    if True:
        return HttpResponse("Você não tem autorização!")
    arquivo_excel = '/home/sistemas/intranet/site/intranet/grdData.xlsx'    
    df = pd.read_excel(arquivo_excel)
    
    for index, row in df.iterrows():

        nome = row['Nome']
        matricula = row['Matricula']
        lotacao = row['Lotacao']
        cpf = row['CPF']
        

        if Meta_Servidores.objects.filter(matricula=matricula).exists():
            continue

        
        servidor = Meta_Servidores(
            nome=nome,
            matricula=matricula,
            secretaria=lotacao,
            cpf=cpf,
            dt_inclusao=datetime.now()  # Data de inclusão definida como o momento atual
        )
                
        servidor.save()

    return HttpResponse("Dados importados com sucesso!")

def api_get_servidor(request):
    dict_mapeamento = {
    'SEC MUNIC FINANCAS,PLANEJAMENTO,DESENV ECON GESTAO': 'Secretaria Municipal de Finanças, Planejamento, Desenvolvimento Econômico e Gestão',
    'CONTROLADORIA GERAL': 'Controladoria Geral',
    'PROCURADORIA GERAL': 'Procuradoria Geral do Município',
    'SECRETARIA MUNICIPAL DA CASA CIVIL - EGCP': 'Secretaria Municipal da Casa Civil',
    'SECRETARIA MUN DE AGRICULTURA E DES RURAL': 'Secretaria Municipal de Agricultura e Desenvolvimento Rural',
    'SEC MUN DE ASSIST SOCIAL DIREITOS HUMANOS TRABALHO': 'Secretaria Municipal de Assistência Social, Direitos Humanos, Trabalho e Políticas Públicas para a Juventude',
    'SEC MUN CIENCIA,TEC,INOV E ENSINO PROF. E SUPERIOR': 'Secretaria Municipal de Ciência, Tecnologia, Inovação e Educação Profissionalizante e Superior',
    'SECRETARIA MUN DE CULTURA': 'Secretaria Municipal de Cultura',
    'SECRETARIA MUNICIPAL DE DEFESA CIVIL': 'Secretaria Municipal de Defesa Civil',
    'SECRETARIA MUNICIPAL DE EDUCACAO': 'Secretaria Municipal de Educação',
    'SEC MUN DE ESPORTES E LAZER': 'Secretaria Municipal de Esportes e Lazer',
    'SECRETARIA MUNICIPAL DE GOVERNO': 'Secretaria de Governo',
    'SECRETARIA MUNICIPAL DE INFRAESTRUTURA E LOGISTICA': 'Secretaria Municipal de Infraestrutura e Logística',
    'SEC MUN DE MEIO AMBIENTE E DESENV URBANO SUSTENTAV': 'Secretaria Municipal de Meio Ambiente e Desenvolvimento Urbano Sustentável',
    'SECRETARIA MUNICIPAL DE OBRAS': 'Secretaria Municipal de Obras',
    'SEC MUN DE ORDEM E MOBILIDADE URBANA': 'Secretaria Municipal de Ordem e Mobilidade Urbana',
    'SECRETARIA MUNICIPAL DE SAUDE': 'Secretaria Municipal de Saúde',
    'SECRETARIA MUN DE SERVICOS PUBLICOS': 'Secretaria Municipal de Serviços Públicos',
    'SECRETARIA MUN DE TURISMO E MARKETING DA CIDADE': 'Secretaria Municipal de Turismo e Marketing da Cidade',
    'SUBPREFEITURA DE CAMPO DO COELHO': 'Subprefeitura de Campo do Coelho',
    'SUBPREFEITURA DE CONSELHEIRO PAULINO': 'Subprefeitura de Conselheiro Paulino',
    'SUBPREFEITURA DE LUMIAR E SAO PEDRO DA SERRA': 'Subprefeitura de Lumiar e São Pedro da Serra',
    'SUBPREFEITURA DE OLARIA E CONEGO': 'Subprefeitura de Olaria e Cônego',
    'FUNDACAO D. JOAO VI DE NOVA FRIBURGO': 'Fundação Dom João VI de Nova Friburgo',
    'SECRETARIA MUNICIPAL DE POLITICAS SOBRE DROGAS': 'Secretaria Municipal de Políticas Sobre Drogas',
    'CRAS': 'CRAS',
    'CREAS': 'CREAS',
    'QUADRO SUPLEMENTAR-LEI COMPLEM.30/2007': 'QUADRO SUPLEMENTAR-LEI COMPLEM.30/2007'
}
    matricula = request.GET.get('matricula', None)
    # Remove leading zeros from matricula if present
    if matricula is not None:
        matricula = matricula.lstrip('0')
    if matricula is not None:
        try:
            servidor = Meta_Servidores.objects.get(matricula=matricula)
            print(servidor.secretaria)
            print(dict_mapeamento[servidor.secretaria])
            try:
                secretaria = Secretaria.objects.get(nome=dict_mapeamento[servidor.secretaria])
                setores = Setor.objects.filter(secretaria=secretaria)
                print(secretaria)
                print(setores)
            except Exception as e:
                print(e)
                pass
            return JsonResponse({'nome': servidor.nome, 'cpf': servidor.cpf, 'secretaria': {'id': secretaria.id, 'nome': secretaria.nome}, 'setores': [{'id': setor.id, 'nome': setor.nome} for setor in setores]})
            # secretaria = Secretaria.objects.get(nome=dict_mapeamento[servidor.secretaria])
            # setores = Setor.objects.filter(secretaria=secretaria)
            # return JsonResponse({'nome': servidor.nome, 'cpf': servidor.cpf, 'secretaria': {'id': secretaria.id, 'nome': secretaria.nome, 'setores': [{'id': setor.id, 'nome': setor.nome} for setor in setores]}})
        except Meta_Servidores.DoesNotExist:
            return JsonResponse({'error': 'Servidor not found'}, status=404)
    else:
        return JsonResponse({'error': 'No matricula provided'}, status=400)
    
def api_teste_cpf(request):
    cpf = request.GET.get('cpf', None)    
    return JsonResponse({'msg': validate_cpf(cpf)})