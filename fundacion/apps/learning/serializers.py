from rest_framework import serializers
from .models import Module, Lesson, LessonProgress


class LessonSerializer(serializers.ModelSerializer):
    completed = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'video_url', 'content', 'order', 'completed']

    def get_completed(self, obj):
        request = self.context.get('request')
        if not request or not request.user or request.user.is_anonymous:
            return False
        return LessonProgress.objects.filter(user=request.user, lesson=obj, completed=True).exists()


class ModuleSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = ['id', 'title', 'order', 'lessons']

    def get_lessons(self, obj):
        lessons = obj.lessons.all().order_by('order')
        return LessonSerializer(lessons, many=True, context=self.context).data