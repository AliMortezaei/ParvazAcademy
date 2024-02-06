

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.courses.views.admin_view import\
(
    AdminCategoryViewSet,
    AdminCourseViewSet,
    CourseStudentsViewSet,
    CourseSectionsViewSet
)

router = DefaultRouter()

router.register(r'categories', AdminCategoryViewSet, basename='Category')
router.register(r'courses', AdminCourseViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('courses/<slug:course_slug>/students/',
         CourseStudentsViewSet.as_view({'get': 'list'}),
         name='student-list'
    ),
    path('courses/<slug:course_slug>/students/<int:student_id>/',
        CourseStudentsViewSet.as_view({'delete': 'destroy','post': 'join_student'}),
        name='students'
    ),
    
    path('courses/<slug:course_slug>/sections/',
         CourseSectionsViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='section-list'
    ),
    path('courses/<slug:course_slug>/sections/<slug:section_slug>/',
        CourseSectionsViewSet.as_view({
                'get': 'retrieve', 'delete': 'destroy', 'put': 'update', 'patch': 'update' 
        }),
        name='section-retrieve'
    ),

] 
