from django.urls import path, include
from .views import CrearPostView, PostDetailView, PostsPorCategoriaView, BuscarPostView, DarLikeAjaxView, PostListPorUsuario, EditarPostView, PostsPorTagView

from django.views.generic import TemplateView
urlpatterns = [
    path('nuevo-post/', CrearPostView.as_view(), name='crear_post'),
    path('post/mis-post', PostListPorUsuario.as_view(), name='mis_post' ),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/categoria/<slug:slug>/', PostsPorCategoriaView.as_view(), name='posts_por_categoria'),
    path('tag/<str:nombre>/', PostsPorTagView.as_view(), name='posts_por_tag'),
    path('post/<int:pk>/like/', DarLikeAjaxView.as_view(), name='dar_like_ajax'),
    path('post/<int:pk>/editar/', EditarPostView.as_view(), name='editar_post'),
    path('buscar/', BuscarPostView.as_view(), name='buscar_posts'),
]