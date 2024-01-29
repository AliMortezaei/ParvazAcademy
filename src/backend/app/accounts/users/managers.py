from typing import Any

from django.contrib.auth.models import BaseUserManager
from django.db.models import QuerySet

class CustomQuerySet(QuerySet):

    def get_or_create(self, **kwargs: Any) -> tuple[Any, bool]:
        try:
            user = self.model.objects.get(phone_number=kwargs['phone_number'])
            return user, False
        except self.model.DoesNotExist:
            return self.model.objects.create_user(**kwargs), True

class UserManager(BaseUserManager):


    def get_or_create(self, **kwargs: Any) -> tuple[Any, bool]:
        return CustomQuerySet(model=self.model).get_or_create(**kwargs)

    def create_user(
        self,
        phone_number: str = None,
        email: str = None,
        full_name: str = None,
        password: str = None,
        user_type: str = "student"
    ):

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            phone_number=phone_number,
            user_type=user_type
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, full_name, password, user_type='admin'):
        user = self.create_user(
            phone_number=phone_number,
            email=email,
            full_name=full_name,
            password=password,
            user_type=user_type
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    @classmethod
    def get_active_user(self):
        return super().get_queryset().filter(is_active=True)







    





    





