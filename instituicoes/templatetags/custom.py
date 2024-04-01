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
