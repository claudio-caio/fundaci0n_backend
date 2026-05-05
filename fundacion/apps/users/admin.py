from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # Lo que se ve en la lista
    list_display = ('username', 'email', 'telefono', 'is_active')

    # Para buscar
    search_fields = ('username', 'email')

    # Filtros
    list_filter = ('is_active', 'is_staff')

    # Ordenar el formulario
    fieldsets = (
        ('Información personal', {
            'fields': ('username', 'email', 'telefono')
        }),
        ('Contraseña', {
            'fields': ('password',)
        }),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Fechas importantes', {
            'fields': ('last_login', 'date_joined')
        }),
    )

admin.site.register(User, CustomUserAdmin)