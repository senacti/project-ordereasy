"""
URL configuration for OrderEasy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import MenuItem
from django.conf import settings
from django.conf.urls.static import static
from .views import exclusive_offers_view


urlpatterns = [
    path('admin/', admin.site.urls, name='admin:index'),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('pedido/', views.hacer_pedido, name='pedido'),
    path('pedido/<int:pedido_id>/cancelar/', views.cancelar_pedido, name='cancelar_pedido'),
    path('pedido/<int:pedido_id>/confirmacion/', views.confirmacion_pedido, name='confirmacion_pedido'),
    path('register/', views.registro, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('menu/', MenuItem, name='menu'),
    path('ofertas/', exclusive_offers_view, name='ofertas'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
