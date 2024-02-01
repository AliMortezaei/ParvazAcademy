 
from xml.sax.handler import feature_external_ges
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters


from apps.courses.mixins.base import AddStudentMixin
from apps.courses.models import Category, Course, CourseStudent
from apps.courses.serializers.admin_serializer import \
(
AdminCategorySerializer,
AdminCourseSerializer

)
from apps.courses.serializers.admin_serializer import CourseStudentListSerialiser


class AdminCategoryViewSet(ModelViewSet):

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



class AdminCourseViewSet(AddStudentMixin,ModelViewSet):

    serializer_class = AdminCourseSerializer

    queryset = Course.objects.all()
    # filter_backends = (filters.DjangoFilterBackend,)
    # filterset_class = CourseFilter

    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


    def get_serializer_class(self):
        match self.action:
            case 'student_list':
                return CourseStudentListSerialiser
            case _:
                return super().get_serializer_class()
     
