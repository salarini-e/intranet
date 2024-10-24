from django.db import models
from instituicoes.models import *
from django.contrib.auth.models import User

import hashlib
from django.utils import timezone
from datetime import datetime, timedelta



class TipoChamado(models.Model):
    nome = models.CharField(max_length=164, verbose_name='Nome')
    sigla = models.CharField(max_length=8, verbose_name='Sigla')
    descricao = models.TextField(verbose_name='Descrição')
    dt_inclusao = models.DateField(auto_now_add=True, verbose_name='Data de inclusão')
    user_inclusao = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Usuário de inclusão', null=True)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Tipo de Chamado'
        verbose_name_plural = 'Tipos de Chamados'

class Atendente(models.Model):
    NIVEL_CHOICES = (
        ('0', 'Nível 1 - Help Desk'),
        ('1', 'Nível 2 - Suporte Técnico'),
        ('2', 'Nível 3 - Administração'),

    )
    servidor = models.ForeignKey(Servidor, on_delete=models.SET_NULL, verbose_name='Servidor', null=True)
    nome_servidor = models.CharField(max_length=64, verbose_name='Nome de usuário', blank=True, null=True)
    nivel = models.CharField(max_length=1, choices=NIVEL_CHOICES, default='0')
    tipo = models.ManyToManyField(TipoChamado)
    dt_inclusao = models.DateField(auto_now_add=True, verbose_name='Data de inclusão')
    user_inclusao = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Usuário de inclusão', null=True)
    ativo = models.BooleanField(default=True, verbose_name='Ativo')

    def __str__(self):
        return self.nome_servidor   
    
    def setName(self):
        if self.servidor:
            self.nome_servidor=self.servidor.nome        
    
    def countChamadosAtribuidos(self):        
        return Chamado.objects.filter(status='0', profissional_designado=self).count()
    
    def save(self, *args, **kwargs):    
        self.setName()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Atendente'
        verbose_name_plural = 'Atendentes'

class PeriodoPreferencial(models.Model):
    nome = models.CharField(max_length=64, verbose_name='Nome')
    
    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Período Preferencial'
        verbose_name_plural = 'Períodos Preferenciais'

