from django.urls import path
from django.contrib.auth.views import  LogoutView
from .views import RegistroView, CustomLoginView, AjaxLoginView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('iniciar-sesion/', AjaxLoginView.as_view(), name='ajax_login'),
    path('registro/', RegistroView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(),name='logout' )
]

if (settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)