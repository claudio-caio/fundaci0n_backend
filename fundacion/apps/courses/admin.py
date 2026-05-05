from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.utils.html import format_html

from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats

from .models import Curso
from apps.enrollments.models import Inscripcion
from .resources import InscripcionResource


# 🔥 Admin para cursos (CON BOTÓN EXPORTAR)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'activo', 'boton_exportar')
    search_fields = ('nombre',)
    list_filter = ('activo',)

    # 👉 Botón en la tabla
    def boton_exportar(self, obj):
        return format_html(
            '<a class="button" href="{}">📥 Exportar</a>',
            f'{obj.id}/exportar/'
        )
    boton_exportar.short_description = 'Exportar'

    # 👉 URL personalizada
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:curso_id>/exportar/',
                self.admin_site.admin_view(self.exportar_inscripciones),
                name='exportar_inscripciones',
            ),
        ]
        return custom_urls + urls

    # 👉 Lógica de exportación
    def exportar_inscripciones(self, request, curso_id):
        inscripciones = Inscripcion.objects.filter(curso_id=curso_id)
        dataset = InscripcionResource().export(inscripciones)

        formato = base_formats.XLSX()
        response = HttpResponse(
            formato.export_data(dataset),
            content_type=formato.get_content_type()
        )

        # 🔥 Nombre más profesional (usa el nombre del curso)
        curso = Curso.objects.get(id=curso_id)
        nombre_archivo = curso.nombre.replace(" ", "_").lower()

        response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}_inscripciones.xlsx"'
        return response


# 🔥 Admin de inscripciones
class InscripcionAdmin(ImportExportModelAdmin):
    resource_class = InscripcionResource

    list_display = ('usuario_nombre', 'usuario_email', 'usuario_telefono', 'curso', 'estado', 'fecha_inscripcion')
    search_fields = ('usuario__username', 'usuario__email', 'curso__nombre')
    list_filter = ('estado', 'curso', 'fecha_inscripcion')
    readonly_fields = ('fecha_inscripcion',)
    
    def usuario_nombre(self, obj):
        return obj.usuario.username if obj.usuario else '-'
    usuario_nombre.short_description = 'Usuario'
    
    def usuario_email(self, obj):
        return obj.usuario.email if obj.usuario else '-'
    usuario_email.short_description = 'Email'
    
    def usuario_telefono(self, obj):
        return obj.usuario.telefono if obj.usuario else '-'
    usuario_telefono.short_description = 'Teléfono'

    actions = ['exportar_seleccionadas']
    
    def exportar_seleccionadas(self, request, queryset):
        dataset = self.resource_class().export(queryset)
        formato = base_formats.XLSX()
        response = HttpResponse(
            formato.export_data(dataset),
            content_type=formato.get_content_type()
        )
        response['Content-Disposition'] = 'attachment; filename="inscripciones.xlsx"'
        return response

    exportar_seleccionadas.short_description = "📥 Exportar seleccionadas"

    actions = ['exportar_por_curso']

    def exportar_por_curso(self, request, queryset):
        dataset = self.resource_class().export(queryset)
        formato = base_formats.XLSX()
        response = HttpResponse(
            formato.export_data(dataset),
            content_type=formato.get_content_type()
        )
        response['Content-Disposition'] = 'attachment; filename="inscripciones.xlsx"'
        return response

    exportar_por_curso.short_description = "📥 Exportar seleccionadas"


# Registramos
admin.site.register(Curso, CursoAdmin)
admin.site.register(Inscripcion, InscripcionAdmin)