class Chamado(models.Model):
    PRIORIDADE_CHOICES =(
        ('-', 'Não definida'),
        ('0', 'Baixa'),
        ('1', 'Média'),
        ('2', 'Alta')        
    )

    STATUS_CHOICES = (
        ('0', 'Aberto'),
        ('1', 'Em atendimento'),
        ('2', 'Pendente'),        
        ('3', 'Fechado'),
        ('4', 'Finalizado'),
    )

    setor = models.ForeignKey(Setor, on_delete=models.SET_NULL, verbose_name='Para qual setor é o chamado?', null=True)
    secretaria = models.ForeignKey(Secretaria, on_delete=models.SET_NULL, verbose_name='Para qual setor é o chamado?', null=True)
    telefone=models.CharField(max_length=15, verbose_name='Qual telefone para contato?')
    requisitante = models.ForeignKey(Servidor, verbose_name='Nome do servidor', null=True, on_delete=models.SET_NULL)
    endereco =models.CharField(max_length=250, verbose_name = 'Endereço', blank=True, null=True)
    tipo = models.ForeignKey(TipoChamado, on_delete=models.SET_NULL, verbose_name='Tipo chamado', null=True)
    assunto = models.CharField(max_length=64, verbose_name='Assunto do chamado')
    prioridade = models.CharField(max_length=1, choices=PRIORIDADE_CHOICES, default='')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')
    descricao = models.TextField(default='', verbose_name='Descrição do problema')
    periodo_preferencial = models.ManyToManyField(PeriodoPreferencial, verbose_name='Escolha o período que você pode ser atendido')
    dt_agendamento = models.DateTimeField(verbose_name='Data agendada para o atendimento', null=True, blank=True)
    atendente = models.ForeignKey(Atendente, on_delete=models.SET_NULL, verbose_name='Atendente', null=True,related_name="chamados_atendente")
    profissional_designado = models.ForeignKey(Atendente, on_delete=models.SET_NULL, verbose_name='Profissional designado', null=True, related_name="profissional_designado_chamados")
    dt_inclusao = models.DateTimeField(auto_now_add=True, verbose_name='Data de inclusão')
    user_inclusao = models.ForeignKey(Servidor, on_delete=models.SET_NULL, null=True, verbose_name='Usuário que cadastrou', related_name="user_inclusao_chamados")
    dt_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Data de ultima atualização', null=True)
    user_atualizacao = models.ForeignKey(Servidor, on_delete=models.SET_NULL, verbose_name='Usuário da ultima atualização', null=True, related_name="user_atualizacao_chamados")
    dt_inicio_execucao = models.DateTimeField(verbose_name='Data do inicio da execução do chamado', null=True)
    dt_execucao = models.DateTimeField(verbose_name='Data o fim da execução do chamado', null=True)
    dt_fechamento = models.DateTimeField(verbose_name='Data do fechamaneto do chamado', null=True)
    n_protocolo = models.CharField(max_length=14, verbose_name='Número de protocolo', null=True)
    anexo = models.FileField(upload_to='chamados/anexos/', default=None, verbose_name='Possui alguma foto ou print do problema? Caso sim, anexe-a abaixo.', null=True, blank=True)
    hash=models.CharField(max_length=64)

    class Meta:
        verbose_name = 'Chamado'
        verbose_name_plural = 'Chamados'

    def __str__(self):
        return self.n_protocolo
    
    def gerar_hash(self):
        
        if not self.hash:            
            hash_obj = hashlib.sha256()
            hash_obj.update(str(self.id).encode('utf-8'))
            self.hash = hash_obj.hexdigest()            
            self.save()
    
    def gerar_protocolo(self):  

        if not self.n_protocolo:
            prefixo = self.tipo.sigla  
            id_formatado = str(self.id).zfill(6)          
            self.n_protocolo = f"{prefixo}{id_formatado}"
            self.save()
        
    def get_total_msg(self):        
        count = Mensagem.objects.filter(chamado=self).count()
        # print(count)
        return count
    
    def get_duracao_execucao(self):
        if self.dt_inicio_execucao and self.dt_execucao:
            intervalos = Pausas_Execucao_do_Chamado.objects.filter(chamado=self)
            if intervalos.exists():
                total_pausa = timezone.timedelta()
                for intervalo in intervalos:                        
                    total_pausa += intervalo.dt_fim - intervalo.dt_inicio
                    
                return self.dt_execucao - self.dt_inicio_execucao - total_pausa
            else:
                return self.dt_execucao - self.dt_inicio_execucao
        return None

    def check_pause(self):
        pausas = Pausas_Execucao_do_Chamado.objects.filter(chamado=self)
        if pausas.exists():
            if pausas.last().dt_fim:
                print(1)
                return False
            print(2)
            return True
        print(3)
        return False

    def get_prioridade_class(self):
        prioridade_classes = {
            '-': 'prioridade-nao-definida', 
            '0': 'prioridade-baixa',
            '1': 'prioridade-media',
            '2': 'prioridade-alta',
        }
        return prioridade_classes[self.prioridade]
    
    def get_status_class(self):
        status_classes = {
            '0': 'status-aberto',
            '1': 'status-atendimento',
            '2': 'status-pendente',
            '3': 'status-fechado',
            '4': 'status-finalizado',
        }
        return status_classes[self.status]
        
    def is_novo(self):
        # Remove o timezone de dt_inclusao e dt_atual
        dt_inclusao_naive = self.dt_inclusao.replace(tzinfo=None)
        dt_atual_naive = timezone.now().replace(tzinfo=None)

        hora = timedelta(hours=1)
        valor = dt_atual_naive - dt_inclusao_naive <= hora
        return valor
    
    def respondido_pelo_cliente(self):
        ultima_mensagem = Mensagem.objects.filter(chamado=self).order_by('-dt_inclusao').first()
        if ultima_mensagem and ultima_mensagem.user_inclusao_id == self.requisitante_id and ultima_mensagem.autor() != 'Atendente':
            return True
    
    def __processTime(self, delta):
        if delta.days > 1:
            return f"há {delta.days} dias"
        elif delta.days == 1:
            return "há 1 dia"
        else:
            horas = delta.seconds // 3600
            minutos = (delta.seconds % 3600) // 60 
            
            if horas > 0:
                if horas == 1:
                    return f"há {horas} hora"
                else:
                    return f"há {horas} horas"
            else:
                if minutos > 0:
                    if minutos == 1:
                        return f"há {minutos} minuto"
                    else:
                        return f"há {minutos} minutos"
                else:
                    return "há menos de um minuto"
    
    def getCreateTime(self):
        agora_utc = timezone.now()
        dt_inclusao_naive = self.dt_inclusao.replace(tzinfo=None)
        delta = agora_utc.replace(tzinfo=None) - dt_inclusao_naive

        return self.__processTime(delta)

    def status_andamento_ticket_detalhes(self):
        result = self.getCreateTime()
        return result
    
    def get_ultima_acao(self):
        agora = timezone.now().replace(tzinfo=None)

        # Verifica se dt_inclusao e dt_atualizacao não são None
        if self.dt_inclusao:
            dt_inclusao_naive = self.dt_inclusao.replace(tzinfo=None)
        else:
            dt_inclusao_naive = None

        if self.dt_atualizacao:
            dt_atualizacao_naive = self.dt_atualizacao.replace(tzinfo=None)
        else:
            dt_atualizacao_naive = None

        # Verifica e ajusta última alteração de prioridade se presente
        if hasattr(self, 'ultima_prioridade_alterada') and self.ultima_prioridade_alterada:
            ultima_prioridade_alterada_naive = self.ultima_prioridade_alterada.replace(tzinfo=None)
            delta = agora - ultima_prioridade_alterada_naive
            return f"Prioridade alterada {self.__processTime(delta)}"

        # Verifica e ajusta última alteração de status se presente
        if hasattr(self, 'ultima_status_alterada') and self.ultima_status_alterada:
            ultima_status_alterada_naive = self.ultima_status_alterada.replace(tzinfo=None)
            delta = agora - ultima_status_alterada_naive
            return f"Status alterado {self.__processTime(delta)}"

        # Verifica a última mensagem e a processa, se for do atendente
        ultima_mensagem = Mensagem.objects.filter(chamado=self).order_by('-dt_inclusao').first()

        if ultima_mensagem and ultima_mensagem.autor() == 'Atendente':
            if not ultima_mensagem.confidencial:
                ultima_mensagem_inclusao_naive = ultima_mensagem.dt_inclusao.replace(tzinfo=None)
                delta = agora - ultima_mensagem_inclusao_naive
                return f"Respondido pelo atendente {self.__processTime(delta)}"

        # Verifica se existe uma última mensagem e se o autor dessa mensagem é o requisitante
        elif ultima_mensagem and ultima_mensagem.user_inclusao_id == self.requisitante_id:
            ultima_mensagem_inclusao_naive = ultima_mensagem.dt_inclusao.replace(tzinfo=None)
            delta = agora - ultima_mensagem_inclusao_naive
            return f"Respondido pelo cliente {self.__processTime(delta)}"

        # Verifica se o status é finalizado
        if self.status == '4' and self.dt_fechamento:
            dt_fechamento_naive = self.dt_fechamento.replace(tzinfo=None)
            delta = agora - dt_fechamento_naive
            return f"Finalizado {self.__processTime(delta)}"

        # Caso não haja mensagens e dt_atualizacao tenha diferenca de no max 30 segundos
        if not ultima_mensagem and dt_inclusao_naive and dt_atualizacao_naive and abs((dt_atualizacao_naive - dt_inclusao_naive).total_seconds()) <= 30:
            delta = agora - dt_inclusao_naive
            return f"Criado {self.__processTime(delta)}"

        # Subtração entre agora e dt_atualizacao para o tempo atualizado
        if dt_atualizacao_naive:
            delta = agora - dt_atualizacao_naive
            return f"Atualizado {self.__processTime(delta)}"

        return "Sem ações recentes"
    # PARTE PARA TIMELIME
    def get_formatted_inclusao(self):
        dt_inclusao_naive = self.dt_inclusao.replace(tzinfo=None)
        agora = timezone.now().replace(tzinfo=None)

        data_inclusao = dt_inclusao_naive.date()

        # Diferença de dias entre hoje e a data de inclusão
        delta = (agora.date() - data_inclusao).days

        if delta == 0:
            # Se o chamado foi criado hoje
            return '<span class="timeline-label">HOJE</span>'
        elif delta == 1:
            # Se o chamado foi criado ontem
            return '<span class="timeline-label">ONTEM</span>'
        else:
            # Para dias anteriores, exibir: dia da semana, dia do mês, mês e ano
            dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
            meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

            dia_semana = dias_semana[data_inclusao.weekday()]  # Obter dia da semana
            dia = data_inclusao.day  # Obter dia do mês
            mes = meses[data_inclusao.month - 1]  # Obter mês
            ano = data_inclusao.year  # Obter ano

        return f'<span class="timeline-label">{dia_semana}, {dia} {mes}, {ano}</span>'
        
