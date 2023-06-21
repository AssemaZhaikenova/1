from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Request, LessonListeners


@receiver(post_save, sender=Request)
def create_lesson_listener(sender, instance, created, **kwargs):
    if created:
        LessonListeners.objects.create(lesson=instance.lesson, student=instance.student)
