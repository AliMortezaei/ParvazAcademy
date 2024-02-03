from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.users.models import User
from utils.media import ImageMediaStorage


class TeacherProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='teacher_profile'
    )
    description = models.TextField(_("description introduction"), blank=True, null=True)
    gender = models.BooleanField(
        _("Gender"),
        null=True,
        blank=True,
        choices=[
            (False, "Female"),
            (True, "male")
        ]
    )
    city = models.CharField(_("city") ,max_length=65, blank=True, null=True)
    birthday = models.DateField(_("bithday"), blank=True, null=True)
    
    image = models.FileField(storage=ImageMediaStorage(), blank=True, null=True)
    
