from django import template
from ..models import Servidor

register = template.Library()

@register.filter
def get_avatar(request):
    try:
        servidor = Servidor.objects.get(user=request.user)
        if servidor.avatar:
            return servidor.avatar.url
        else:
            return '/static/images/user.png'
    except:
        return '/static/images/user.png'

@register.filter
def get_tema(user):
    if user.last_name == '0':
        return 'light'
    elif user.last_name == '1':
        return 'dark'
    else:
        return 'light'
    
@register.filter
def get_user_name(user):    
    servidor = Servidor.objects.get(user=user)    
    return servidor.nome

@register.filter
def get_registro_por_dia(registros, dia):
    for registro in registros:
        if registro.data_registro == dia:
            return registro
    return None