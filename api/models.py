from django.db import models
from django.contrib.auth.models import AbstractUser

class Paciente(models.Model):
    cpf = models.CharField(max_length=14, primary_key=True)
    nome = models.CharField(max_length=60)
    nome_social = models.CharField(max_length=60, blank=True)
    cns = models.IntegerField()
    filas = models.ManyToManyField('Fila', through='Alocacao')

class Endereco(models.Model):
    uf = models.CharField(max_length=2)
    cidade = models.CharField(max_length=30)
    bairro = models.CharField(max_length=30)
    complemento = models.CharField(max_length=30)
    cep = models.CharField(max_length=30)
    paciente = models.ForeignKey(Paciente, to_field='cpf', on_delete=models.CASCADE, related_name="endereco", null=True)

class Cadastro(AbstractUser):
    username = None
    cpf = models.CharField(max_length=14, primary_key=True)
    paciente = models.ForeignKey(Paciente, to_field='cpf', on_delete=models.CASCADE, related_name='cadastro', null=True)

    USERNAME_FIELD = 'cpf'

class Fila(models.Model):
    nome_fila = models.CharField(max_length=45)
    especialidade = models.CharField(max_length=45)

class Agendamento(models.Model):
    class Preferences(models.TextChoices):
        NO_PREFERENCE = "SEM PREFERÊNCIA", "Sem preferência"
        DEFICIENTE = "DEFICIENTE", "Deficiente"
        IDOSO = "IDOSO", "Idoso"
        GESTANTE = "GESTANTE", "Gestante"
        LACTANTE = "LACTANTE", "Lactante"
        OBESO = "OBESO", "Obeso"
        CRIANÇA_COLO = "CRIANÇA DE COLO", "Criança de colo"

    data_prevista = models.DateField(null=True)
    data_conclusao = models.DateField(null=True)
    especialidade = models.CharField(max_length=45)
    descricao = models.TextField()
    preferencia = models.CharField(max_length=25, choices=Preferences.choices, blank=True)
    paciente = models.ForeignKey(Paciente, to_field='cpf', on_delete=models.CASCADE)

class Alocacao(models.Model):
    paciente = models.ForeignKey(Paciente, related_name="alocacao", to_field='cpf', on_delete=models.CASCADE)
    fila = models.ForeignKey(Fila, to_field='id', on_delete=models.CASCADE)
    posicao = models.IntegerField(null=True)
    atendido = models.BooleanField(default=False)
    agendamento = models.ForeignKey(Agendamento, to_field='id', related_name="agendamento", on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        agendamento = kwargs.pop("agendamento", None)
        self.agendamento = agendamento

        super(Alocacao, self).save(*args, **kwargs)
