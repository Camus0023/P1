from django import forms
from django.contrib.auth.hashers import make_password
from .models import Usuario, Anuncio

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
