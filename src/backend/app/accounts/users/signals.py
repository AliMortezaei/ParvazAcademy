from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User
from accounts.students.models import StudentProfile
from accounts.teachers.models import TeacherProfile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        match str(instance.user_type):
            case "student":
                StudentProfile.objects.create(user_id=instance.id)
            case "teacher":
                TeacherProfile.objects.create(user_id=instance.id)
            case _:
                raise ValueError("user type not found")

