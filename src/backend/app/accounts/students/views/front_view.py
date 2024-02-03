
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import UpdateModelMixin
from rest_framework.generics import UpdateAPIView, GenericAPIView
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from rest_framework.exceptions import NotAcceptable


from accounts.students.models import StudentProfile
from accounts.students.serializers.front_serialiser import ChangePasswordSerializer, ProfileModificationSerializer, ProfileStudentSerialiser
from accounts.students.mixins.front import RetrieveUserMixin, UpdateUserMixin

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


class ProfileChangePasswordApiView(UpdateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    http_method_names = ['put']
    
    def get_object(self):
        return self.request.user
    

