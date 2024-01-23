from django.contrib.auth.models import BaseUserManager

class MyUserManager(BaseUserManager):
    
    def create_user(self, phone_number, email, username, password):
        if not username:
            raise ValueError("Username is required")
        if not phone_number:
            raise ValueError("Phone number is required")
        if not email:
            raise ValueError("Email is required")
        if not password:
            raise ValueError("Password is required.")

        user = self.model(email=self.normalize_email(email),
                                        username=username,
                                        phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, username, password):
        user = self.create_user(phone_number=phone_number,
                                email=email,
                                username=username,
                                password=password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    @classmethod
    def get_active_user(self):
        return super().get_queryset().filter(is_active=True)

    












    





