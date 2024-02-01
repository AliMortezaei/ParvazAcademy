from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters


from apps.courses.mixins.admin import SectionMixin, StudentMixin
from apps.courses.models import Category, Course
from apps.courses.serializers.admin_serializer import \
(
    AdminCategorySerializer,
    AdminCourseSectionSerializer,
    AdminCourseSerializer
)
from apps.courses.serializers.admin_serializer import \
(
    AdminCourseStudentListSerialiser,

)

class AdminCategoryViewSet(ModelViewSet):

    permission_classes = [IsAdminUser]
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



class AdminCourseViewSet(SectionMixin, StudentMixin,ModelViewSet):

    serializer_class = AdminCourseSerializer
    #permission_classes = [IsAdminUser]
    queryset = Course.objects.all()
    # filter_backends = (filters.DjangoFilterBackend,)
    # filterset_class = CourseFilter

    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'



    def get_serializer_class(self):
        match self.action:
            case "student_list":
                return AdminCourseStudentListSerialiser
            case "sections":
                return AdminCourseSectionSerializer
            case "add_section":
                return AdminCourseSectionSerializer
            case "update_section":
                return AdminCourseSectionSerializer

        return super().get_serializer_class()
     
