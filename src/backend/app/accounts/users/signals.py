from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from jalali_date import datetime2jalali

from core import settings
from .models import User
from accounts.students.models import StudentProfile
from accounts.teachers.models import TeacherProfile



@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        match str(instance.user_type):
            case "student":
                StudentProfile.objects.create(
                    user_id=instance.id, image=settings.DEFAULT_PROFILE
                )
            case "teacher":
                TeacherProfile.objects.create(
                    user_id=instance.id, image=settings.DEFAULT_PROFILE
                )
   


@receiver(post_save, sender=User)
def change_data_jalali(sender, instance, created, **kwargs):
    if created:
        user_date_join = instance.date_joined
        new_date = datetime2jalali(user_date_join)
        user = User.objects.get(email=instance.email)
        user.date_joined = str(new_date)
        user.save()
                
    














    