class Pausas_Execucao_do_Chamado(models.Model):
    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE, verbose_name='Chamado')
    dt_inicio = models.DateTimeField(verbose_name='Data de início da pausa')
    dt_fim = models.DateTimeField(verbose_name='Data de fim da pausa', null=True, blank=True)
    motivo = models.TextField(verbose_name='Motivo da pausa', null=True, blank=True)
    user_inclusao = models.ForeignKey(Servidor, on_delete=models.SET_NULL, verbose_name='Usuário de inclusão', null=True, related_name="user_inclusao_pausas", blank=True)
    user_fim = models.ForeignKey(Servidor, on_delete=models.SET_NULL, verbose_name='Usuário de finalização', null=True, related_name="user_finalizacao_pausas", blank=True)

    class Meta:
        verbose_name = 'Pausa na execução do chamado'
        verbose_name_plural = 'Pausas na execução do chamado'
        
    def __str__(self):
        return f"Pausa do Chamado {self.chamado.n_protocolo} - {self.dt_inicio} até {self.dt_fim if self.dt_fim else 'em andamento'}"
class Mensagem(models.Model):
    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE, verbose_name='Chamado')    
    mensagem = models.TextField(verbose_name='Mensagem')
    anexo = models.FileField(upload_to='chamados/anexos/', default=None, null=True, blank=True)
    dt_inclusao = models.DateTimeField(auto_now_add=True, verbose_name='Data de inclusão')
    user_inclusao = models.ForeignKey(Servidor, on_delete=models.SET_NULL, verbose_name='Usuário de inclusão', null=True, related_name="user_inclusao_mensagens")
    confidencial = models.BooleanField(default=False, verbose_name='Confidencial')

    def autor(self):                
        atendente = Atendente.objects.filter(servidor=self.user_inclusao)
        if atendente.exists():
            return 'Atendente'
        else:
            return self.user_inclusao
    
    def __processTime(self, delta):
        if delta.days > 1:
            return f"há {delta.days} dias"
        elif delta.days == 1:
            return "há 1 dia"
        else:
            horas = delta.seconds // 3600
            minutos = (delta.seconds % 3600) // 60  # Calcular minutos restantes
            
            if horas > 0:
                if horas == 1:
                    return f"há {horas} hora"
                else:
                    return f"há {horas} horas"
            else:
                if minutos > 0:
                    if minutos == 1:
                        return f"há {minutos} minuto"
                    else:
                        return f"há {minutos} minutos"
                else:
                    return "há menos de um minuto"
            
    def getCreateTime(self):
        agora_utc = timezone.now()
        dt_inclusao_naive = self.dt_inclusao.replace(tzinfo=None)
        delta = agora_utc.replace(tzinfo=None) - dt_inclusao_naive

        return self.__processTime(delta)

    def status_andamento_mensagem(self):
        result = self.getCreateTime()
        return result

    class Meta:
        verbose_name = 'Mensagem'
        verbose_name_plural = 'Mensagens'

