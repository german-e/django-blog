from django.contrib import admin
from .models import Post, Categoria
# Register your models here.
class PublicacionAdmin(admin.ModelAdmin):
    list_display = ['id', 'titulo', 'publicado_por', 'fecha_publicacion', 'publicado', 'destacado']


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre']

admin.site.register(Post, PublicacionAdmin)
admin.site.register(Categoria, CategoriaAdmin)
