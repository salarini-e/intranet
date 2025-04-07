from django.db import models
from instituicoes.models import Servidor as Responsavel
# Create your models here
    
class PlanejamentoAcao(models.Model):

    STATUS_CHOICES = (
        ('p', 'Pendente'),
        ('e', 'Em andamento'),
        ('c', 'Concluído'),
        ('x', 'Cancelado'),
    )
    data = models.DateField()
    descricao = models.TextField(max_length=500)
    local = models.CharField(max_length=100)
    horario = models.TimeField()
    responsavel = models.ForeignKey(Responsavel, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='p')
    
    class Meta:
        ordering = ['data', 'horario']
        verbose_name = 'Planejamento'

    def __str__(self):
        return f'{self.data} {self.descricao} {self.local} {self.horario} {self.responsavel} {self.status}'
    