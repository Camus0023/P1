from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, Anuncio, Apartamento, Piso, Torre, Visita, Unidad, Paquete, Proveedor, Domicilio
from .forms import UsuarioForm, AnuncioForm, PaqueteForm, DomicilioForm, VisitaForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
import qrcode
from PIL import Image
from pyzbar.pyzbar import decode

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
                return redirect('administrador_dashboard')
            elif user_role_id == 3:  # Portero
                return redirect('portero_dashboard')
            elif user_role_id == 2:  # Residente
                return redirect('residente_dashboard')
            else:
                messages.error(request, 'Rol desconocido')
        else:
            messages.error(request, 'Credenciales incorrectas')
    return render(request, 'usuarios/auth/login.html')  # Actualizado a la nueva estructura


def dashboard(request):
    user = request.user  # Usuario autenticado
    
    if user.id_rol.nombre == 'Administración':
        return redirect('administrador_dashboard')
    elif user.id_rol.nombre == 'Portero':
        return redirect('portero_dashboard')
    elif user.id_rol.nombre == 'Residente':
        return redirect('residente_dashboard')
    else:
        # En caso de que el rol no esté definido correctamente
        messages.error(request, 'No tienes permisos para acceder.')
        return redirect('logout')


def administrador_dashboard(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/administrador/dashboard.html', {'usuarios': usuarios})  # Actualizado a la nueva estructura

def residente_dashboard(request):
    anuncios = Anuncio.objects.all()[:5]  # Limitamos a los 5 anuncios más recientes
    return render(request, 'usuarios/residente/dashboard.html', {'anuncios': anuncios})  # Actualizado a la nueva estructura


def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/administrador/dashboard.html', {'usuarios': usuarios})  # Actualizado a la nueva estructura


def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('administrador_dashboard')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'usuarios/administrador/editar_usuario.html', {'form': form, 'usuario': usuario})  # Actualizado a la nueva estructura


def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        usuario.delete()
        return redirect('administrador_dashboard')
    return render(request, 'usuarios/administrador/eliminar_usuario.html', {'usuario': usuario})  # Actualizado a la nueva estructura


def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('administrador_dashboard')
    else:
        form = UsuarioForm()  # Asegúrate de inicializar el formulario

    return render(request, 'usuarios/administrador/crear_usuario.html', {'form': form})

def crear_anuncio(request):
    if request.method == 'POST':
        form = AnuncioForm(request.POST)
        if form.is_valid():
            anuncio = form.save(commit=False)
            anuncio.autor = "administracion"
            anuncio.save()
            return redirect('administrador_dashboard')
    else:
        form = AnuncioForm()  # Asegúrate de inicializar el formulario

    return render(request, 'usuarios/administrador/crear_anuncio.html', {'form': form})



def lista_anuncios(request):
    anuncios = Anuncio.objects.all()[:5]  # Limitamos a los 5 anuncios más recientes
    return render(request, 'usuarios/residente/lista_anuncios.html', {'anuncios': anuncios})  # Actualizado a la nueva estructura


def nueva_visita(request):
    if request.method == 'POST':
        form = VisitaForm(request.POST)
        if form.is_valid():
            visita = form.save(commit=False)
            visita.apartamento = request.user.id_apartamento  # Asignar la visita al apartamento del residente
            visita.save()

            if visita.es_frecuente:  # Si es una visita frecuente, redirigir a la vista de confirmación
                return redirect('confirmacion_visita_frecuente', visita_id=visita.id)

            messages.success(request, "Visita registrada correctamente.")
            return redirect('residente_dashboard')
    else:
        form = VisitaForm()
    return render(request, 'usuarios/residente/nueva_visita.html', {'form': form})


def confirmacion_visita_frecuente(request, visita_id):
    visita = get_object_or_404(Visita, id=visita_id)
    return render(request, 'usuarios/residente/confirmacion_visita_frecuente.html', {'visita': visita})


