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
from .models import Chamado, TipoChamado
from django.utils import timezone


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
    
    def create_email_to_msg(self, email_to, email_template_name, mensagem):    
        c = {
            "email": email_to,
            'domain': 'intranet.novafriburgo.rj.gov.br',
            'chamado': self.chamado,
            'mensagem': mensagem,
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
        # print(email_template)
        self.criar_notificacao('Chamado criado com sucesso!')

        msg = {
            'subject': 'Chamado criado com sucesso!',
            'email_template': email_template,
            'email_to': email_to
        }
        return self.enviar(msg)
    
    def mensagem_criada(self, mensagem): 
        email_template = self.create_email_to_msg(self.chamado.requisitante.email, 'chamados/emails/mensagem_criada.txt', mensagem)   
        email_to = self.chamado.requisitante.email
        # print(email_template)

        msg = {
            'subject': f'Nova mensgem para o chamado {self.chamado.n_protocolo}!',
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
        chamados = Chamado.objects.exclude(status__in=['3', '4']).order_by('-dt_atualizacao')        
        if filtros:
            chamados = Chamado.objects.filter().order_by('-dt_atualizacao')
            chamados = aplicar_filtros(chamados, filtros)
    
    else:
        chamados = Chamado.objects.exclude(status__in=['3', '4']).filter(requisitante=servidor).order_by('-dt_atualizacao')        
        if filtros:
            chamados = Chamado.objects.filter(requisitante=servidor).order_by('-dt_atualizacao')
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
    paginator = Paginator(chamados, 25) 
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
    # print(request.POST)
    agentes = request.POST['agentes']
    status = request.POST['status']
    tiposChamados = request.POST['tiposChamados']
    prioridade = request.POST['prioridade']
    criadoEm = request.POST['criadoEm']
    fechadoEm = request.POST['fechadoEm']
    agendadoPara = request.POST['agendadoPara']
    atualizacaoEm = request.POST['atualizacaoEm']


    agentesLista = agentes.split(';')
    statusLista = status.split(';')
    tiposChamadosLista = tiposChamados.split(';')
    prioridadeLista = prioridade.split(';')
    agentesLista.pop()
    statusLista.pop()
    tiposChamadosLista.pop()
    prioridadeLista.pop()

    agentes = []
    status =[]
    tiposChamados = []
    prioridades = []

    request.session['agentes']=None
    for id_agente in agentesLista:
        agente = Atendente.objects.get(id=id_agente)
        agentes.append({'id': agente.id, 'nome': agente.nome_servidor})
    
    request.session['status']=None
    status_choices = dict(Chamado.STATUS_CHOICES)
    for id_status in statusLista:
        if id_status in status_choices:
            status.append({'id': id_status, 'nome': status_choices[id_status]})
   
    request.session['tiposChamados'] = None
    for id_tipos_chamados in tiposChamadosLista:
        tipoChamado = TipoChamado.objects.get(id=id_tipos_chamados)
        tiposChamados.append({'id': tipoChamado.id, 'nome': tipoChamado.nome})
   
    request.session['prioridade'] = None
    prioridades_choices = dict(Chamado.PRIORIDADE_CHOICES)
    for id_prioridade in prioridadeLista:
        if id_prioridade in prioridades_choices:
            prioridades.append({'id': id_prioridade, 'nome': prioridades_choices[id_prioridade]})

    request.session['agentes'] = agentes
    request.session['status'] = status
    request.session['tiposChamados'] = tiposChamados
    request.session['prioridade'] = prioridades
    # print("Prioridades: ", prioridades)
    request.session['criadoEm'] = criadoEm
    request.session['fechadoEm'] = fechadoEm
    request.session['agendadoPara'] = agendadoPara
    request.session['atualizacaoEm'] = atualizacaoEm
    # else:
    #     try:
    #         agentes = request.session.get('agentes', '')
    #         status = request.session.get('status', '')
    #         tiposChamados = request.session.get('tiposChamados', '')
    #         prioridade =  request.session.get('prioridade', '')
    #         criadoEm =  request.session.get('criadoEm', '')
    #         fechadoEm = request.session.get('fechadoEm', '')
    #         agendadoPara = request.session.get('agendadoPara', '')
    #         atualizacaoEm = request.session.get('atualizacaoEm', '')
    #     except Exception as E:
    #         print(E)
    #         pass

    pass


def calcular_tempo_criacao(selecao_tempo):
    agora = timezone.now()
    
    if selecao_tempo == '5min':
        return agora - timedelta(minutes=5)
    elif selecao_tempo == '15min':
        return agora - timedelta(minutes=15)
    elif selecao_tempo == '30min':
        return agora - timedelta(minutes=30)
    elif selecao_tempo == '1hora':
        return agora - timedelta(hours=1)
    elif selecao_tempo == '4horas':
        return agora - timedelta(hours=4)
    elif selecao_tempo == '12horas':
        return agora - timedelta(hours=12)
    elif selecao_tempo == '24horas':
        return agora - timedelta(days=1)
    elif selecao_tempo == 'Hoje':
        return agora.replace(hour=0, minute=0, second=0, microsecond=0)
    elif selecao_tempo == 'Ontem':
        return (agora - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    elif selecao_tempo == 'EstaSemana':
        return agora - timedelta(days=agora.weekday())  # Início da semana
    elif selecao_tempo == 'EsteMes':
        return agora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    elif selecao_tempo == '7dias':
        return agora - timedelta(days=7)
    elif selecao_tempo == '30dias':
        return agora - timedelta(days=30)
    elif selecao_tempo == '60dias':
        return agora - timedelta(days=60)
    elif selecao_tempo == '180dias':
        return agora - timedelta(days=180)
    else:
        return ''
    

def make_query_chamados(request):
    sql = "SELECT * FROM chamados_chamado WHERE hash!=''"
    # CONCATENAR CASO TENHA AGENTE SELECIONADO
    if 'agentes' in request.session and request.session['agentes'] is not None:
        str_id_agentes = ''
        for agente in request.session['agentes']:
            str_id_agentes += str(agente['id']) + ','

        if str_id_agentes:
            sql += f" AND profissional_designado_id IN ({str_id_agentes[:-1]})"

    # CONCATENAR CASO TENHA STATUS SELECIONADO
    if 'status' in request.session and request.session['status'] is not None:
        str_id_status = ''
        for status_item in request.session['status']:
            str_id_status += str(status_item['id']) + ','

        if str_id_status:
            sql += f" AND status IN ({str_id_status[:-1]})"

    # CONCATENAR CASO TENHA TIPO DO CHAMADO SELECIONADO
    if 'tiposChamados' in request.session and request.session['tiposChamados'] is not None:
        str_id_tiposChamados = ''
        for tipoChamado in request.session['tiposChamados']:
            str_id_tiposChamados += str(tipoChamado['id']) + ','

        if str_id_tiposChamados:
            sql += f" AND tipo_id IN ({str_id_tiposChamados[:-1]})"

    # CONCATENAR CASO TENHA PRIORIDADE SELECIONADA
    if 'prioridade' in request.session and request.session['prioridade'] is not None:
        str_id_prioridade = ''
        
        for prioridade_item in request.session['prioridade']:
            if prioridade_item['id'] == '-':
                str_id_prioridade += "'"+str(prioridade_item['id']) + "',"
            else:
                str_id_prioridade += str(prioridade_item['id']) + ','

        if str_id_prioridade:
            sql += f" AND prioridade IN ({str_id_prioridade[:-1]})"

    # if 'criadoEm' in request.session and request.session['criadoEm'] is not None:
    #     tempo_limite_criadoEm = calcular_tempo_criacao(request.session['criadoEm'])
    #     if tempo_limite_criadoEm!='':
    #         sql += f" AND dt_inclusao >= '{tempo_limite_criadoEm.strftime('%Y-%m-%d %H:%M:%S')}'"

    # if 'fechadoEm' in request.session and request.session['fechadoEm'] is not None:
    #     tempo_limite_fechadoEm = calcular_tempo_criacao(request.session['fechadoEm'])
    #     if tempo_limite_fechadoEm!='':
    #         sql += " AND dt_fechamento IS NOT NULL"
    #         sql += f" AND dt_fechamento >= '{tempo_limite_fechadoEm.strftime('%Y-%m-%d %H:%M:%S')}'"

    if 'criadoEm' in request.session and request.session['criadoEm'] is not None:
        # tempo_limite_criadoEm = calcular_tempo_criacao(request.session['criadoEm'])
        tempo_limite_criadoEm = request.session['criadoEm']
        if tempo_limite_criadoEm!='':
            sql += f" AND dt_inclusao >= '{tempo_limite_criadoEm} 00:00:00'"

    if 'fechadoEm' in request.session and request.session['fechadoEm'] is not None:
        # tempo_limite_fechadoEm = calcular_tempo_criacao(request.session['fechadoEm'])
        tempo_limite_fechadoEm = request.session['fechadoEm']
        if tempo_limite_fechadoEm!='':
            # sql += " AND dt_fechamento IS NOT NULL"
            sql += f" AND dt_inclusao <= '{tempo_limite_fechadoEm} 23:59:59'"


    if 'agendadoPara' in request.session and request.session['agendadoPara'] is not None:
        # tempo_limite_agendadoPara = calcular_tempo_criacao(request.session['agendadoPara'])
        tempo_limite_agendadoPara = request.session['agendadoPara']
        if tempo_limite_agendadoPara!='':
            sql += " AND secretaria_id IS NOT NULL"
            sql += f" AND secretaria_id = '{request.session['agendadoPara']}'"

    if 'atualizacaoEm' in request.session and request.session['atualizacaoEm'] is not None:
        tempo_limite_atualizacaoEm = calcular_tempo_criacao(request.session['atualizacaoEm'])
        if tempo_limite_atualizacaoEm!='':
            sql += " AND dt_atualizacao IS NOT NULL"
            sql += f" AND dt_atualizacao >= '{tempo_limite_atualizacaoEm.strftime('%Y-%m-%d %H:%M:%S')}'"

    # print('SQL', sql)
    sql += " ORDER BY dt_atualizacao DESC"
    return sql
 
from django.db import connection, models
def filtrar_chamados(request):
    if request.user.is_superuser or Atendente.objects.filter(servidor__user=request.user, ativo=True).exists():
        sql = make_query_chamados(request)
        
        results = Chamado.objects.raw(sql)
        queryset = []
        fechados = []
        ordenacao = request.session.get('ordenacao', False)

        for chamado in results:
            if (chamado.status == '4' or chamado.status == '5') and ordenacao:
                fechados.append(chamado)
            elif chamado.status != '6':
                queryset.append(chamado)
        queryset.sort(key=lambda x: (x.dt_atualizacao or x.dt_inclusao), reverse=True)
        if ordenacao:
            fechados.sort(key=lambda x: (x.dt_atualizacao or x.dt_inclusao), reverse=True)
            queryset.extend(fechados)
        return queryset
    else:
        return Chamado.objects.filter(requisitante__user=request.user).order_by('-dt_atualizacao')
    
# def filtrar_chamados(request):
#     if request.user.is_superuser or Atendente.objects.filter(servidor__user=request.user, ativo=True).exists():
#         sql = make_query_chamados(request)

#         with connection.cursor() as cursor:
#             cursor.execute(sql)
#             results = cursor.fetchall()

#             queryset = []
#             fechados =[]

#             for row in results:                

#                 data = {
#                     'id': row[0],
#                     'telefone': row[1],
#                     'assunto': row[2],
#                     'prioridade': row[3],
#                     'status': row[4],
#                     'descricao': row[5],
#                     'dt_inclusao': row[6],
#                     'dt_atualizacao': row[7],
#                     'dt_execucao': row[8],
#                     'dt_fechamento': row[9],
#                     'n_protocolo': row[10],
#                     'anexo': row[11],
#                     'hash': row[12],
#                     'atendente_id': row[13],
#                     'profissional_designado_id': row[14],
#                     'requisitante_id': row[15],
#                     'setor_id': row[16],
#                     'user_atualizacao_id': row[17],
#                     'user_inclusao_id': row[18],
#                     'tipo_id': row[19],
#                     'dt_inicio_execucao': row[20],
#                     'dt_agendamento': row[21],
#                     'endereco': row[22]
#                 }
#                 chamado = Chamado(**data)
                
#                 if (row[4] == '4' or row[4] == '5') and request.session['ordenacao']:
#                     fechados.append(chamado)
#                 elif row[4] != '6':                    
#                     queryset.append(chamado)

#             queryset = sorted(queryset, key=lambda x: (x.dt_atualizacao if x.dt_atualizacao else x.dt_inclusao), reverse=True)
#             if request.session['ordenacao']:
#                 fechados = sorted(fechados, key=lambda x: (x.dt_atualizacao if x.dt_atualizacao else x.dt_inclusao), reverse=True)
#                 queryset.extend(fechados)
#             # print("chamado:", queryset, '\n')
#         print(request.session['ordenacao'])
#         return queryset  

#     else:
#         queryset = Chamado.objects.filter(requisitante__user=request.user).order_by('-dt_atualizacao')
    
#     return queryset