

from django.urls import include, path
from rest_framework import routers

from apps.courses.views.front_view import CategoryViewSet, CoursesViewSet, SectionsViewSet


router = routers.DefaultRouter()
router.register(r'^courses', CoursesViewSet) 
router.register(r'^categories', CategoryViewSet, basename='Category')
urlpatterns = [
    
    path('', include(router.urls)),
    
    path('courses/<slug:course_slug>/sections/',
        SectionsViewSet.as_view({'get': 'list'}),
        name='course-section-list'
    ),
    path('courses/<slug:course_slug>/sections/<slug:section_slug>/',
        SectionsViewSet.as_view({'get': 'retrieve'}),
        name='course-section-detail'
    )
    
] 

