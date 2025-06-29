from functools import wraps
from django.http import HttpResponseForbidden

from instituicoes.models import Servidor as Pessoa

def required_almoxarifado(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        funcionario = Pessoa.objects.filter(matricula=request.user)

        # AQUI EU LIMITO O ACESSO A PARTE DE ALMOXARIFADO APENAS AO ROMULO E ALESSANDRO DA SUBSECRETARIA DE TI
        # SERÁ UTILIZADO ESSE DECORATORS NA MODELS DA SEGUINTE FORMA: @required_almoxarifado
        if funcionario.exists() and ((funcionario.first().matricula == '063613') or (funcionario.first().matricula == '063563') or (funcionario.first().matricula == 'gustavo.dias') or (funcionario.first().matricula == '063508')):
            
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Acesso restrito a Secretaria de TI.")
    return _wrapped_view