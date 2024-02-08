from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django_filters import rest_framework as filters
from rest_framework.mixins import ListModelMixin, DestroyModelMixin
from drf_spectacular.utils import extend_schema

from apps.courses.mixins.admin import StudentsJoinMixin
from apps.courses.models import Category, Course
from apps.courses.serializers.admin_serializer import \
(
    AdminCategorySerializer,
    AdminCourseModificationSerializer,
    AdminCourseSectionListSerializer,
    AdminSectionSeialiser,
    AdminCourseSerializer,
    AdminCourseStudentListSerialiser,
    

)

@extend_schema(operation_id="categories", tags=["admin category"])
class AdminCategoryViewSet(ModelViewSet):

    #permission_classes = [IsAdminUser]
    serializer_class = AdminCategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


# class CourseFilter(filters.FilterSet):
#     category__title = filters.CharFilter(lookup_expr='icontains',field_name='category')
#     #students__name = filters.CharFilter(lookup_expr='icontains')
    
#     class Meta:
#         model = Course
#         fields = ['is_start', 'students']


@extend_schema(operation_id="course", tags=["admin course"])
class AdminCourseViewSet(ModelViewSet):

    serializer_class = AdminCourseSerializer
   # permission_classes = [IsAdminUser]
    queryset = Course.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    # filterset_class = CourseFilter

    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    def get_serializer_class(self):
        if self.action == "partial_update" or self.action == "update":
            return AdminCourseModificationSerializer
        return super().get_serializer_class()
            

@extend_schema(operation_id="section", tags=["admin section"])
class CourseSectionsViewSet(ModelViewSet):

    #permission_classes = [IsAdminUser]
    serializer_class = AdminCourseSectionListSerializer

    def get_queryset(self):
        course_slug = self.kwargs.get("course_slug")
        course = get_object_or_404(Course, slug=course_slug)
        return course.sections.all()
        
    
    def get_object(self):
        section_slug = self.kwargs.get("section_slug")
        return get_object_or_404(self.get_queryset(), slug=section_slug)
        
        

    def get_serializer_class(self):
        match self.action:
            case "list":
                return AdminCourseSectionListSerializer
            case "create":
                return AdminSectionSeialiser
            case "retrieve":
                return AdminSectionSeialiser
            
            
@extend_schema(operation_id="student", tags=["admin student"])
class CourseStudentsViewSet(ListModelMixin, StudentsJoinMixin, DestroyModelMixin, GenericViewSet):

    #permission_classes = [IsAdminUser]
    queryset = Course.objects.all().select_related('students')

    def get_queryset(self):
        course = self.get_object()
        return course.students.all()

    def get_object(self):
        course_slug = self.kwargs.get("course_slug")
        return get_object_or_404(Course, slug=course_slug)

    def get_serializer_class(self):
        if self.action == "list":
            return AdminCourseStudentListSerialiser

    