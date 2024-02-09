from rest_framework.exceptions import NotAcceptable
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import (GenericViewSet, ModelViewSet, ReadOnlyModelViewSet)
from rest_framework.mixins import ListModelMixin, DestroyModelMixin

from accounts.teachers.permissions import IsTeacher, IsTeacherCourse
from accounts.teachers.serialisers.front_serialiser import TeacherCourseModificationSerialiser, TeacherCourseSerialiser
from apps.courses.mixins.front import JoinStudentCourseMixin, SectionDestroMixin
from apps.courses.models import Category, Course, Section
from apps.courses.permissions import StudentCoursePermission
from apps.courses.serializers.front_serializer import \
(
    CategoryListSerialiser,
    CategoryRetrieveSerialiser,
    CourseListSerialiser,
    CourseRetrieveSerialiser,
    CourseStudentSerialiser,
    SectionListSerialiser,
    SectionSerialiser
)



class CoursesViewSet(JoinStudentCourseMixin, ModelViewSet):

    permission_classes = [AllowAny]
    queryset = Course.objects.all()
    lookup_field = 'slug'
    lookup_url_kwarg = 'course_slug'

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

class SectionsViewSet(ModelViewSet):

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


class CourseStudentsViewSet(ListModelMixin, SectionDestroMixin, GenericViewSet):
    
    queryset = Course.objects.all().select_related('students')
    permission_classes = [IsTeacher, IsTeacherCourse]
    serializer_class = CourseStudentSerialiser
    
    def get_queryset(self):
        course = self.get_object()
        return course.students.all()

    def get_object(self):
        course_slug = self.kwargs.get("course_slug")
        return get_object_or_404(Course, slug=course_slug)

