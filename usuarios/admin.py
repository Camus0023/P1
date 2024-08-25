from django.contrib import admin
from .models import Rol, Unidad, Torre, Piso, Apartamento, Usuario

admin.site.register(Rol)
admin.site.register(Unidad)
admin.site.register(Torre)
admin.site.register(Piso)
admin.site.register(Apartamento)
admin.site.register(Usuario)