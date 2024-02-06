
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotAcceptable
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from apps.courses.permissions import StudentCoursePermission
from apps.courses.models import Category, Course, Section
from apps.courses.serializers.front_serializer import CategoryListSerialiser, CategoryRetrieveSerialiser, CourseListSerialiser, CourseRetrieveSerialiser, SectionRetriveSerialiser
from apps.courses.mixins.front import JoinStudentCourseMixin

class CoursesViewSet(JoinStudentCourseMixin, ReadOnlyModelViewSet):

    permission_classes = [AllowAny]
    queryset = Course.objects.all()
    lookup_field = 'slug'
    lookup_url_kwarg = 'course_slug'

    def get_permissions(self):
        if self.action == "join_student_in_course":
            return [IsAuthenticated()]
        return [AllowAny()]
    
    def get_serializer_class(self):
        match self.action:
            case "list":
                return CourseListSerialiser
            case "retrieve":
                return CourseRetrieveSerialiser
            case _:
                return NotAcceptable()


class SectionsViewSet(ReadOnlyModelViewSet):

    permission_classes = [StudentCoursePermission]
    queryset = Section.objects.all().select_related('course')
    serializer_class = SectionRetriveSerialiser
    lookup_field = 'slug'
    lookup_url_kwarg = 'section_slug'

    def get_queryset(self):
        course_slug = self.kwargs.get("course_slug")
        course = get_object_or_404(Course, slug=course_slug)
        return self.queryset.filter(course=course)


class CategoryViewSet(ReadOnlyModelViewSet):

    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategoryListSerialiser
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


    def get_serializer_class(self):
        match self.action:
            case "list":
                return CategoryListSerialiser
            case "retrieve":
                return CategoryRetrieveSerialiser
            case _:
                return NotAcceptable