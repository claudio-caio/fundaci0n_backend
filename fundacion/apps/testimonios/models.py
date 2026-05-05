from django.db import models

class Testimonio(models.Model):
    nombre = models.CharField(max_length=255)
    rol = models.CharField(max_length=255)  # estudiante, empresario, etc
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='testimonios/', blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
