
from django.db import models
from django.conf import settings

class Curso(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Modulo(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='modulos')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    video = models.URLField()
    material = models.URLField(blank=True, null=True)
    orden = models.IntegerField()

    def __str__(self):
        return f"{self.curso.nombre} - {self.titulo}"
    
class Inscripcion(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='inscripciones')

    # 👇 NUEVO (clave)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='course_inscriptions'
    )

    # 👇 lo mantenemos por ahora
    nombre = models.CharField(max_length=200)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)

    activo = models.BooleanField(default=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.usuario:
            return f"{self.usuario.username} - {self.curso.nombre}"
        return f"{self.nombre} - {self.curso.nombre}"    