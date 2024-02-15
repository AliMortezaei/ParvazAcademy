
from django.urls import include
from rest_framework.urls import path
from rest_framework.routers import DefaultRouter

from accounts.teachers.views.front_view import TeacherCoursesViewSet, TeacherProfileApiView



urlpatterns = [
    path('', TeacherProfileApiView.as_view()),
    path('courses', TeacherCoursesViewSet.as_view())
]
