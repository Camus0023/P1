from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('crear/', views.crear_usuario, name='crear_usuario'),
    path('editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    
    path('', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('portero/', views.portero_dashboard, name='portero_dashboard'),
    path('residente/', views.residente_dashboard, name='residente_dashboard'),
    path('administracion/', views.administracion_dashboard, name='administracion_dashboard'),

    path('crear_anuncio/', views.crear_anuncio, name='crear_anuncio'),
    path('anuncios/', views.lista_anuncios, name='lista_anuncios'),

     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
