from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cadastro_Aulas_Processo_Digital
from .models import Inscricao_Decretos_Portaria_Atos_Prefeito

# Sinal para desativar a turma quando atingir o limite de 30 inscrições no Cadastro_Aulas_Processo_Digital
@receiver(post_save, sender=Cadastro_Aulas_Processo_Digital)
def check_turma_capacity(sender, instance, **kwargs):
    turma = instance.turma_escolhida
    if turma:
        inscricoes = Cadastro_Aulas_Processo_Digital.objects.filter(turma_escolhida=turma).count()
        if inscricoes >= 30 and turma.ativo:
            turma.ativo = False
            turma.save()
