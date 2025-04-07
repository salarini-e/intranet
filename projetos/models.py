from django.db import models
from django.contrib.auth.models import User
from instituicoes.models import Servidor
from django.db.models import Count, Q

# A demanda poderá vir da tareja de um projeto, da subtarefa de um projeto, do futuro agendamento de ações que será desenvolvido, ou pode ser demandas criadas ali avulsas mesmo:
class Demandas(models.Model):
    
    REFERENCIA_CHOICES = {
        ('t', 'Gestão de Projetos'),
        ('a', 'Gestão de Projetos'),
        ('p', 'Ação planejada'),
        ('n', 'Nenhuma'),
    }
    PRIORIDADE_CHOICES = {
        (0, 'Regular'),
        (1, 'Média'),
        (2, 'Importante'),
        (3, 'Urgente'),        

    }
    nome = models.CharField(max_length=255)
    descricao = models.TextField(verbose_name='Descrição')
    prioridade = models.IntegerField(choices=PRIORIDADE_CHOICES, default=0)
    data_prevista_execucao = models.DateField(null=True, blank=True)
    rotina = models.BooleanField(default=False, verbose_name="É uma rotina?")
    ordem_dia = models.IntegerField(null=True, blank=True, verbose_name="Ordem do dia")
    ##########
    concluido = models.BooleanField(default=False)
    dt_concluido = models.DateField(null=True, blank=True)

    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)
        
    atribuicao = models.ForeignKey(Servidor, on_delete=models.SET_NULL, null=True, blank=True, related_name='demandas')
    dt_inclusao = models.DateField(auto_now_add=True)
    dt_att  = models.DateField(auto_now=True)

    referencia = models.CharField(max_length=1, choices=REFERENCIA_CHOICES, default='n')
    id_referencia = models.IntegerField(null=True, blank=True)
    user_inclusao = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Usuário de inclusão')

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name_plural = "Demandas"
        verbose_name = "Demanda"
        ordering = ['ordem_dia', 'data_prevista_execucao', 'nome']  # Order by ordem_dia, then date, then name

    def save(self, *args, **kwargs):        
        if not self.atribuicao:
            self.atribuicao = Servidor.objects.get(user=self.user_inclusao)
        if self.concluido:
            self.dt_concluido = self.dt_att
        super(Demandas, self).save(*args, **kwargs)

class Grupo(models.Model):
    responsavel = models.ForeignKey(Servidor, on_delete=models.SET_NULL, null=True, blank=True)
    nome = models.CharField(max_length=255)
    membros = models.ManyToManyField(Servidor, related_name='grupos', blank=True)
    
    user_inclusao = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Usuário de inclusão')
    dt_inclusao = models.DateField(auto_now_add=True)
    dt_att  = models.DateField(auto_now=True)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name_plural = "Grupos de servidores"
        verbose_name = "Grupo de servidores"

