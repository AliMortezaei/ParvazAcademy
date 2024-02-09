
from django.shortcuts import get_object_or_404
from rest_framework.generics import UpdateAPIView, GenericAPIView, ListAPIView
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
)
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


class TeacherCoursesViewSet(ListAPIView):
    
    permission_classes = [IsTeacher]
    
    serializer_class = CourseListSerialiser
    lookup_field = 'slug'
    lookup_url_kwarg = 'course_slug'
    
    def get_queryset(self):
        user = self.get_object()
        return user.teacher_courses.all()
    
    def get_object(self):
        return self.request.user

