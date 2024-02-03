from rest_framework.urls import path
from rest_framework.routers import  DefaultRouter

from accounts.students.views.front_view import UserProfileApiView, ProfileChangePasswordApiView

# router = DefaultRouter
# router.register(r'courses', ProfileCourseViewSet)



urlpatterns = [
    path('', UserProfileApiView.as_view()),
    path('change_password/', ProfileChangePasswordApiView.as_view())
]