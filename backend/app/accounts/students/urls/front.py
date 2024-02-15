from rest_framework.urls import path
from rest_framework.routers import  DefaultRouter

from accounts.students.views.front_view import \
(
    UserProfileApiView,
    ProfileChangePasswordApiView,
    UserCoursesViewSet

)

# router = DefaultRouter
# router.register(r'courses', ProfileCourseViewSet)



urlpatterns = [
    path('', UserProfileApiView.as_view()),
    path('courses/', UserCoursesViewSet.as_view({'get': 'list'}) ),
    path('change_password/', ProfileChangePasswordApiView.as_view())
]