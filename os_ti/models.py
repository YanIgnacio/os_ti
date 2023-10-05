from tabnanny import verbose
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.functions import Extract
import uuid
from django.utils import timezone

from django.db.models.signals import post_save
from django.dispatch import receiver


class Endereco(models.Model):
    cep = models.CharField(max_length=9, verbose_name='CEP', default='')
    referencia = models.CharField(max_length=200, verbose_name='Referência', blank=True)
    bairro = models.CharField(max_length=150, verbose_name='Bairro')
    logradouro = models.CharField(max_length=150, verbose_name='Logradouro')
    numero = models.IntegerField(verbose_name='Numero', default=0)
    
class Secretaria(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome')
    
    def __str__(self):
        return self.nome

class Setor(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome')
    secretaria = models.ForeignKey(Secretaria, on_delete=models.CASCADE)
    endereco = models.CharField(max_length=128, verbose_name='Endereco', null=True)
    
    def __str__(self):
        return self.nome
    

class Pessoa(models.Model):
    def __str__(self):
        return '%s - Email: %s' % (self.nome, self.email)
    
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    nome=models.CharField(max_length=64, verbose_name='Nome')
    email=models.EmailField()
    matricula=models.CharField(max_length=7, verbose_name='Matricula', unique=True, null=True)
    telefone=models.CharField(max_length=15, verbose_name='Telefone', null=True)
    dt_nascimento=models.DateField(verbose_name='Data de nascimento', null=True)
    secretaria=models.CharField(max_length=100, verbose_name='Secretaria', default='')
    dt_inclusao=models.DateField(auto_now_add=True, verbose_name='Data de inclusão')

class Tipo_Material(models.Model):
    nome=models.CharField('Tipo de Material', max_length=120)
    dt_inclusao=models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')

    class Meta:
        verbose_name_plural = "Tipos de Materiais"
        verbose_name = "Tipo de Material"
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Material(models.Model):
    tipo=models.ForeignKey(Tipo_Material, on_delete=models.CASCADE)
    nome=models.CharField('Nome do Material', max_length=120)
    qnt_em_estoque=models.IntegerField(default=0, blank=True, null=True)
    dt_inclusao=models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')

    class Meta:
        verbose_name_plural = "Materiais"
        verbose_name = "Material"
        ordering = ['tipo__nome','nome', 'qnt_em_estoque']
    
    def __str__(self):
        return self.nome

class Tipo_OS(models.Model):
    
    nome=models.CharField(max_length=100, verbose_name='Tipo de OS', blank=True)
    sigla=models.CharField(max_length=10, verbose_name='Sigla', blank=True, null=True)
    def __str__(self):
        return self.nome

class Funcionario_OS(models.Model):
    def __str__(self):
        return self.pessoa.nome
    NIVEL_CHOICES=(
        ('0','0 - Agente de atendimento'),
        ('1','1 - Suporte de campo'),
        ('2','2 - Suporte avançado'),
        ('3','3 - Coordenador de serviços públicos'),
    )

    pessoa = models.ForeignKey(Pessoa, models.CASCADE)
    tipo_os =  models.ManyToManyField(Tipo_OS)
    nivel = models.CharField(max_length=1, verbose_name='Nível de acesso', choices=NIVEL_CHOICES, null=True, default='0')
    dt_inclusao=models.DateField(auto_now_add=True, verbose_name='Data de inclusão')


class TotalOSPorSemanaAno(models.Model):
    ano = models.IntegerField()
    semana = models.IntegerField()
    total_os = models.IntegerField()


class TotalOSPorMesAno(models.Model):
    ano = models.IntegerField()
    mes = models.IntegerField()
    total_os = models.IntegerField()

class OrdemDeServico(models.Model):
    STATUS_CHOICES=(
        ('0','Novo'),
        ('1','Aguardando'),
        ('2','Em execução'),
        ('f','Finalizado')
    )
    PRIORIDADE_CHOICES=(
        ('0','Normal'),
        ('1','Moderada'),
        ('2','Urgente'),
    )
    MESSAGE_STATUS_CHOICES=(
        ('0','Sem mensagens'),
        ('1','Mensagens lidas'),
        ('2','Nova mensagem'),
    )

    
    tipo=models.ForeignKey(Tipo_OS, on_delete=models.PROTECT, null=True)
    numero = models.CharField(max_length=130, verbose_name='Nº da OS', blank=True)
    prioridade =models.CharField(max_length=1, verbose_name='Prioridade', default='0', choices=PRIORIDADE_CHOICES, null=True)

    dt_solicitacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de solicitação', blank=True)
    atendente = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    
    logradouro = models.CharField(max_length=150, verbose_name='Logradouro')
    bairro = models.CharField(max_length=150, verbose_name='Bairro')
    referencia = models.CharField(max_length=200, verbose_name='Referência', blank=True)

    nome_do_contribuinte = models.CharField(max_length=200, verbose_name='Nome do contribuinte', blank=True)
    telefone_do_contribuinte = models.CharField(max_length=12, verbose_name='Telefone do contribuinte', blank=True)
    secretaria = models.ForeignKey(Secretaria, verbose_name='Secretaria', on_delete=models.CASCADE)
    setor = models.ForeignKey(Setor, verbose_name='Setor', on_delete=models.CASCADE)

    cadastrado_por = models.ForeignKey(Pessoa, on_delete=models.CASCADE, null=True)   

    motivo_reclamacao = models.TextField(verbose_name='Motivo da solicitação')            
    
    status =models.CharField(max_length=1, verbose_name='Status', choices=STATUS_CHOICES, null=True, default='0')
    pontos_atendidos=models.PositiveIntegerField(default=0)
    observacao_pontos=models.TextField(verbose_name='Observação', default='', null=True, blank=True)
    
    dt_alteracao = models.DateTimeField(verbose_name='Data de alteração', blank=True, null=True)
    dt_execucao = models.DateTimeField(verbose_name='Data de execução', blank=True, null=True)
    dt_conclusao = models.DateTimeField(verbose_name='Data de conclusão', blank=True, null=True)
    message_status = models.CharField(max_length=1, verbose_name='Status de mensagens', default='0', choices=MESSAGE_STATUS_CHOICES, null=True)
    finalizado_por = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name='ordem_finalizada_por')
    
    def semana_atendimento(self):
        return self.dt_conclusao.isocalendar()[1]

    @staticmethod
    def total_os_por_semana_ano():
        # Obtém a contagem de OS por semana e ano
        os_por_semana_ano = OrdemDeServico.objects.filter(status='f').annotate(ano=Extract('dt_conclusao', 'year'), semana=Extract('dt_conclusao', 'week')).values('ano', 'semana').annotate(total_os=Count('id'))

        # print(os_por_semana_ano)
        # Salva os valores na tabela TotalOSPorSemanaAno
        for item in os_por_semana_ano:
            ano = item['ano']
            semana = item['semana']
            total_os = item['total_os']
            # print(semana, ano, total_os)
            TotalOSPorSemanaAno.objects.create(ano=ano, semana=semana, total_os=total_os)
    
    @staticmethod
    def total_os_por_mes_ano():
        # Obtém a contagem de OS por mês
        os_por_mes = OrdemDeServico.objects.filter(status='f').annotate(ano=Extract('dt_conclusao', 'year'), mes=Extract('dt_conclusao', 'month')).values('ano', 'mes').annotate(total=Count('id'))

        # Salva os valores na tabela TotalOSPorMes
        for item in os_por_mes:            
            ano = item['ano']
            mes = item['mes']
            total_os = item['total']
            print(mes, ano, total_os)
            TotalOSPorMesAno.objects.create(ano=ano, mes=mes, total_os=total_os)


    class Meta:
        ordering = ['-dt_alteracao', '-dt_solicitacao']

    def gerar_protocolo(self):        
        self.numero = f"{self.tipo.sigla}{int(uuid.uuid4().hex[:10], 16)}/{self.dt_solicitacao.strftime('%y')}"
        self.save()
        return self.numero
    
    def save(self, *args, **kwargs):
        # Atualiza a data de alteração antes de salvar o modelo
        self.dt_alteracao = timezone.now()
        super().save(*args, **kwargs)

    def finalizar_chamado(self, user):
        
        if self.status == 'f':
            return "Chamado já foi finalizado."
            
        self.status = 'f'
        self.finalizado_por = user
        self.dt_conclusao = timezone.now()
        self.save()
        return "Chamado finalizado com sucesso."
    

class OS_ext(models.Model):    
    os=models.ForeignKey(OrdemDeServico, on_delete=models.PROTECT)
    equipe=models.ManyToManyField(Funcionario_OS, blank=True, null=True)
    cod_veiculo=models.CharField(max_length=14, verbose_name='Código do veículo', blank=True)

class OS_Linha_Tempo(models.Model):
    os=models.ForeignKey(OrdemDeServico, on_delete=models.CASCADE)
    pessoa=models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    mensagem=models.TextField()
    anexo = models.FileField(upload_to='anexos/', blank=True, null=True)
    dt_inclusao = models.DateTimeField(auto_now_add=True, verbose_name='Data da mensagem', blank=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Atualizar a data de alteração da OrdemDeServico relacionada
        self.os.save()

# Sinal para atualizar a data de alteração da OrdemDeServico após salvar uma instância de OS_Linha_Tempo
@receiver(post_save, sender=OS_Linha_Tempo)
def update_os_alteracao(sender, instance, **kwargs):
    instance.os.save()

class MateriaisUsados(models.Model):
    os=models.ForeignKey(OrdemDeServico, on_delete=models.PROTECT)
    material=models.ForeignKey(Material, on_delete=models.PROTECT)
    quantidade=models.IntegerField()


    

