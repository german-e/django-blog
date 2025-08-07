from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, View, UpdateView

from .models import Post, Categoria, Tag
from .forms import PostForm
from apps.comentarios.forms import ComentarioForm
from django.db.models import Q

class CrearPostView(LoginRequiredMixin, CreateView):
    
    form_class = PostForm
    template_name = 'crear_post.html'

    def form_valid(self, form):
        form.instance.publicado_por = self.request.user  # ⚠️ Esto es clave
        response = super().form_valid(form)
    
        tags_input = self.request.POST.getlist('tags')
        for nombre in tags_input:
            nombre_limpio = nombre.strip()
            if nombre_limpio:
                tag, _ = Tag.objects.get_or_create(nombre=nombre_limpio)

                self.object.tags.add(tag)
        return response

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})
        
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'  # tu template
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['comentarios'] = self.object.comentarios.order_by('-fecha_creacion')
        context['form_comentario'] = ComentarioForm()
        
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ComentarioForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            comentario = form.save(commit=False)
            comentario.post = self.object
            comentario.autor = request.user
            comentario.save()
        return redirect('post_detail', pk=self.object.pk)

    
class PostsPorTagView(ListView):
    template_name = 'posts_por_tag.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(tags__nombre=self.kwargs['nombre'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.kwargs['nombre']
        return context

class PostListView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'

    paginate_by = 6

    def get_queryset(self):        
        return Post.objects.filter(publicado=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['destacados'] = Post.objects.filter(publicado=True, destacado=True).order_by('-fecha_publicacion')[:3]
        context['ultimo_destacado'] = Post.objects.filter(publicado=True, destacado=True).order_by('-fecha_publicacion').first()        
        
        return context
    
class PostListPorUsuario(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.filter(publicado_por=self.request.user)

    
class EditarPostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'crear_post.html'
    form_class = PostForm


    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.publicado_por  #Solo editar el autor del post logueado
   
    




class PostsPorCategoriaView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.categoria = Categoria.objects.get(slug=self.kwargs['slug'])
        return Post.objects.filter(categorias=self.categoria, publicado=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoria_actual'] = self.categoria
        return context



class DarLikeView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)

        if post.likes.filter(pk=request.user.pk).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return redirect('post_detail', pk=pk)


#Para no recargar la página, usa javascript (en archivo js/script.js)
class DarLikeAjaxView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        dio_like = False

        if post.le_dio_like(user):
            post.likes.remove(user)
        else:
            post.likes.add(user)
            dio_like = True

        return JsonResponse({
            'likes': post.likes.count(),
            'dio_like': dio_like
        })

class BuscarPostView(ListView):
    model = Post
    template_name = 'posts_resultados_busqueda.html'
    context_object_name = 'posts'

    def get_queryset(self):
        consulta = self.request.GET.get('q')
        if consulta:
            return Post.objects.filter(
                Q(titulo__icontains=consulta) |
                Q(contenido__icontains=consulta),
                publicado=True
            ).distinct()
        return Post.objects.none()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context