# Vista para registrar un nuevo domicilio
def nuevo_domicilio(request):
    proveedores_domicilio = Proveedor.objects.filter(tipo='domicilio')

    if request.method == 'POST':
        form = DomicilioForm(request.POST)
        if form.is_valid():
            domicilio = form.save(commit=False)
            proveedor = form.cleaned_data['proveedor']
            proveedor_personalizado = form.cleaned_data.get('proveedor_personalizado')

            # Verificar si se seleccionó "Otro" y se proporciona un proveedor personalizado
            if proveedor.nombre == 'Otro' and proveedor_personalizado:
                nuevo_proveedor = Proveedor.objects.create(nombre=proveedor_personalizado, tipo='domicilio')
                domicilio.proveedor = nuevo_proveedor

            domicilio.apartamento = request.user.id_apartamento
            domicilio.estado = 'pendiente'  # Estado por defecto "pendiente"
            domicilio.save()

            messages.success(request, "Domicilio registrado correctamente y está pendiente de confirmación.")
            return redirect('residente_dashboard')
        else:
            messages.error(request, "Por favor corrija los errores en el formulario.")
    else:
        form = DomicilioForm()

    return render(request, 'usuarios/residente/nuevo_domicilio.html', {'form': form, 'proveedores_domicilio': proveedores_domicilio})

# Vista para registrar un nuevo paquete
def nuevo_paquete(request):
    proveedores_paquete = Proveedor.objects.filter(tipo='paquete')

    if request.method == 'POST':
        form = PaqueteForm(request.POST)
        if form.is_valid():
            paquete = form.save(commit=False)
            # Verificar si se seleccionó "Otro" y se proporcionó un proveedor personalizado
            if form.cleaned_data.get('proveedor').nombre == 'Otro':
                # Crear un nuevo proveedor con el nombre personalizado
                nuevo_proveedor = Proveedor.objects.create(
                    nombre=form.cleaned_data.get('proveedor_personalizado'),
                    tipo='paquete'
                )
                paquete.proveedor = nuevo_proveedor
            paquete.apartamento = request.user.id_apartamento
            paquete.estado = 'pendiente'  # Estado por defecto "pendiente"
            paquete.save()

            messages.success(request, "Paquete registrado correctamente y está pendiente de confirmación.")
            return redirect('residente_dashboard')
        else:
            messages.error(request, "Por favor corrija los errores en el formulario.")
    else:
        form = PaqueteForm()

    return render(request, 'usuarios/residente/nuevo_paquete.html', {'form': form, 'proveedores_paquete': proveedores_paquete})


def portero_dashboard(request):
    # Obtener la primera unidad disponible
    unidad = Unidad.objects.first()
    
    # Si hay una unidad disponible, mostrar sus torres
    if unidad:
        torres = Torre.objects.filter(id_unidad=unidad)
    else:
        torres = []

    return render(request, 'usuarios/portero/torres.html', {'torres': torres, 'unidad': unidad})

def portero_apartamentos(request, piso_id):
    piso = get_object_or_404(Piso, id=piso_id)
    apartamentos = Apartamento.objects.filter(id_piso=piso)

    return render(request, 'usuarios/portero/apartamentos.html', {
        'piso': piso,
        'apartamentos': apartamentos
    })

def portero_pisos(request, torre_id):
    torre = get_object_or_404(Torre, id=torre_id)
    pisos = Piso.objects.filter(id_torre=torre)
    return render(request, 'usuarios/portero/pisos.html', {'torre': torre, 'pisos': pisos})


def portero_detalle_apartamento(request, apartamento_id):
    apartamento = get_object_or_404(Apartamento, id=apartamento_id)
    
    # Obtener visitas, domicilios y paquetes pendientes asociados al apartamento
    visitas_pendientes = Visita.objects.filter(apartamento=apartamento, estado='pendiente')
    domicilios_pendientes = Domicilio.objects.filter(apartamento=apartamento, estado='pendiente')
    paquetes_pendientes = Paquete.objects.filter(apartamento=apartamento, estado='pendiente')

    # Confirmar solicitudes (si el portero confirma algo)
    if request.method == 'POST':
        solicitud_id = request.POST.get('solicitud_id')
        tipo = request.POST.get('tipo')
        
        if tipo == 'visita':
            Visita.objects.filter(id=solicitud_id).update(estado='confirmada')
            messages.success(request, "Visita confirmada correctamente.")
        elif tipo == 'domicilio':
            Domicilio.objects.filter(id=solicitud_id).update(estado='confirmado')
            messages.success(request, "Domicilio confirmado correctamente.")
        elif tipo == 'paquete':
            Paquete.objects.filter(id=solicitud_id).update(estado='confirmado')
            messages.success(request, "Paquete confirmado correctamente.")

        return redirect('portero_detalle_apartamento', apartamento_id=apartamento_id)

    # Renderizar la plantilla con las solicitudes pendientes
    return render(request, 'usuarios/portero/detalle_apartamento.html', {
        'apartamento': apartamento,
        'visitas_pendientes': visitas_pendientes,
        'domicilios_pendientes': domicilios_pendientes,
        'paquetes_pendientes': paquetes_pendientes,
    })


