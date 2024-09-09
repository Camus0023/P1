from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, Anuncio
from .forms import UsuarioForm, AnuncioForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(f"Email: {email}")
        print(f"Password: {password}")
        user = authenticate(request, email=email, password=password)
        print(f"User: {user}")
        if user is not None:
            login(request, user)
            user_role_id = user.id_rol.id
            print(f"User Role ID: {user_role_id}")
            if user_role_id == 1:  # Administrador
                return redirect('administracion_dashboard')
            elif user_role_id == 3:  # Portero
                return redirect('portero_dashboard')
            elif user_role_id == 2:  # Residente
                return redirect('residente_dashboard')
            else:
                messages.error(request, 'Rol desconocido')
        else:
            messages.error(request, 'Credenciales incorrectas')
    return render(request, 'usuarios/login.html')



def dashboard(request):
    user = request.user  # Usuario autenticado
    
    if user.id_rol.nombre == 'Administración':
        return redirect('administracion_dashboard')
    elif user.id_rol.nombre == 'Portero':
        return redirect('portero_dashboard')
    elif user.id_rol.nombre == 'Residente':
        return redirect('residente_dashboard')
    else:
        # En caso de que el rol no esté definido correctamente
        messages.error(request, 'No tienes permisos para acceder.')
        return redirect('logout')


def administracion_dashboard(request):
    usuarios = Usuario.objects.all()

    return render(request, 'usuarios/administracion_dashboard.html', {'usuarios': usuarios})

def portero_dashboard(request):
    return render(request, 'usuarios/portero_dashboard.html')

def residente_dashboard(request):
    anuncios = Anuncio.objects.all()[:5]  # Limitamos a los 5 anuncios más recientes
    return render(request, 'usuarios/residente_dashboard.html', {'anuncios': anuncios})


def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/administracion_dashboard.html', {'usuarios': usuarios})


def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()  # Esto ahora encripta la contraseña antes de guardar
            return redirect('administracion_dashboard')
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/crear_usuario.html', {'form': form})



def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('administracion_dashboard')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'usuarios/editar_usuario.html', {'form': form, 'usuario': usuario})


def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        usuario.delete()
        return redirect('administracion_dashboard')
    return render(request, 'usuarios/eliminar_usuario.html', {'usuario': usuario})


def crear_anuncio(request):
    if request.method == 'POST':
        form = AnuncioForm(request.POST)
        if form.is_valid():
            anuncio = form.save(commit=False)
            anuncio.autor = "administracion"
            anuncio.save()
            return redirect('administracion_dashboard')
    else:
        form = AnuncioForm()
    return render(request, 'usuarios/crear_anuncio.html', {'form': form})

def lista_anuncios(request):
    anuncios = Anuncio.objects.all()[:5]  # Limitamos a los 5 anuncios más recientes
    return render(request, 'lista_anuncios.html', {'anuncios': anuncios})