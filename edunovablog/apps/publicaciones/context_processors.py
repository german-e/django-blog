from .models import Categoria, Tag
def categorias_disponibles(request):
    return {
        'categorias': Categoria.objects.all().order_by('nombre')
    }

def tags_registrados(request):
    return {
        'tags': Tag.objects.all().order_by('nombre')
    }