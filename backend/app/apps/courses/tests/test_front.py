
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.courses.models import Category, Course
from accounts.users.models import User, UserType
from core import settings


class CourseTestCase(APITestCase):

    def setUp(self) -> None:
        # self.course_url = reverse('course-list')
        self.category = Category.objects.create(title='learn programming language')
        teacher_type = UserType.objects.create(user_type='teacher')
        self.teacher = User.objects.create(
            user_type=teacher_type, full_name='user teacher',email='user@teacher.com',
            is_active=True, is_staff=False, phone_number='09123456789', password='teacher2324'
        )
        self.refresh = RefreshToken.for_user(self.teacher)
        
        self.valid_date = {
            "title": "learn JavaScript",
            "category": self.category,
            "teacher": self.teacher,
            "description": "course learn javascript with html"
        }
        self.course = Course.objects.create(**self.valid_date)      

          
    def test_course_list(self):
        self.course
        response = self.client.get('/api/v1/courses/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        
    def test_category_list(self):
        response = self.client.get('/api/v1/categories/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_course_retrieve(self):
        course = self.course
        response = self.client.get(f'/api/v1/courses/{course.slug}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], course.title)


    def test_teacher_create_course(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.refresh.access_token)}')
        response = self.client.post(f'/api/v1/courses/', {
            'category': self.category.slug,
            'title': 'learn fastapi'
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_teacher_retrieve_course(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.refresh.access_token)}')
        response = self.client.get(f'/api/v1/courses/{self.course.slug}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_teacher_delete_course(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.refresh.access_token)}')
        response = self.client.delete(f'/api/v1/courses/{self.course.slug}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    




        

        