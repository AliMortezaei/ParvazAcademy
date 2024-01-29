from django.urls import path
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainSlidingView
)

from ..views.front_view import \
(
    UserRegisterApiView,
    UserVerifyApiView,
    UserLoginOtpApiView,
    UserLoginEmailApiView
)

router = DefaultRouter()

router.register(r'', UserRegisterApiView, basename='register')
router.register(r'', UserVerifyApiView, basename='verify')
router.register(r'', UserLoginOtpApiView, basename='login')
router.register(r'login', UserLoginEmailApiView, basename='email_login')

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_obtain_pair'),

] + router.urls 

