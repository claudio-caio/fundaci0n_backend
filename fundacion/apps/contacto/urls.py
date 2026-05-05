from django.urls import path
from .views import contacto_email

urlpatterns = [
    path('', contacto_email),
]