from xml.etree.ElementInclude import default_loader

from django.db import models
from stdimage.models import StdImageField
from django.contrib.auth.models import User
from .utils.funcs import get_filename


class Base(models.Model):

    create = models.DateTimeField('CreateAt', auto_now_add=True)
    change = models.DateField('ChangesTo', auto_now=True)
    status = models.BooleanField('Status', default=True)

    class Meta:
        abstract = True

class Profile(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = StdImageField('user_image',
                          variations={'thumb': {'width': 480, 'height': 480, 'crop': True}},
                          upload_to=get_filename,
                          null=True,
                          blank=True,
                          default='default/default_profile.thumb.png')

    def __str__(self):
        return f'Profile of {self.user.username}'

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
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='usuario', null=True)
    teste = models.BooleanField

    class Meta:
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'

    def __str__(self):
        return self.title


class Project(Base):

    title = models.CharField('Title', max_length=120)