from django.db import models

class Item(models.Model):
    nome = models.CharField(max_length=255)
    quantidade_total = models.IntegerField()

    def __str__(self):
        return f"{self.nome}"

class AlocaItem(models.Model):
    user = models.CharField(max_length=100)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    data = models.DateField(auto_now_add=True)
    quantidade = models.IntegerField()
    descricao = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.user} - {self.item.nome}"
    
class RetiraItem(models.Model):
    user = models.CharField(max_length=100)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    data = models.DateField(auto_now_add=True)
    quantidade = models.IntegerField()
    descricao = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.user} - {self.item.nome}"

class HistoricoItem(models.Model):
    TIPO_ACAO = (
        ('ALOCACAO', 'Alocação'),
        ('RETIRADA', 'Retirada'),
        ('ADICAO', 'Adição'),
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    usuario = models.CharField(max_length=100)
    data = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=10, choices=TIPO_ACAO)
    descricao = models.CharField(max_length=500)
    quantidade_inicial = models.IntegerField()
    quantidade = models.IntegerField()
    quantidade_final = models.IntegerField()

    def __str__(self):
        return f"{self.item.nome} - {self.get_tipo_display()} - {self.data.strftime('%d/%m/%Y %H:%M')}"
