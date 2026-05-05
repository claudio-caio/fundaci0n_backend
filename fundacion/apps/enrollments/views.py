from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Inscripcion
from apps.courses.models import Curso
from .serializers import InscripcionSerializer


class InscripcionViewSet(viewsets.ModelViewSet):
    queryset = Inscripcion.objects.all()
    serializer_class = InscripcionSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def inscribirse(self, request):
        """
        Endpoint para que un usuario se inscriba en un curso.
        Requiere autenticación JWT.
        """
        curso_id = request.data.get('curso_id')
        
        if not curso_id:
            return Response(
                {'error': 'curso_id es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            curso = Curso.objects.get(id=curso_id)
        except Curso.DoesNotExist:
            return Response(
                {'error': 'Curso no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Verificar si ya está inscrito
        inscripcion_existente = Inscripcion.objects.filter(
            usuario=request.user,
            curso=curso
        ).first()
        
        if inscripcion_existente:
            return Response(
                {'error': 'Ya estás inscrito en este curso'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Crear inscripción
        inscripcion = Inscripcion.objects.create(
            usuario=request.user,
            curso=curso
        )
        
        serializer = self.get_serializer(inscripcion)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def mis_cursos(self, request):
        """
        Obtener los cursos en los que el usuario está inscrito.
        Requiere autenticación JWT.
        """
        inscripciones = Inscripcion.objects.filter(usuario=request.user)
        serializer = self.get_serializer(inscripciones, many=True)
        return Response(serializer.data)
