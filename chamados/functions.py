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
