from django.db import models

# Create your models here.

from django.db import models

class Profissional(models.Model):
    id = models.BigAutoField(primary_key=True)  
    nome = models.CharField(max_length=100)
    nome_social = models.CharField(max_length=100, blank=True, null=True)
    especialidade = models.CharField(max_length=100, blank=False, null=False)
    data_nascimento = models.DateField(blank=False, null=False)

    def __str__(self):
       return self.nome_social if self.nome_social and self.nome_social.strip() else self.nome


class Consulta(models.Model):
    id = models.BigAutoField(primary_key=True)
    profissional = models.ForeignKey(
        'Profissional',
        on_delete=models.CASCADE,
        related_name='consultas_profissional',
    )
    nome_paciente = models.CharField(
        max_length=100,
        blank=False,
        null=False,
    )
    data_consulta = models.DateTimeField(blank=False, null=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    observacoes = models.TextField(blank=True, null=True)
    STATUS_CHOICES = [
        ('AGENDADA', 'Agendada'),
        ('CONFIRMADA', 'Confirmada'),
        ('REALIZADA', 'Realizada'),
        ('CANCELADA', 'Cancelada'),
        ('FALTOU', 'Paciente faltou'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AGENDADA')

    class Meta:
        ordering = ['-data_consulta']
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'

    def __str__(self):
        data_formatada = self.data_consulta.strftime("%d/%m/%Y às %H:%M")
        return f"Consulta de {self.nome_paciente} com {self.profissional} em {data_formatada}"