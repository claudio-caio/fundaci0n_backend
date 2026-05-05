from django.db import models

class CasoExito(models.Model):

    SECTORES = [
        ('empresa', 'Empresas'),
        ('institucion', 'Instituciones'),
        ('coaching', 'Coaching Personalizado'),
    ]

    sector = models.CharField(max_length=20, choices=SECTORES)
    cliente = models.CharField(max_length=100)
    problema = models.TextField()
    capacitacion = models.TextField()
    resultado = models.TextField()
    testimonio = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='trayectoria/', blank=True, null=True)
    fecha = models.DateField()

    @property
    def imagen_url(self):
        if self.imagen:
            return self.imagen.url
        return None

    def __str__(self):
        return f"{self.cliente} - {self.sector}"



class CasoExitoImagen(models.Model):
    caso = models.ForeignKey(CasoExito, related_name='galeria', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='trayectoria/galeria/')
    titulo = models.CharField(max_length=120, blank=True)
    descripcion = models.CharField(max_length=255, blank=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('orden',)

    def __str__(self):
        return f"Imagen {self.orden} - {self.caso.cliente}"