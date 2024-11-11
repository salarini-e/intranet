from django.db import models
from instituicoes.models import Servidor

from django.utils.html import format_html
from django.utils.timesince import timesince
from django.utils import timezone

class Notificacao(models.Model):
    new= models.BooleanField(default=True)
    user = models.ForeignKey(Servidor, on_delete=models.CASCADE)
    icone = models.CharField(max_length=150)
    msg = models.CharField(max_length=100)
    lida = models.BooleanField(default=False)
    link = models.CharField(max_length=100, null=True, blank=True)
    data = models.DateTimeField(auto_now_add=True)
    cadastrado_por = models.ForeignKey(Servidor, on_delete=models.CASCADE, related_name='cadastrado_por', null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {self.msg}'
    
    def get_latest_notifications_html(self, user):
        notifications = Notificacao.objects.filter(user=user).order_by('-data')[:4]
        html_content = ""

        for notification in notifications:
            icon_html = (
                f'<i class="{notification.icone}"></i>'
                if "fa-" in notification.icone
                else f'<img class="profile-image" src="{notification.icone}" alt="">'
            )
            time_since = timesince(notification.data, timezone.now())
            html_content += format_html(
                '''
                <div class="item p-3">
                    <div class="row gx-2 justify-content-between align-items-center">
                        <div class="col-auto">
                            <div class="app-icon-holder icon-holder-mono">
                                {icon}
                            </div>
                        </div>
                        <div class="col">
                            <div class="info">
                                <div class="desc">{msg}</div>
                                <div class="meta">{time_since} atrás</div>
                            </div>
                        </div>
                    </div>
                    <a class="link-mask" href="{link}"></a>
                </div>
                ''',
                icon=icon_html,
                msg=notification.msg,
                time_since=time_since,
                link=notification.link or "#"
            )

        if not html_content:
            html_content = format_html(
                '''
                <div class="item p-3">
                    <div class="row gx-2 justify-content-between align-items-center">
                        <div class="col-auto">
                            <div class="app-icon-holder icon-holder-mono">
                                <i class="fa-solid fa-hammer"></i>
                            </div>
                        </div>
                        <div class="col">
                            <div class="info">
                                <div class="desc">Estamos construindo nosso sistema de notificação. Aguarde...</div>
                                <div class="meta">:)</div>
                            </div>
                        </div>
                    </div>
                </div>
                '''
            )

        return html_content