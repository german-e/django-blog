from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Usuario(AbstractUser):
    foto_perfil = models.ImageField(verbose_name='Foto', upload_to='perfil', null=True, blank=True)
    

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    