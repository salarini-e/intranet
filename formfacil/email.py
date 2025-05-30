from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.shortcuts import redirect

class Email:
    def __init__(self, objeto):
        # self.servidor = servidor
        self.model = objeto

    def create_email(self, email_to, email_template_name):    
        c = {
            "email": email_to,
            'domain': 'intranet.novafriburgo.rj.gov.br',
            'model': self.model,
            'site_name': 'Intranet',                            
            'protocol': 'https',
        }
        email = render_to_string(email_template_name, c)
        return email

    def criar_notificacao(self, subject):
        pass


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
