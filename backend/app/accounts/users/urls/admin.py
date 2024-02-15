from django.urls import path
from rest_framework.routers import DefaultRouter

from accounts.users.views.admin_view import AdminUserViewSet


router = DefaultRouter()

router.register(r'', AdminUserViewSet, basename='user')

urlpatterns = router.urls


