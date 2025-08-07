from django.db import models
from django.utils.html import strip_tags
from django.utils.text import Truncator
from apps.usuarios.models import Usuario
from ckeditor.fields import RichTextField

class Tag(models.Model):
    nombre = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.nombre
    
    @property
    def cantidad_usos(self):
        return self.post_set.count()

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)


    def __str__(self):
        return f'{self.nombre}'

# Create your models here.
class Post(models.Model):
    titulo = models.CharField(max_length=100, null=False, blank=False)    
    subtitulo = models.CharField(max_length=200)
    contenido = RichTextField()
    imagen = models.ImageField(upload_to='Post')
    fecha_publicacion = models.DateTimeField(auto_now=True)
    publicado_por = models.ForeignKey(to=Usuario, on_delete=models.RESTRICT)
    publicado = models.BooleanField(default=False, verbose_name='Publicar ahora')
    categorias = models.ManyToManyField(to=Categoria, related_name='posts', blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    likes = models.ManyToManyField(Usuario, related_name='likes', blank=True)
    destacado = models.BooleanField(default=False)  
    class Meta:
        ordering = ['-fecha_publicacion']


    def total_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return f'{self.titulo} [{self.fecha_publicacion}]'
    
    def le_dio_like(self, user):
        return self.likes.filter(pk=user.pk).exists()
    
    def vista_previa(self):
        return Truncator( strip_tags(self.contenido)).words(25)
