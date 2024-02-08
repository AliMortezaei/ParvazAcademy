
from django.shortcuts import get_object_or_404
from rest_framework.generics import UpdateAPIView, GenericAPIView
from rest_framework.exceptions import NotAcceptable
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, CreateModelMixin

from rest_framework.viewsets import ModelViewSet
from accounts.teachers.permissions import IsTeacher, IsTeacherCourse
from accounts.students.mixins.front import RetrieveUserMixin, UpdateUserMixin
from accounts.teachers.models import TeacherProfile
from accounts.teachers.serialisers.front_serialiser import\
(
    ProfileTeacherSerialiser,
    ProfileModificationSerializer as TeacherModificationSerialiser,
    TeacherCourseModificationSerialiser,
    TeacherCourseSerialiser,

)
from apps.courses.models import Course
from apps.courses.serializers.front_serializer import CourseListSerialiser


class TeacherProfileApiView(RetrieveUserMixin, UpdateUserMixin, GenericAPIView):
    
    permission_classes = [IsTeacher]

    def get_queryset(self):
        user = self.get_object()
        return TeacherProfile.objects.filter(user_id=user.id).first()
    
    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        match self.request.method:
            case "GET":
                return ProfileTeacherSerialiser
            case "PUT":
                return TeacherModificationSerialiser
            case "PATCH":
                return TeacherModificationSerialiser
            case _:
                raise NotAcceptable()

    def update(self, instance, validated_data, request):
        validated_data['resume'] = request.data['resume']
        instance.resume = self.check(validated_data['resume'], instance.resume)
        return super().update(instance, validated_data, request)


class TeacherCoursesViewSet(ModelViewSet):
    
    permission_classes = [IsTeacher, IsTeacherCourse]
    
    #serializer_class = CourseListSerialiser
    lookup_field = 'slug'
    lookup_url_kwarg = 'course_slug'
    
    def get_permissions(self):
        if self.action == "list":
                return [IsTeacher()]
        return super().get_permissions()
    
    def get_serializer_class(self):
        match self.action:
            case "list":
                return CourseListSerialiser
            case "create":
                return TeacherCourseSerialiser
            case _:
                return TeacherCourseModificationSerialiser

    def get_queryset(self):
        user = self.get_object()
        return user.teacher_courses.all()
        
    def get_object(self):
        if self.action == "list":
            return self.request.user
        course_slug = self.kwargs.get("course_slug")
        return get_object_or_404(Course, slug=course_slug)
    
    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     #print(type(instance))
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     #print(serializer.data)
    #     return Response()