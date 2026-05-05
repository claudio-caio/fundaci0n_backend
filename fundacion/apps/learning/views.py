from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.enrollments.models import Inscripcion
from apps.courses.models import Curso
from .models import Module, LessonProgress, Lesson
from .serializers import ModuleSerializer
from django.db.models import Count, Q


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def enrolled_courses(request):
    """
    Obtiene los cursos en los que está inscrito el usuario.
    """
    inscripciones = Inscripcion.objects.filter(
        usuario=request.user,
        estado='activo'  # Cambiado de activo=True a estado='activo'
    ).select_related('curso')

    courses_data = []
    for inscripcion in inscripciones:
        course = inscripcion.curso
        modules = Module.objects.filter(course=course).order_by('order')
        
        # Calcular progreso
        total_lessons = Lesson.objects.filter(
            module__course=course
        ).count()
        
        completed_lessons = LessonProgress.objects.filter(
            user=request.user,
            lesson__module__course=course,
            completed=True
        ).count()
        
        progress_percentage = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0

        courses_data.append({
            "id": course.id,
            "nombre": course.nombre,
            "descripcion": course.descripcion,
            "precio": str(course.precio),
            "activo": course.activo,
            "total_lessons": total_lessons,
            "completed_lessons": completed_lessons,
            "progress_percentage": round(progress_percentage, 2),
            "enrolled_date": inscripcion.fecha_inscripcion.isoformat() if inscripcion.fecha_inscripcion else None,  # Cambiado de fecha a fecha_inscripcion
        })

    return Response({
        "enrolled_courses": courses_data,
        "count": len(courses_data)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def course_content(request, course_id):
    try:
        course = Curso.objects.get(id=course_id)
    except Curso.DoesNotExist:
        return Response(
            {"error": "Curso no encontrado"},
            status=status.HTTP_404_NOT_FOUND
        )

    # 🔒 Validación de inscripción
    if not Inscripcion.objects.filter(usuario=request.user, curso=course).exists():
        return Response(
            {"error": "No autorizado"},
            status=status.HTTP_403_FORBIDDEN
        )

    modules = Module.objects.filter(course=course).order_by('order')

    serializer = ModuleSerializer(modules, many=True, context={'request': request})

    total_lessons = Lesson.objects.filter(module__course=course).count()
    completed_lessons = LessonProgress.objects.filter(
        user=request.user,
        lesson__module__course=course,
        completed=True
    ).count()
    progress_percentage = round((completed_lessons / total_lessons * 100), 2) if total_lessons > 0 else 0

    return Response({
        "course": course.nombre,
        "description": course.descripcion,
        "modules": serializer.data,
        "total_lessons": total_lessons,
        "completed_lessons": completed_lessons,
        "progress_percentage": progress_percentage,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_lesson(request, course_id, lesson_id):
    try:
        lesson = Lesson.objects.get(id=lesson_id)
    except Lesson.DoesNotExist:
        return Response(
            {"error": "Lección no encontrada"},
            status=status.HTTP_404_NOT_FOUND
        )

    if lesson.module.course.id != course_id:
        return Response(
            {"error": "La lección no pertenece a este curso"},
            status=status.HTTP_404_NOT_FOUND
        )

    if not Inscripcion.objects.filter(usuario=request.user, curso_id=course_id).exists():
        return Response(
            {"error": "No autorizado"},
            status=status.HTTP_403_FORBIDDEN
        )

    progress, created = LessonProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson,
        defaults={'completed': True}
    )

    if not progress.completed:
        progress.completed = True
        progress.save()

    total_lessons = Lesson.objects.filter(module__course=lesson.module.course).count()
    completed_lessons = LessonProgress.objects.filter(
        user=request.user,
        lesson__module__course=lesson.module.course,
        completed=True
    ).count()
    progress_percentage = round((completed_lessons / total_lessons * 100), 2) if total_lessons > 0 else 0

    return Response({
        "completed": progress.completed,
        "total_lessons": total_lessons,
        "completed_lessons": completed_lessons,
        "progress_percentage": progress_percentage,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lesson_detail(request, course_id, lesson_id):
    """
    Obtiene el detalle de una lección específica.
    """
    try:
        lesson = Lesson.objects.get(id=lesson_id)
    except Lesson.DoesNotExist:
        return Response(
            {"error": "Lección no encontrada"},
            status=status.HTTP_404_NOT_FOUND
        )

    # Verificar que la lección pertenece al curso
    if lesson.module.course.id != course_id:
        return Response(
            {"error": "La lección no pertenece a este curso"},
            status=status.HTTP_404_NOT_FOUND
        )

    # 🔒 Validación de inscripción
    if not Inscripcion.objects.filter(usuario=request.user, curso_id=course_id).exists():
        return Response(
            {"error": "No autorizado"},
            status=status.HTTP_403_FORBIDDEN
        )

    # Obtener progreso de la lección
    progress, created = LessonProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson,
        defaults={'completed': False}
    )

    # Navegación previa/siguiente dentro del curso
    ordered_lessons = list(
        Lesson.objects.filter(module__course=lesson.module.course)
        .order_by('module__order', 'order')
        .values('id', 'title')
    )

    current_index = next(
        (index for index, item in enumerate(ordered_lessons) if item['id'] == lesson.id),
        None
    )

    prev_lesson = None
    next_lesson = None
    if current_index is not None:
        if current_index > 0:
            prev_lesson = ordered_lessons[current_index - 1]
        if current_index < len(ordered_lessons) - 1:
            next_lesson = ordered_lessons[current_index + 1]

    lesson_data = {
        "id": lesson.id,
        "title": lesson.title,
        "video_url": lesson.video_url,
        "content": lesson.content,
        "order": lesson.order,
        "completed": progress.completed,
        "module_title": lesson.module.title,
        "course_title": lesson.module.course.nombre,
        "prev_lesson": prev_lesson,
        "next_lesson": next_lesson,
    }

    return Response(lesson_data)