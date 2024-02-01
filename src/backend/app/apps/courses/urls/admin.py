

from rest_framework.routers import DefaultRouter

from apps.courses.views.admin_view import AdminCategoryViewSet, AdminCourseViewSet


router = DefaultRouter()

router.register(r'categories', AdminCategoryViewSet, basename='Category')
router.register(r'courses', AdminCourseViewSet)


urlpatterns = router.urls
