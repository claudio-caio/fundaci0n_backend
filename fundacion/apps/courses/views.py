from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Curso
from .serializers import CursoSerializer


class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.filter(activo=True)
    serializer_class = CursoSerializer
    permission_classes = [AllowAny]  # 🔓 Permitir acceso anónimo a la lista de cursos