def verificar_qr(request, apartamento_id):
    if request.method == 'POST':
        imagen_qr = request.FILES['qr_image']
        
        # Procesar la imagen del QR
        img = Image.open(imagen_qr)
        decodificado = decode(img)
        
        if not decodificado:
            messages.error(request, "El QR no pudo ser leído.")
            return redirect('portero_detalle_apartamento', apartamento_id=apartamento_id)
        
        mensaje_qr_leido = decodificado[0].data.decode('utf-8')
        
        # Buscar si el mensaje QR coincide con alguna visita frecuente
        visita = Visita.objects.filter(mensaje_qr=mensaje_qr_leido, estado='pendiente', apartamento_id=apartamento_id).first()
        
        if visita:
            # Confirmar la visita
            visita.estado = 'confirmada'
            visita.save()
            messages.success(request, f"La visita de {visita.nombre_visitante} ha sido confirmada.")
        else:
            messages.error(request, "El QR no coincide con ninguna visita registrada.")
        
        return redirect('portero_detalle_apartamento', apartamento_id=apartamento_id)

    return render(request, 'usuarios/portero/verificar_qr.html', {'apartamento_id': apartamento_id})

def pendientes_portero(request):
    # Obtener todas las visitas, domicilios y paquetes que estén en estado 'pendiente'
    visitas_pendientes = Visita.objects.filter(estado='pendiente')
    domicilios_pendientes = Domicilio.objects.filter(estado='pendiente')
    paquetes_pendientes = Paquete.objects.filter(estado='pendiente')
    
    # Pasamos las listas de pendientes al template
    return render(request, 'usuarios/portero/pendientes.html', {
        'visitas_pendientes': visitas_pendientes,
        'domicilios_pendientes': domicilios_pendientes,
        'paquetes_pendientes': paquetes_pendientes,
    })

def pendientes_residente(request):
    # Obtener el apartamento del residente actual
    apartamento = request.user.id_apartamento

    # Consultar los pendientes del apartamento del residente
    paquetes_pendientes = Paquete.objects.filter(apartamento=apartamento, estado='pendiente')
    domicilios_pendientes = Domicilio.objects.filter(apartamento=apartamento, estado='pendiente')
    visitas_no_anunciadas = Visita.objects.filter(apartamento=apartamento, estado='no_anunciada')

    context = {
        'paquetes_pendientes': paquetes_pendientes,
        'domicilios_pendientes': domicilios_pendientes,
        'visitas_no_anunciadas': visitas_no_anunciadas,
    }

    return render(request, 'usuarios/residente/pendientes.html', context)


def historial_residente(request):
    # Obtener el apartamento del residente actual
    apartamento = request.user.id_apartamento

    # Historial de lo que ha recibido
    paquetes_recibidos = Paquete.objects.filter(apartamento=apartamento, estado='confirmado')
    domicilios_recibidos = Domicilio.objects.filter(apartamento=apartamento, estado='confirmado')
    visitas_recibidas = Visita.objects.filter(apartamento=apartamento, estado='confirmada')

    # Historial de lo que el residente ha enviado
    visitas_enviadas = Visita.objects.filter(apartamento=apartamento)
    domicilios_enviados = Domicilio.objects.filter(apartamento=apartamento)
    paquetes_enviados = Paquete.objects.filter(apartamento=apartamento)

    context = {
        'paquetes_recibidos': paquetes_recibidos,
        'domicilios_recibidos': domicilios_recibidos,
        'visitas_recibidas': visitas_recibidas,
        'visitas_enviadas': visitas_enviadas,
        'domicilios_enviados': domicilios_enviados,
        'paquetes_enviados': paquetes_enviados,
    }

    return render(request, 'usuarios/residente/historial.html', context)


def historial_portero(request):
    # Obtener todo lo que ha sido confirmado
    visitas_confirmadas = Visita.objects.filter(estado='confirmada')
    domicilios_confirmados = Domicilio.objects.filter(estado='confirmado')
    paquetes_confirmados = Paquete.objects.filter(estado='confirmado')

    context = {
        'visitas_confirmadas': visitas_confirmadas,
        'domicilios_confirmados': domicilios_confirmados,
        'paquetes_confirmados': paquetes_confirmados,
    }

    return render(request, 'usuarios/portero/historial.html', context)

