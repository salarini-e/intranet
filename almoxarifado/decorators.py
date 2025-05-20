from functools import wraps
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden

Pessoa = get_user_model()

def required_almoxarifado(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        funcionario = Pessoa.objects.filter(username=request.user)

        # AQUI EU LIMITO O ACESSO A PARTE DE ALMOXARIFADO APENAS AO ROMULO E ALESSANDRO DA SUBSECRETARIA DE TI
        # SERÁ UTILIZADO ESSE DECORATORS NA MODELS DA SEGUINTE FORMA: @required_almoxarifado
        if funcionario.exists() and ((funcionario.first().username == '063613') or (funcionario.first().username == '063563') or (funcionario.first().username == 'gustavo.dias')):
            
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Acesso restrito a Secretaria de TI.")
    return _wrapped_view
