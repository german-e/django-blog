from django.db import models

from apps.publicaciones.models import Post
from apps.usuarios.models import Usuario


# Create your models here.
class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='comentarios')
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    aprobado = models.BooleanField(default=True)

    class Meta:
        ordering = ['fecha_creacion']

    def __str__(self):
        return f'Comentario de {self.autor.username} en "{self.post.titulo}"'