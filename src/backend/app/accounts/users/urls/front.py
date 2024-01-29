from django.urls import path
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainSlidingView,
    TokenBlacklistView
)

from ..views.front_view import \
(
    UserRegisterApiView,
    UserVerifyApiView,
    UserLoginApiView,
)

router = DefaultRouter()

router.register(r'', UserRegisterApiView, basename='register')
router.register(r'', UserVerifyApiView, basename='verify')
router.register(r'login', UserLoginApiView, basename='login')

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_obtain_pair'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),

] + router.urls 

