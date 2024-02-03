from rest_framework.urls import path

from accounts.students.views.front_view import UserProfileApiView



urlpatterns = [
    path('', UserProfileApiView.as_view())
]