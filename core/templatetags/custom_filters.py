# myapp/templatetags/custom_filters.py
from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def first_name(full_name):
    return full_name.split()[0] if full_name else ''


@register.filter
def tempo_desde(data):
    agora = timezone.now()
    delta = agora - data

    if delta.days > 1:
        return f"há {delta.days} dias"
    elif delta.days == 1:
        return "há 1 dia"
    else:
        horas = delta.seconds // 3600
        if horas > 0:
            return f"há {horas} horas"
        else:
            return "há menos de uma hora"