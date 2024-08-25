from django import forms
from .models import Usuario, Apartamento, Rol

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'email', 'password', 'id_rol', 'id_apartamento']
        widgets = {
            'password': forms.PasswordInput(),
        }
