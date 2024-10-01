from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib import messages
from instituicoes.models import Servidor
from .models import Chamado

class Email_Chamado:
    def __init__(self, chamado):
        # self.servidor = servidor
        self.chamado = chamado

    def create_email(self, email_to, email_template_name):    
        c = {
            "email": email_to,
            'domain': 'intranet.novafriburgo.rj.gov.br',
            'chamado': self.chamado,
            'site_name': 'Intranet',                            
            'url': redirect('chamados:detalhes', hash=self.chamado.hash).url,
            'protocol': 'https',
        }
        email = render_to_string(email_template_name, c)
        return email

    def criar_notificacao(self, subject):
        pass

    def atribuir_atendente(self, subject): 
        email_template = self.create_email(self.chamado.profissional_designado.servidor.email, 'chamados/emails/atribuir_atendente.txt')   
        email_to = self.chamado.profissional_designado.servidor.email

        self.criar_notificacao(subject)

        msg = {
            'subject': subject,
            'email_template': email_template,
            'email_to': email_to
        }
        return self.enviar(msg)
    
    

    def chamado_criado(self): 
        email_template = self.create_email(self.chamado.requisitante.email, 'chamados/emails/criar_chamado.txt')   
        email_to = self.chamado.requisitante.email
        print(email_template)
        self.criar_notificacao('Chamado criado com sucesso!')

        msg = {
            'subject': 'Chamado criado com sucesso!',
            'email_template': email_template,
            'email_to': email_to
        }
        return self.enviar(msg)

    def notificar_solicitante(self, subject):
        email_template = self.create_email(self.chamado.requisitante.email, 'chamados/emails/notificar_solicitante.txt')   
        email_to = self.chamado.requisitante.email
        
        self.criar_notificacao(subject)

        msg = {
            'subject': subject,
            'email_template': email_template,
            'email_to': email_to
        }
        return self.enviar(msg)

    def enviar(self, msg):
        try:
            send_mail(msg['subject'], 
                      msg['email_template'], 
                      msg['email_to'], 
                      (msg['email_to'],), 
                      fail_silently=False)
        except Exception as e:
            print(e)
            return 'Falha ao enviar email.', 400
        return 'Email enviado com sucesso.', 200


def enviar_email_atendente(servidor, chamado):
          
    subject = "Novo chamado atribuido a você."
    email_template_name = "chamados/atendente_atribuido.txt"
    c = {
        "email": servidor.email,
        'domain': 'intranet.novafriburgo.rj.gov.br',
        'chamado': chamado,
        'site_name': 'Intranet',                
        "servidor": servidor,
        'url': redirect('chamados:detalhes', hash=chamado.hash).url,
        'protocol': 'https',
    }
    email = render_to_string(email_template_name, c)
    try:
        send_mail(subject, email, servidor.email, [servidor.email], fail_silently=False)
    except Exception as e:
        print(e)
        return 'Falha ao enviar email.', 400
    return 'Email enviado com sucesso.', 200

from django.core.paginator import Paginator
from .models import Servidor, Atendente, Chamado, Secretaria, Setor

def obter_filtros(request):
    if request.method == 'POST':
        filtros = {
            'protocolo': request.POST.get('protocolo', ''),
            'secretaria': request.POST.get('secretaria', ''),
            'setor': request.POST.get('setor', ''),
            'requisitante': request.POST.get('requisitante', ''),
            'dt_solicitacao': request.POST.get('dt_solicitacao', ''),
            'designado': request.POST.get('designado', ''),
            'prioridade': request.POST.get('prioridade', ''),
            'status': request.POST.get('status', '')
        }
        request.session['filtros'] = filtros
    else:
        filtros = request.session.get('filtros', {})
    return filtros

def verificar_filtrado(request, filtros):
    return any(value for value in filtros.values())

def obter_chamados(request, filtros):
    servidor = Servidor.objects.get(user=request.user)
    atendente = Atendente.objects.filter(servidor=servidor).first()
    if atendente:
        chamados = Chamado.objects.exclude(status__in=['3', '4']).order_by('-dt_inclusao')        
        if filtros:
            chamados = Chamado.objects.filter().order_by('-dt_inclusao')
            chamados = aplicar_filtros(chamados, filtros)
    
    else:
        chamados = Chamado.objects.exclude(status__in=['3', '4']).filter(requisitante=servidor).order_by('-dt_inclusao')        
        if filtros:
            chamados = Chamado.objects.filter(requisitante=servidor).order_by('-dt_inclusao')
            chamados = aplicar_filtros(chamados, filtros)
    

    
    return chamados

def aplicar_filtros(chamados, filtros):
    if filtros['protocolo']:
        chamados = chamados.filter(protocolo__icontains=filtros['protocolo'])
    if filtros['secretaria']:
        chamados = chamados.filter(setor__secretaria_id=filtros['secretaria'])
    if filtros['setor']:
        chamados = chamados.filter(setor_id=filtros['setor'])
    if filtros['requisitante']:
        chamados = chamados.filter(requisitante_id=filtros['requisitante'])
    if filtros['dt_solicitacao']:
        chamados = chamados.filter(dt_solicitacao=filtros['dt_solicitacao'])
    if filtros['designado']:
        if filtros['designado']!='n/h':
            chamados = chamados.filter(profissional_designado_id=filtros['designado'])
        else:
            chamados = chamados.filter(profissional_designado__isnull=True)
    if filtros['prioridade'] and filtros['prioridade']!='n':
        chamados = chamados.filter(prioridade=filtros['prioridade'])
    if filtros['status']:
        chamados = chamados.filter(status=filtros['status'])
    
    return chamados