class OSInternet(models.Model):
    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE, verbose_name='Chamado', null=True, blank=True)
    nofcip = models.CharField(max_length=64, verbose_name='NOFCIP', null=True)

    class Meta:
        verbose_name = 'Ordem de Serviço - Internet'
        verbose_name_plural = 'Ordens de Serviço - Internet'

class OSImpressora(models.Model):
    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE, verbose_name='Chamado', null=True, blank=True)
    n_serie = models.CharField(max_length=64, verbose_name='Número de série', null=True)
    contador = models.IntegerField(verbose_name='Contador', null=True)

    class Meta:
        verbose_name = 'Ordem de Serviço - Impressora'
        verbose_name_plural = 'Ordens de Serviço - Impressora'

class OSSistemas(models.Model):
    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE, verbose_name='Chamado', null=True, blank=True)
    sistema = models.CharField(max_length=64, verbose_name='Sistema')    

    class Meta:
        verbose_name = 'Ordem de Serviço - Sistemas'
        verbose_name_plural = 'Ordens de Serviço - Sistemas'

class OSTelefonia(models.Model):
    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE, verbose_name='Chamado', null=True, blank=True)
    ramal = models.CharField(max_length=20, verbose_name='Ramal')

    class Meta:
        verbose_name = 'Ordem de Serviço - Telefonia'
        verbose_name_plural = 'Ordens de Serviço - Telefonia'