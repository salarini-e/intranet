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
        print(email_template)
        self.criar_notificacao('Chamado criado com sucesso!')

        msg = {
            'subject': 'Chamado criado com sucesso!',
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
