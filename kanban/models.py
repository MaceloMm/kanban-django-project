from django.db import models
from stdimage.models import StdImageField


class Base(models.Model):

    create = models.DateTimeField('CreateAt', auto_now_add=True)
    change = models.DateField('ChangesTo', auto_now=True)
    status = models.BooleanField('Status', default=True)

    class Meta:
        abstract = True


class Task(Base):

    STATUS_CHOICES = [
        ('NI', 'Não iniciado'),
        ('EA', 'Em Andamento'),
        ('CL', 'Concluido')
    ]

    title = models.CharField('Title', max_length=120)
    description = models.CharField('Description', max_length=220)
    task_status = models.CharField('Task Status', max_length=12, choices=STATUS_CHOICES, default='NI')
    task_conclusion = models.DateTimeField('Ended', null=True, blank=True)

    class Meta:
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'

    def __str__(self):
        return self.title
