from django.db import models
from django.conf import settings
from apps.courses.models import Curso


class Payment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pendiente"),
        ("approved", "Aprobado"),
        ("rejected", "Rechazado"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Curso', on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pago {self.payment_id} - {self.user} - {self.status}"

    class Meta:
        ordering = ["-created_at"]