from django.db import models

class Module(models.Model):
    course = models.ForeignKey('courses.Curso', on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    order = models.IntegerField()

class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    video_url = models.URLField(blank=True, null=True)
    content = models.TextField(blank=True)  # texto tipo blog
    order = models.IntegerField()

class LessonProgress(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)