


from django.urls import path
from rest_framework.routers import DefaultRouter

from accounts.students.views.admin_view import AdminProfileApiView


router = DefaultRouter()

router.register('profile', AdminProfileApiView, basename='profile' )

urlpatterns = [] + router.urls
