from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cadastro_Aulas_Processo_Digital, Opcao_Turmas

# Sinal para desativar a turma quando atingir o limite de 25 inscrições
@receiver(post_save, sender=Cadastro_Aulas_Processo_Digital)
def check_turma_capacity(sender, instance, **kwargs):
    turma = instance.turma_escolhida
    if turma:
        # Conta o número de inscrições na turma
        inscricoes = Cadastro_Aulas_Processo_Digital.objects.filter(turma_escolhida=turma).count()
        # Se atingiu o limite de 25, desativa a turma
        if inscricoes >= 30:
            turma.ativo = False
            turma.save()