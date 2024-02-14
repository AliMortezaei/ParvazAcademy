

from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from apps.courses.views.admin_view import\
(
    AdminCategoryViewSet,
    AdminCourseStudentsViewSet,
    AdminCourseViewSet,
    CourseSectionsViewSet
)

router = DefaultRouter()

router.register(r'categories', AdminCategoryViewSet, basename='admin-category')
router.register(r'courses', AdminCourseViewSet, basename='admin-course')


urlpatterns = [
    path(r'', include(router.urls)),
    path(r'courses/<str:course_slug>/students/',
         AdminCourseStudentsViewSet.as_view({'get': 'list'}),
         name='admin-student-list'
    ),
    path(r'courses/<str:course_slug>/students/<int:student_id>/',
        AdminCourseStudentsViewSet.as_view({'delete': 'destroy','post': 'join_student'}),
        name='admin-student'
    ),
    
    path(r'courses/<str:course_slug>/sections/',
         CourseSectionsViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='admin-section-list'
    ),
    path(r'courses/<str:course_slug>/sections/<str:section_slug>/',
        CourseSectionsViewSet.as_view({
                'delete': 'destroy', 'put': 'update', 'patch': 'update' 
        }),
        name='admin-section'
    ),

] 
