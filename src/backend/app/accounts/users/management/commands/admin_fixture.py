from django.core.management.base import BaseCommand, CommandError

from accounts.users.models import User, UserType




class Command(BaseCommand):

    help = "Generate User fixture in db"
    
    def handle(self, *args, **options):
        try:
            admin_type = UserType.objects.get(user_type='admin')
            user = User(user_type=admin_type)
        except Exception as exp:
            raise CommandError(exp)
        user.email = "admin@email.com"
        user.full_name = "admin"
        user.phone_number = "09123456789"
        user.password = "admin2324"
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {user.email}, {user.password}')
        )
        