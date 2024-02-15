
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import UpdateModelMixin, ListModelMixin
from rest_framework.generics import UpdateAPIView, GenericAPIView
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from rest_framework.exceptions import NotAcceptable
from drf_spectacular.utils import extend_schema

from accounts.students.models import StudentProfile
from accounts.students.serializers.front_serialiser import ChangePasswordSerializer, ProfileModificationSerializer, ProfileStudentSerialiser
from accounts.students.mixins.front import RetrieveUserMixin, UpdateUserMixin
from apps.courses.serializers.front_serializer import CourseListSerialiser

@extend_schema(operation_id="user-profile", tags=["user profile"])
class UserProfileApiView(RetrieveUserMixin, UpdateUserMixin, GenericAPIView):

    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.get_object()
        return StudentProfile.objects.filter(user_id=user.id).first()

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        match self.request.method:
            case "GET":
                return ProfileStudentSerialiser
            case "PUT":
                return ProfileModificationSerializer
            case "PATCH":
                return ProfileModificationSerializer
            case _:
                raise NotAcceptable()

@extend_schema(operation_id="user-profile-change-password", tags=["user profile"])
class ProfileChangePasswordApiView(UpdateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    http_method_names = ['put']
    
    def get_object(self):
        return self.request.user
    
@extend_schema(operation_id="user-profile-courses", tags=["user profile"])
class UserCoursesViewSet(ListModelMixin, GenericViewSet):
    
    permission_classes = [IsAuthenticated]

    serializer_class = CourseListSerialiser
    
    def get_object(self):
        return self.request.user

    def get_queryset(self):
        user = self.get_object()
        return user.courses.all()