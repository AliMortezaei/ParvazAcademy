
from django.urls import include
from rest_framework.urls import path
from rest_framework.routers import DefaultRouter

from accounts.teachers.views.front_view import TeacherCoursesViewSet, TeacherProfileApiView

router = DefaultRouter()

router.register('courses', TeacherCoursesViewSet, basename='teacher_courses')



urlpatterns = [
    path('', TeacherProfileApiView.as_view()),
    path('', include(router.urls)),
]
