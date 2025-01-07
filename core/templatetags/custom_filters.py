from django import template
from django.utils import timezone
from chamados.models import Chamado, SubTipoChamado, chamadoSatisfacao
from notificacoes.models import Notificacao
from instituicoes.models import Servidor
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.timesince import timesince

register = template.Library()

@register.filter
def first_name(full_name):
    return full_name.split()[0] if full_name else ''

def get_custom_timesince(notification_time):
    # Calculando a diferença de tempo
    diff = timezone.now() - notification_time

    # Menor que 1 hora - minutos
    if diff.total_seconds() < 3600:
        minutes = int(diff.total_seconds() // 60)
        return f'{minutes} minuto{"s" if minutes > 1 else ""}'

    # Menor que 1 dia - horas
    elif diff.total_seconds() < 86400:
        hours = int(diff.total_seconds() // 3600)
        return f'{hours} hora{"s" if hours > 1 else ""}'

    # Menor que 1 semana - dias
    elif diff.total_seconds() < 604800:
        days = int(diff.total_seconds() // 86400)
        return f'{days} dia{"s" if days > 1 else ""}'

    # Menor que 1 mês - semanas
    elif diff.total_seconds() < 2592000:
        weeks = int(diff.total_seconds() // 604800)
        return f'{weeks} semana{"s" if weeks > 1 else ""}'

    # Maior que 1 mês - meses
    else:
        months = int(diff.total_seconds() // 2592000)
        return f'{months} mês{"es" if months > 1 else ""}'
@register.simple_tag
def get_notifications(user):
    servidor = Servidor.objects.get(user=user)
    notifications = Notificacao.objects.filter(user=servidor).order_by('-data')[:4]
    content = ""

    for notification in notifications:
        # Adiciona a classe 'new' para notificações não lidas
        new_class = 'new' if not notification.lida else ''

        icon_html = (
            f"<i class='{notification.icone}'></i>"
            if "fa-" in notification.icone
            else f'<img class="profile-image" src="{notification.icone}" alt="">'
        )
        
        # Usando a função personalizada para calcular o tempo
        time_since = get_custom_timesince(notification.data)

        content += f'''
            <div class="item p-3 {new_class}" data-id="{notification.id}">
                <div class="row gx-2 justify-content-between align-items-center">
                    <div class="col-auto">
                        <div class="app-icon-holder icon-holder-mono">
                            {icon_html}
                        </div>
                    </div>
                    <div class="col">
                        <div class="info">
                            <div class="desc">{notification.msg}</div>
                            <div class="meta">{time_since} atrás</div>
                        </div>
                    </div>
                </div>
                <a class="link-mask" href="{notification.link}"></a>
            </div>
        '''

    if not content:
        content = format_html(
            '''
            <div class="item p-3">
                <div class="row gx-2 justify-content-between align-items-center">
                    <div class="col-auto">
                        <div class="app-icon-holder icon-holder-mono">
                            <i class="fa-solid fa-hammer"></i>
                        </div>
                    </div>
                    <div class="col">
                        <div class="info">
                            <div class="desc">Estamos construindo nosso sistema de notificação. Aguarde...</div>
                            <div class="meta">:)</div>
                        </div>
                    </div>
                </div>
            </div>
            '''
        )

    return mark_safe(content)


from chamados.models import Atendente

@register.filter
def acesso_adm_or_helpdesk(chamado_id, user):
    try:
        servidor = Servidor.objects.get(user=user)
        atendentes = Atendente.objects.filter(servidor=servidor)
            
        if atendentes:
            atendente = atendentes.first()            
            if atendente.nivel in ['0', '2']:
                return True
            
    except (Servidor.DoesNotExist, Chamado.DoesNotExist):
        return False
    
    try:
        chamado = Chamado.objects.get(id=chamado_id)
        if chamado:
                if atendente == chamado.profissional_designado:
                    return True
    except Chamado.DoesNotExist:
            return False
    
    return False


@register.filter
def total_subtipo(tipo__nome):
    
    return 'tenho que terminar esse filtro'

@register.filter
def check_satisfacao(user):
    # return True    
    servidor = Servidor.objects.get(user=user)
    chamados = Chamado.objects.filter(requisitante=servidor, status='4', pesquisa_satisfacao=False).order_by('-id')
    if chamados.exists():
            return True        
    return False

@register.filter
def check_satisfacao_chamado(user):
    # return Chamado.objects.get(id=216).id
    servidor = Servidor.objects.get(user=user)
    return Chamado.objects.filter(requisitante=servidor, status='4', pesquisa_satisfacao=False).order_by('-id').first()

@register.filter
def chamado_satisfacao_display(user):
    servidor = Servidor.objects.get(user=user)
    chamados = Chamado.objects.filter(requisitante=servidor, status='4', pesquisa_satisfacao=False).order_by('-id')
    if chamados.exists():
        chamado = chamados.first()
        return f'''
        <p class="text-center" style="margin-bottom: 0; padding-bottom: 0; line-height: auto;"><strong>#{chamado.n_protocolo}</strong></p>
        <p class="text-center" style="margin: 0;">{chamado.descricao}</p>				
        <p class="text-center" style="color: #5b6b7c; margin-top: 10px;">
                <i class="fa-solid fa-tools"></i> {chamado.profissional_designado}
        </p>'''
    return False