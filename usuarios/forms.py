from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'email', 'password', 'id_rol', 'id_apartamento']
        widgets = {
            'password': forms.PasswordInput(),
        }
