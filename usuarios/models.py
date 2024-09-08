from django.db import models
from django.utils import timezone

class Rol(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Unidad(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Torre(models.Model):
    id_unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Piso(models.Model):
    id_torre = models.ForeignKey(Torre, on_delete=models.CASCADE)
    numero = models.IntegerField()

    def __str__(self):
        return f"Piso {self.numero} - {self.id_torre.nombre}"

class Apartamento(models.Model):
    id_piso = models.ForeignKey(Piso, on_delete=models.CASCADE)
    numero = models.IntegerField()

    def __str__(self):
        return f"Apartamento {self.numero} - {self.id_piso}"

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    id_apartamento = models.ForeignKey(Apartamento, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.email}"


class Anuncio(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['-fecha_publicacion']