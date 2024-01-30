from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import UserManager


    

class UserType(models.Model):
    class UserTypeChoice(models.TextChoices):
        admin = "admin"
        student = "student"
        teacher = "teacher"
    
    user_type = models.CharField(
        max_length=8,
        choices=UserTypeChoice.choices,
        help_text=_("Selection User Type"),
        primary_key=True
    ) 
    introduction = models.TextField(_("description user type"), null=True, blank=True)

    def __str__ (self):
        return self.user_type

    class Meta:
        verbose_name = _("user_type")
        verbose_name_plural = _("users_type")


class User(AbstractBaseUser, PermissionsMixin):

    objects = UserManager()
    
    user_type = models.ForeignKey(
        UserType, on_delete=models.CASCADE,
        db_column="type",
        related_name='users'
    )

    full_name = models.CharField(_("full name"), max_length=150, blank=True, null=True)
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(
        _("phone number"),
        validators=[RegexValidator('^09[0-9]{9}$')],
        error_messages={
            "invalid": _("The phone number is invalid")
        }, 
        max_length=11,
        unique=True)
    
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)

    

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["email", "full_name"]


    def __str__ (self):
        return self.email


    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")



 
            
