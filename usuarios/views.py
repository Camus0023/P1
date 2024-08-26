from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario
from .forms import UsuarioForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages



def user_login(request):
    return render(request, 'usuarios/login.html')


def dashboard(request):
    user = request.user
    if user.rol.nombre == 'Administración':
        return redirect('administracion_dashboard')
    elif user.rol.nombre == 'Portero':
        return redirect('portero_dashboard')
    elif user.rol.nombre == 'Residente':
        return redirect('residente_dashboard')
    else:
        # Redirigir a una página de error o logout
        return redirect('logout')
    
def administracion_dashboard(request):
    return render(request, 'usuarios/administracion_dashboard.html')

def portero_dashboard(request):
    return render(request, 'usuarios/portero_dashboard.html')

def residente_dashboard(request):
    return render(request, 'usuarios/residente_dashboard.html')


def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})


def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/crear_usuario.html', {'form': form})


def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'usuarios/editar_usuario.html', {'form': form, 'usuario': usuario})


def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        usuario.delete()
        return redirect('lista_usuarios')
    return render(request, 'usuarios/eliminar_usuario.html', {'usuario': usuario})
