from django.contrib import admin
from django.utils.html import format_html
from .models import CasoExito, CasoExitoImagen


class CasoExitoImagenInline(admin.TabularInline):
    model = CasoExitoImagen
    extra = 1
    fields = ('orden', 'titulo', 'descripcion', 'imagen', 'imagen_preview')
    readonly_fields = ('imagen_preview',)

    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="max-height: 80px; max-width: 120px;" />', obj.imagen.url)
        return '-'
    imagen_preview.short_description = 'Vista previa'


class CasoExitoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'sector', 'fecha', 'imagen_preview')
    list_filter = ('sector', 'fecha')
    search_fields = ('cliente', 'problema', 'resultado')
    readonly_fields = ('imagen_preview',)
    fields = ('sector', 'cliente', 'problema', 'capacitacion', 'resultado', 'testimonio', 'imagen', 'imagen_preview', 'fecha')
    inlines = (CasoExitoImagenInline,)

    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="max-height: 120px; max-width: 200px;" />', obj.imagen.url)
        return '-'
    imagen_preview.short_description = 'Vista previa'


admin.site.register(CasoExito, CasoExitoAdmin)
admin.site.register(CasoExitoImagen)
