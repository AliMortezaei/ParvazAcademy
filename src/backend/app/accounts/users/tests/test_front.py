
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from jalali_date import datetime2jalali

from accounts.users.models import User, UserType
from accounts.students.models import StudentProfile

from utils.redis import RedisManager



class AuthUserRegisterTestCase(APITestCase):
    """
    Test api auth user => register with RegisterUserMixin
    Test api verify user => with VerifyUserMixin
    Test api login otp => with LoginEmailUserMixin  
    Test api login email => with LoginOtpUserMixin
    
    Args:
        phone_number, email, full_name, password
    """
    def setUp(self) -> None:
        self.login_email_url = reverse('login-login-email')
        self.login_otp_url = reverse('login-login-otp')
        self.register_url = reverse("register-register")
        self.verify_url = reverse("verify-verify")
        
        self.user_type = UserType.objects.create(user_type='student')
        self.redis = RedisManager()
        self.validـdata = {
            "phone_number": "09012340218",
            "email": "mortezaei2324@gmail.com",
            "full_name": "alireza mortezaei",
            "password": "Ali232410"
        }

    def test_register_view(self):
        response = self.client.post(self.register_url, self.validـdata)
        data = self.redis.get_by_redis(response.data['phone_number'])
        
        self.assertEqual(data['full_name'], self.validـdata['full_name'])
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        return {
            "phone_number": response.data['phone_number'],
            "code": data['code']
        }
        
    def test_verify_view(self):
        data = self.test_register_view()
        response = self.client.post(self.verify_url, data)

        self.assertTrue(response.data['token']['access'])
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(StudentProfile.objects.all().count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_login_email_view(self):
        user = User.objects.create_user(**self.validـdata, user_type=self.user_type)
        response = self.client.post(
            self.login_email_url,
            data={'email': 'mortezaei2324@gmail.com', 'password': 'Ali232410'}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['token']['access'])

    def test_login_otp_view(self):
        user = User.objects.create_user(**self.validـdata, user_type=self.user_type)
        response = self.client.post(self.login_otp_url,
            data={'phone_number': '09012340218'}
        )
        data = self.redis.get_by_redis(response.data['phone_number'])

        self.assertEqual(data['full_name'], self.validـdata['full_name'])
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)


    