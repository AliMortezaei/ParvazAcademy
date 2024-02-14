from rest_framework.exceptions import NotAcceptable
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import (GenericViewSet, ModelViewSet, ReadOnlyModelViewSet)
from rest_framework.mixins import ListModelMixin, DestroyModelMixin
from drf_spectacular.utils import extend_schema
from django_filters import rest_framework as filters

from accounts.teachers.permissions import IsTeacher, IsTeacherCourse
from accounts.teachers.serialisers.front_serialiser import TeacherCourseModificationSerialiser, TeacherCourseSerialiser
from apps.courses.mixins.front import JoinStudentCourseMixin, StudentDestroMixin
from apps.courses.models import Category, Course, Section
from apps.courses.permissions import StudentCoursePermission
from apps.courses.filters import CourseFilter
from apps.courses.serializers.front_serializer import \
(
    CategoryListSerialiser,
    CourseListSerialiser,
    CourseRetrieveSerialiser,
    CourseStudentSerialiser,
    SectionListSerialiser,
    SectionSerialiser
)


@extend_schema(operation_id="courses", tags=["courses"])
class CoursesViewSet(JoinStudentCourseMixin, ModelViewSet):
    """
    handles various actions related to `courses`,including `creating`, `updating`,
    and `deleting` and `list` courses, as well as `joining students` to courses.
    
    """

    permission_classes = [AllowAny]
    queryset = Course.objects.all()
    lookup_field = 'slug'
    lookup_url_kwarg = 'course_slug'
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CourseFilter

    def get_object(self):
        match self.action:
            case "update" | "partial_update" | "destroy":
                course_slug = self.kwargs.get("course_slug")
                return get_object_or_404(Course, slug=course_slug)
        return super().get_object()

    def get_permissions(self):
        match self.action: 
            case "join_student_in_course":
                return [IsAuthenticated()]
            case "create":
                return [IsTeacher()]
            case "update" | "partial_update" | "destroy":
                return [IsTeacherCourse()]
        return super().get_permissions()
            
    
    def get_serializer_class(self):
        match self.action:
            case "list":
                return CourseListSerialiser
            case "retrieve":
                return CourseRetrieveSerialiser
            case "create":
                return TeacherCourseSerialiser
            case _:
                return TeacherCourseModificationSerialiser
            
    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)
@extend_schema(operation_id="course-sections", tags=["course sections"])
class SectionsViewSet(ModelViewSet):
    """
    The Sections class used add section to course and delete section that course , retrieve list
    sections.
    `None` the class used for `teacher` that must be the `owner of the course`
    takes course_slug and must course would have existed
    con `retrieve special section` whit section_slug 
    """

    permission_classes = [IsAuthenticated, StudentCoursePermission]
    queryset = Course.objects.all().select_related('sections')
    serializer_class = SectionSerialiser
    lookup_field = 'slug'
    lookup_url_kwarg = 'section_slug'
    

    def get_permissions(self):
        match self.action:
            case "list":
                return [AllowAny()]
            case "create" | "update" | "partial_update" | "destroy":
                return [IsTeacher(), IsTeacherCourse()]
        return super().get_permissions()
    
    def get_serializer_class(self):
        match self.action:
            case "list":
                return SectionListSerialiser
        return super().get_serializer_class()
    
    def get_queryset(self):
        course_slug = self.kwargs.get("course_slug")
        course = get_object_or_404(Course, slug=course_slug)
        return course.sections.all()
    
    def get_object(self):
        section_slug = self.kwargs.get("section_slug")
        return get_object_or_404(self.get_queryset(), slug=section_slug)

@extend_schema(operation_id="category", tags=["category"])
class CategoryViewSet(ListModelMixin, GenericViewSet):
    """
    a endpoint for category courses for use see all 
     
    """
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategoryListSerialiser


@extend_schema(operation_id="course-students", tags=["course students"])
class CourseStudentsViewSet(ListModelMixin, StudentDestroMixin, GenericViewSet):
    """
    a endpoint used for list students that course and remove student from course 
    takes course_slug and for remove student from course used student_id 
    
    """
    queryset = Course.objects.all().select_related('students')
    permission_classes = [IsTeacher, IsTeacherCourse]
    serializer_class = CourseStudentSerialiser
    
    def get_queryset(self):
        course = self.get_object()
        return course.students.all()

    def get_object(self):
        course_slug = self.kwargs.get("course_slug")
        return get_object_or_404(Course, slug=course_slug)

