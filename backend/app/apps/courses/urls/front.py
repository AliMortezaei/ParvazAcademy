

from django.urls import include, path
from rest_framework import routers

from apps.courses.views.front_view import CategoryViewSet, CoursesViewSet, SectionsViewSet, CourseStudentsViewSet


router = routers.DefaultRouter()
router.register(r'^courses', CoursesViewSet, basename='course') 
router.register(r'^categories', CategoryViewSet, basename='category')
urlpatterns = [
    
    path('', include(router.urls)),
    
    path('courses/<str:course_slug>/sections/',
        SectionsViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='course-section-list-create'
    ),
    path('courses/<str:course_slug>/sections/<str:section_slug>/',
        SectionsViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'update', 'delete': 'destroy'}),
        name='course-section-slug'
    ),
    path('courses/<str:course_slug>/students/',
        CourseStudentsViewSet.as_view({'get': 'list'}),
        name='course-student-list'
    ),
    path('courses/<str:course_slug>/students/<int:student_id>/',
        CourseStudentsViewSet.as_view({'delete': 'destroy'}),
        name='course-student-delete'
    ),
] 

