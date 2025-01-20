from instituicoes.models import Servidor

class ServidorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Adicionar o atributo `servidor` ao objeto `request`
        if request.user.is_authenticated:
            request.servidor = Servidor.objects.filter(user=request.user).first()
        else:
            request.servidor = None

        response = self.get_response(request)
        return response