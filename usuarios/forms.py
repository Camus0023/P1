from django import forms
from django.contrib.auth.hashers import make_password
from .models import Usuario, Anuncio, Visita, Domicilio, Paquete

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'email', 'password', 'id_rol', 'id_apartamento']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        # Sobrescribir el método save para encriptar la contraseña
        usuario = super(UsuarioForm, self).save(commit=False)
        usuario.password = make_password(self.cleaned_data['password'])  # Encriptar la contraseña
        if commit:
            usuario.save()
        return usuario
    
class AnuncioForm(forms.ModelForm):
    class Meta:
        model = Anuncio
        fields = ['titulo', 'contenido']


# Formulario para registrar una nueva visita
class VisitaForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields = ['nombre_visitante', 'apellido_visitante', 'fecha_visita', 'es_frecuente', 'fecha_expiracion_frecuente']
        widgets = {
            'fecha_visita': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_expiracion_frecuente': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        es_frecuente = cleaned_data.get('es_frecuente')
        fecha_expiracion_frecuente = cleaned_data.get('fecha_expiracion_frecuente')

        # Validar que si es frecuente, debe tener fecha de expiración
        if es_frecuente and not fecha_expiracion_frecuente:
            raise forms.ValidationError("Las visitas frecuentes deben tener una fecha de expiración.")
        
        return cleaned_data

# Formulario para registrar un nuevo domicilio
class DomicilioForm(forms.ModelForm):
    class Meta:
        model = Domicilio
        fields = ['proveedor', 'proveedor_personalizado', 'nombre_producto']

    def clean(self):
        cleaned_data = super().clean()
        proveedor = cleaned_data.get('proveedor')
        proveedor_personalizado = cleaned_data.get('proveedor_personalizado')

        # Validar si se seleccionó "Otro", entonces debe ingresar el proveedor personalizado
        if proveedor and proveedor.nombre == 'Otro' and not proveedor_personalizado:
            raise forms.ValidationError("Debe especificar el nombre del proveedor personalizado si selecciona 'Otro'.")
        
        return cleaned_data
    


class PaqueteForm(forms.ModelForm):
    class Meta:
        model = Paquete
        fields = ['proveedor', 'proveedor_personalizado', 'nombre_producto', 'fecha_estimacion']

    def clean(self):
        cleaned_data = super().clean()
        proveedor = cleaned_data.get('proveedor')
        proveedor_personalizado = cleaned_data.get('proveedor_personalizado')

        # Validar si se seleccionó "Otro", entonces debe ingresar el proveedor personalizado
        if proveedor and proveedor.nombre == 'Otro' and not proveedor_personalizado:
            raise forms.ValidationError("Debe especificar el nombre del proveedor personalizado si selecciona 'Otro'.")
        
        return cleaned_data
