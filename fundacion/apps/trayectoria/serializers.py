from rest_framework import serializers
from .models import CasoExito, CasoExitoImagen

class CasoExitoImagenSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = CasoExitoImagen
        fields = ('id', 'titulo', 'descripcion', 'orden', 'imagen_url')

    def get_imagen_url(self, obj):
        request = self.context.get('request')
        if obj.imagen:
            if request is not None:
                return request.build_absolute_uri(obj.imagen.url)
            return obj.imagen.url
        return None


class CasoExitoSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()
    galeria = CasoExitoImagenSerializer(many=True, read_only=True)

    class Meta:
        model = CasoExito
        fields = ('id', 'sector', 'cliente', 'problema', 'capacitacion', 'resultado', 'testimonio', 'imagen_url', 'galeria', 'fecha')

    def get_imagen_url(self, obj):
        request = self.context.get('request')
        if obj.imagen:
            if request is not None:
                return request.build_absolute_uri(obj.imagen.url)
            return obj.imagen.url
        return None