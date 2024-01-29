from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.users.models import User


class TeacherProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='teacher_profile'
    )
    description = models.TextField(_("description introduction"), blank=True)
    gender = models.BooleanField(
        _("Gender"),
        blank=True,
        choices=[
            (False, "Female"),
            (True, "male")
        ]
    )
    city = models.CharField(_("city") ,max_length=65, blank=True)
    birthday = models.DateField(_("bithday"), blank=True)
    
    # TODO: image profile teacher
    #image = models.ImageField(_("profile image"))
    
    # TODO: cv_file models
    #cv_file = models.FieldFile()