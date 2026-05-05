from rest_framework import serializers
from .models import Inscripcion
from apps.users.serializers import UserDetailSerializer
from apps.courses.serializers import CursoSerializer


class InscripcionSerializer(serializers.ModelSerializer):
    usuario = UserDetailSerializer(read_only=True)
    curso = CursoSerializer(read_only=True)
    curso_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Inscripcion
        fields = ['id', 'usuario', 'curso', 'curso_id', 'fecha_inscripcion', 'estado']
        read_only_fields = ['id', 'fecha_inscripcion', 'usuario']
