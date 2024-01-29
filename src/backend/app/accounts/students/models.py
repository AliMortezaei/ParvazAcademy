from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.users.models import User


class StudentProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='student_profile'
    )
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

    # TODO: image save s3 ...
    #image = models.ImageField(_("profile image"), blank=True, null=True)



    

