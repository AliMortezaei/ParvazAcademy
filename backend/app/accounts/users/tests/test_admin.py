
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.users.models import User, UserType



class UserAdminTestCase(APITestCase):
    """
    class for test endpoint user admin 
    --user must type user_type admin 
    """
    def setUp(self) -> None:
        self.user_url = reverse('user-list')
        self.admin_type = UserType.objects.create(user_type='admin')

        self.user_type = UserType.objects.create(user_type='student')
        # self.user = User.objects.create_user(user_type=self.user_type, full_name='user normal', email='user@normal',)
        self.admin = User(user_type=self.admin_type, full_name='admin', email='user@admin.com', phone_number='09123456789')
        self.admin.is_active = True
        self.admin.is_staff = True
        self.admin.is_superuser = True
        self.admin.save()
        refresh = RefreshToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        self.user = User.objects.first()
        self.validـdata = {
            "phone_number": "09011340218",
            "email": "mortezaei23s24@gmail.com",
            "full_name": "alirezsa mortezaei",
            "password": "Ali232s41s0",
            "user_type": self.user_type,
            "is_active": True,
            "is_staff": False,
            "is_superuser": False,
        }
        
    def test_list_user(self):
        response = self.client.get(self.user_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_user(self):
        resposne = self.client.post(self.user_url, self.validـdata)
    
        self.assertEqual(resposne.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 2)

    def test_update_user(self):
        self.update_data = {
            "full_name": 'rezaaaaaaaaa',
            }
        response = self.client.patch(f'{self.user_url}{self.user.id}/', self.update_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def test_delete_user(self):
        response = self.client.delete(f'{self.user_url}{self.user.id}/')
        
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    
        


    
        