class Projetos(models.Model):
    
    STATUS_CHOICES = (
        ('C', 'Planejamento'),
        ('E', 'Em andamento'),        
        ('F', 'Finalizado'),
        ('P', 'Parado'),
        ('A', 'Arquivado'),
    )
    
    responsavel = models.ForeignKey(Servidor, on_delete=models.SET_NULL, null=True, blank=True)
    grupos = models.ManyToManyField(Grupo, related_name='grupos', blank=True)
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

    def save(self, *args, **kwargs):
        if not self.pk:
            self.status = 'C'
        if not self.responsavel:
            self.responsavel = Servidor.objects.get(user=self.user_inclusao)
        super(Projetos, self).save(*args, **kwargs)
        
    def get_status_color(self):
        if self.status == 'C':
            return '#8B8000'  # Dark mustard
        elif self.status == 'E':
            return '#1c8f1a'
        elif self.status == 'F':
            return '#000000'  # Black
        elif self.status == 'P':
            return '#da2e48'
    
    def get_status_icon(self):
        if self.status == 'C':
            return '<i class="fa-solid fa-circle-notch me-3" style="color: #313131;"></i>'
        elif self.status == 'E':
            return '<i class="fa-regular fa-clock me-3" style="color: #1c8f1a;"></i>'
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
        # unique_together = ('projeto', 'ordem')
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
    atribuicao = models.ForeignKey(Servidor, on_delete=models.SET_NULL, null=True, blank=True, related_name='atribuicao')
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
    
    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = Tarefas.objects.get(pk=self.pk)
            if old_instance.anexo and old_instance.anexo != self.anexo:
                old_instance.anexo.delete(save=False)
            if old_instance.atribuicao != self.atribuicao and self.atribuicao:
                if self.exist_demanda():
                    self.att_demanda()
                else:
                    self.cria_demanda()
        if self.concluido and self.exist_demanda():
            self.att_demanda()
            
        super(Tarefas, self).save(*args, **kwargs)

    def cria_demanda(self):
        demanda = Demandas.objects.create(
            nome=self.nome,
            descricao=self.descricao,
            prioridade=self.prioridade if self.prioridade else 0,
            data_inicio=self.data_inicio,
            data_fim=self.data_fim,
            atribuicao=self.atribuicao,
            concluido=self.concluido,
            referencia='t',
            id_referencia=self.id,
            user_inclusao=self.user_inclusao,
        )
        return demanda
    
    def exist_demanda(self):
        try:
            demanda = Demandas.objects.get(id_referencia=self.id, referencia='t')
            return True
        except Demandas.DoesNotExist:
            return False
    
    def att_demanda(self):
        try:
            demanda = Demandas.objects.get(id_referencia=self.id, referencia='t')
            demanda.nome = self.nome
            demanda.descricao = self.descricao
            demanda.data_inicio = self.data_inicio
            demanda.data_fim = self.data_fim
            demanda.atribuicao = self.atribuicao
            demanda.concluido = self.concluido
            demanda.save()
        except Demandas.DoesNotExist:            
            demanda = None
        return demanda
    
    
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

    def cria_demanda(self):
        demanda = Demandas.objects.create(
            nome=self.nome,
            descricao=self.descricao,
            prioridade=self.tarefa.prioridade if self.tarefa.prioridade else 0,
            data_inicio=self.data_inicio,
            data_fim=self.data_fim,
            atribuicao=self.atribuicao,
            concluido=self.concluido,            
            referencia='a',
            id_referencia=self.id,
            user_inclusao=self.user_inclusao,
        )
        return demanda
    
    def exist_demanda(self):
        try:
            demanda = Demandas.objects.get(id_referencia=self.id, referencia='t')
            return True
        except Demandas.DoesNotExist:
            return False
    
    def att_demanda(self):
        try:
            demanda = Demandas.objects.get(id_referencia=self.id, referencia='t')
            demanda.nome = self.nome
            demanda.descricao = self.descricao
            demanda.data_inicio = self.data_inicio
            demanda.data_fim = self.data_fim
            demanda.atribuicao = self.atribuicao
            demanda.concluido = self.concluido
            demanda.save()
        except Demandas.DoesNotExist:
            demanda = None
        return demanda
    
class Comentarios(models.Model):
    
    ATRIBUICAO_CHOICES = (
        ('p', 'Projeto'),
        ('t', 'Tarefa'),
        ('a', 'Atividade'),
    )
    atribuicao = models.CharField(max_length=1, choices=ATRIBUICAO_CHOICES)
    projeto = models.ForeignKey(Projetos, on_delete=models.CASCADE, null=True, blank=True)
    tarefa = models.ForeignKey(Tarefas, on_delete=models.CASCADE, null=True, blank=True)
    atividade = models.ForeignKey(Atividades, on_delete=models.CASCADE, null=True, blank=True)
    descricao = models.TextField()
    
    user_inclusao = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Usuário de inclusão')
    dt_inclusao = models.DateTimeField(auto_now_add=True)
    dt_att  = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.descricao[:30]}..."
    
    def servidor(self):
        servidor=Servidor.objects.get(user=self.user_inclusao)
        return servidor.nome.title()
        
    class Meta:
        verbose_name_plural = "Comentários das tarefas"
        verbose_name = "Comentário da tarefa"

class Anexo(models.Model):
    tarefa = models.ForeignKey(Tarefas, on_delete=models.CASCADE, null=True, blank=True, related_name='anexos_tarefa')
    atividade = models.ForeignKey(Atividades, on_delete=models.CASCADE, null=True, blank=True, related_name='anexos_atividade')
    arquivo = models.FileField(upload_to='projetos/anexos/')
    tipo = models.CharField(max_length=1, choices=(('t', 'Tarefa'), ('a', 'Atividade')))
    
    def __str__(self):
        return self.arquivo.name
    
    class Meta:
        verbose_name_plural = "Anexos das tarefas e das atividades"
        verbose_name = "Anexo das tarefa ou das atividade"

    def delete(self, *args, **kwargs):
        self.arquivo.delete()
        super().delete(*args, **kwargs)
