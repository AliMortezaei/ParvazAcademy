from urllib import response
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.courses.models import Category, Course
from accounts.users.models import User, UserType



class AdminCourseTestCase(APITestCase):

    def setUp(self) -> None:
        self.admin_type = UserType.objects.create(user_type='admin')
        self.admin = User(user_type=self.admin_type, full_name='admin', email='user@admin2com', phone_number='09123456780')
        self.admin.is_active = True
        self.admin.is_staff = True
        self.admin.is_superuser = True
        self.admin.save()
        refresh = RefreshToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        self.category = Category.objects.create(title='learn programming language2')
        teacher_type = UserType.objects.create(user_type='teacher')
        self.teacher = User.objects.create(
            user_type=teacher_type, full_name='user teacher2',email='user@teacher2.com',
            is_active=True, is_staff=False, phone_number='09123456781', password='teacher2324'
        )
        self.valid_data = {
            "title": "learn R",
            "category": self.category.slug,
            "teacher": self.teacher.full_name,
        }
    def test_category_create(self):
        response = self.client.post(f'/api/v1/admin/categories/', {'title': 'programming R'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_course_create(self):
        response = self.client.post(f'/api/v1/admin/courses/', self.valid_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        



        
        