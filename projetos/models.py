from django.db import models
from django.contrib.auth.models import User
from instituicoes.models import Servidor
from django.db.models import Count, Q


class Projetos(models.Model):
    
    STATUS_CHOICES = (
        ('C', 'Planejamento'),
        ('E', 'Em andamento'),        
        ('F', 'Finalizado'),
        ('P', 'Parado'),
    )
    
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='C')
    
    user_inclusao = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Usuário de inclusão')
    dt_inclusao = models.DateField(auto_now_add=True)
    dt_att  = models.DateField(auto_now=True)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name_plural = "Fases dos projetos"
        verbose_name = "Fase do projeto"

    def get_status_color(self):
        if self.status == 'C':
            return '#313131'
        elif self.status == 'E':
            return '#FCAA3D'
        elif self.status == 'F':
            return '#00C875'
        elif self.status == 'P':
            return '#da2e48'
    
    def get_status_icon(self):
        if self.status == 'C':
            return '<i class="fa-solid fa-circle-notch me-3" style="color: #313131;"></i>'
        elif self.status == 'E':
            return '<i class="fa-regular fa-clock me-3" style="color: #FCAA3D;"></i>'
        elif self.status == 'F':
            return ' <i class="fa-solid fa-circle-check me-lg-3" style="color: #00C875;"></i>'
        elif self.status == 'P':
            return '<i class="fa-solid fa-circle-pause me-3" style="color: #da2e48;"></i>'
        
    def servidor(self):
        servidor=Servidor.objects.get(user=self.user_inclusao)
        return servidor.nome.title()
    
    def get_progresso(self):
        tarefas = Tarefas.objects.filter(fase__projeto=self)
        total_atividades = 0
        total_atividades_concluidas = 0
        
        for tarefa in tarefas:
            atividades = Atividades.objects.filter(tarefa=tarefa)
            
            if atividades.exists():
                total_atividades += atividades.count() 
                total_atividades_concluidas += atividades.filter(concluido=True).count() 
            else:
                total_atividades += 1  
                total_atividades_concluidas += 1 if tarefa.concluido else 0  

        if total_atividades > 0:
            progresso = (total_atividades_concluidas / total_atividades) * 100
        else:
            progresso = 0  

        # print('Projeto:', self.nome)
        # print('Total tarefas:',tarefas.count())
        # print('Total concluidas:' , tarefas.filter(concluido=True).count())
        # print('Total de atividades:', total_atividades)
        # print('Total atividades concluidas:', total_atividades_concluidas)
        return round(progresso)


class Fases(models.Model):
    
    STATUS_CHOICES = (
        ('at', 'Ativo'),
        ('ar', 'Arquivado'),
    )
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='at')
    projeto = models.ForeignKey(Projetos, on_delete=models.CASCADE)
    ordem = models.IntegerField()
    nome = models.CharField(max_length=255)
    descricao = models.TextField(verbose_name='Descrição')
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)
    
    user_inclusao = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Usuário de inclusão')
    dt_inclusao = models.DateField(auto_now_add=True)
    dt_att  = models.DateField(auto_now=True)

    def __str__(self):
        return self.nome

    class Meta:
        unique_together = ('projeto', 'ordem')
        verbose_name_plural = "Etapas dos projetos"
        verbose_name = "Etapa do projeto"

    def get_tarefas(self):
        tarefas = Tarefas.objects.filter(fase=self).order_by('orderm')
        return tarefas
    
class Categorias(models.Model):
    
    nome = models.CharField(max_length=255)
    descricao = models.TextField(verbose_name='Descrição')
    user_inclusao = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Usuário de inclusão')
    dt_inclusao = models.DateField(auto_now_add=True)
    dt_att  = models.DateField(auto_now=True)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name_plural = "Categorias das tarefas"
        verbose_name = "Categoria das tarefas"

class Prioridade(models.Model):
    nome = models.CharField(max_length=50)
    cor = models.CharField(max_length=7, default="#FFFFFF")  # Código de cor para UI
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name_plural = "Prioridades das tarefas"
        verbose_name = "Prioridade das tarefas"
    
class Tarefas(models.Model):    

    fase = models.ForeignKey(Fases, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    descricao = models.TextField(verbose_name='Descrição')
    orderm = models.IntegerField()
    concluido = models.BooleanField(default=False)
    data_inicio = models.DateField(null=True, blank=True, verbose_name='Data de início')
    data_fim = models.DateField(null=True, blank=True, verbose_name='Data de fim')
    categoria = models.ManyToManyField(Categorias)
    prioridade = models.ForeignKey(Prioridade, on_delete=models.SET_NULL, null=True, blank=True)
    anexo = models.FileField(upload_to='projetos/anexos/', null=True, blank=True)
    
    user_inclusao = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Usuário de inclusão')
    dt_inclusao = models.DateField(auto_now_add=True)
    dt_att  = models.DateField(auto_now=True)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name_plural = "Tarefas dos projetos"
        verbose_name = "Tarefa do projeto"

    def get_comentarios(self):
        comentarios = Comentarios.objects.filter(atribuicao='t', tarefa=self.id)
        return comentarios

    def get_atividades(self):
        atividades = Atividades.objects.filter(tarefa=self).order_by('ordem')
        return atividades
    
class Atividades(models.Model):
    
    tarefa = models.ForeignKey(Tarefas, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    descricao = models.TextField(verbose_name='Descrição')
    ordem = models.IntegerField()
    concluido = models.BooleanField(default=False)
    data_execucao = models.DateField(null=True, blank=True, verbose_name='Data de execução')
    anexo = models.FileField(upload_to='projetos/anexos/', null=True, blank=True)
    
    user_inclusao = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Usuário de inclusão')
    dt_inclusao = models.DateField(auto_now_add=True)
    dt_att  = models.DateField(auto_now=True)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name_plural = "Atividades das tarefas"
        verbose_name = "Atividade da tarefa"

    def get_comentarios(self):
        comentarios = Comentarios.objects.filter(atribuicao='a', atividade=self.id)
        return comentarios 

class Comentarios(models.Model):
    
    ATRIBUICAO_CHOICES = (
        ('t', 'Tarefa'),
        ('a', 'Atividade'),
    )
    atribuicao = models.CharField(max_length=1, choices=ATRIBUICAO_CHOICES)
    tarefa = models.ForeignKey(Tarefas, on_delete=models.CASCADE, null=True, blank=True)
    atividade = models.ForeignKey(Atividades, on_delete=models.CASCADE, null=True, blank=True)
    descricao = models.TextField()
    
    user_inclusao = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Usuário de inclusão')
    dt_inclusao = models.DateField(auto_now_add=True)
    dt_att  = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.descricao[:30]}..."
    
    class Meta:
        verbose_name_plural = "Comentários das tarefas"
        verbose_name = "Comentário da tarefa"