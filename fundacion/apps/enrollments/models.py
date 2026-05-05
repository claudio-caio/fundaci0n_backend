from django.db import models
from django.conf import settings
from apps.courses.models import Curso

class Inscripcion(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    curso = models.ForeignKey('courses.Curso', on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='activo')

    def __str__(self):
        return f"{self.usuario} - {self.curso}"

# Create your models here.
