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

def enviar_email_atendente(request, chamado):
    
    servidor = Servidor.objects.filter(user=request.user)
    if servidor.exists():
        for user in servidor:
            subject = "Novo chamado atribuido a você."
            email_template_name = "chamados/atendente_atribuido.txt"
            c = {
                "email": user.email,
                'domain': 'intranet.novafriburgo.rj.gov.br',
                'chamado': chamado,
                'site_name': 'Intranet',
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                'url': redirect('chamados:detalhes', hash=chamado.hash).url,
                'protocol': 'https',
            }
            email = render_to_string(email_template_name, c)
            try:
                send_mail(subject, email, user.email, [
                            user.email], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("autenticacao:passwd_reset_done")
    else:
        messages.error(request, 'Email não cadastrado no sistema.')