def obter_atendente(request):
    servidor = Servidor.objects.get(user=request.user)
    return Atendente.objects.filter(servidor=servidor).first()

def obter_opcoes_filtros():
    return {
        'secretarias': Secretaria.objects.all(),
        'setores': Setor.objects.all(),
        'requisitantes': Servidor.objects.all(),
        'atendentes': Atendente.objects.all(),
        'prioridades': Chamado.PRIORIDADE_CHOICES,
        'status': Chamado.STATUS_CHOICES
    }

def paginar_chamados(request, chamados):
    paginator = Paginator(chamados, 50)  # Mostra 10 chamados por página
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)

from datetime import datetime, timedelta

def verificar_chamados_atrasados():
    # Obtém a data atual
    data_atual = datetime.now().date()
    
    # Calcula a data 30 dias atrás
    trinta_dias_atras = data_atual - timedelta(days=30)
    
    # Verifica os chamados abertos que já passaram da data agendada
    chamados_atrasados_data_agendada = Chamado.objects.filter(dt_agendamento__lt=data_atual, status='Aberto')
    
    # Verifica os chamados abertos há mais de 30 dias
    chamados_atrasados_trinta_dias = Chamado.objects.filter(dt_inclusao__lt=trinta_dias_atras, status='Aberto')
    
    # Retorna True se houver algum chamado atrasado, caso contrário, False
    return chamados_atrasados_data_agendada.exists(), chamados_atrasados_trinta_dias.exists()

def carregar_novos_filtros(request):
    print(request.POST)
    agentes = request.POST['agentes']
    #     status = request.POST['status']
    #     tiposChamados = request.POST['tiposChamados']
    #     prioridade = request.POST['prioridade']
    #     criadoEm = request.POST['criadoEm']
    #     fechadoEm = request.POST['fechadoEm']
    #     resolvidoEm = request.POST['resolvidoEm']
    #     venceEm = request.POST['venceEm']
    #     # print("Agentes", agentes)
    agentesLista = agentes.split(';')
    #     statusLista = status.split(';')
    #     tiposChamadosLista = tiposChamados.split(';')
    #     prioridadeLista = prioridade.split(';')
    agentesLista.pop()
    agentes = []
    request.session['agentes']=None
    for id_agente in agentesLista:
        
        agente = Atendente.objects.get(id=id_agente)
        agentes.append({'id': agente.id, 'nome': agente.nome_servidor})
    #     statusLista.pop()
    #     tiposChamadosLista.pop()
    #     prioridadeLista.pop()
    #     # print("Lista Agentes", agentesLista)
        request.session['agentes'] = agentes
    #     request.session['status'] = statusLista
    #     request.session['tiposChamados'] = tiposChamadosLista
    #     request.session['prioridade'] = prioridadeLista
    #     request.session['criadoEm'] = criadoEm
    #     request.session['fechadoEm'] = fechadoEm
    #     request.session['resolvidoEm'] = resolvidoEm
    #     request.session['venceEm'] = venceEm
    # else:
    #     try:
    #         agentes = request.session.get('agentes', '')
    #         status = request.session.get('status', '')
    #         tiposChamados = request.session.get('tiposChamados', '')
    #         prioridade =  request.session.get('prioridade', '')
    #         criadoEm =  request.session.get('criadoEm', '')
    #         fechadoEm = request.session.get('fechadoEm', '')
    #         resolvidoEm = request.session.get('resolvidoEm', '')
    #         venceEm = request.session.get('venceEm', '')
    #     except Exception as E:
    #         print(E)
    #         pass

    pass


def make_query_chamados(request):

    sql = "SELECT * FROM chamados_chamado WHERE hash!=''"
    str_id_agentes = ''
    print(request.session['agentes']    )
    for agente in request.session['agentes']:
        print(agente)
        str_id_agentes += str(agente['id'])+','
    
    if  'agentes' in request.session:
        sql += f' AND atendente_id IN ({str_id_agentes[:-1]})'
    
    sql+= ' ORDER BY dt_inclusao DESC'
    return sql 
 
from django.db import connection, models
def filtrar_chamados(request):
   
    if request.user.is_superuser:
        
        sql = make_query_chamados(request)
        chamados = Chamado.objects.all().order_by('-dt_inclusao')
    else:
        # Se não for superusuário, lista apenas os chamados do requisitante
        chamados = Chamado.objects.filter(user_inclusao__user=request.user).order_by('-dt_inclusao')

    with connection.cursor() as cursor:
        cursor.execute(sql)
        results = cursor.fetchall()

        queryset = []
        for row in results:
            print(row, '\n')
            data=[
                # 'id': row[0],
            ]
            # chamado = Chamado(**data)
            # queryset.append(chamado)
            # queryset = sorted(queryset, key=lambda x: (x.dt_alteracao if x.dt_alteracao else x.dt_solicitacao), reverse=True)
    

    return chamados
