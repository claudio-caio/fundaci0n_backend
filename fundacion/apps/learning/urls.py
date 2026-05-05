from django.urls import path
from .views import course_content, enrolled_courses, lesson_detail, complete_lesson

urlpatterns = [
    path('enrolled-courses/', enrolled_courses, name='enrolled-courses'),
    path('course/<int:course_id>/', course_content, name='course-content'),
    path('course/<int:course_id>/lesson/<int:lesson_id>/', lesson_detail, name='lesson-detail'),
    path('course/<int:course_id>/lesson/<int:lesson_id>/complete/', complete_lesson, name='lesson-complete'),
]