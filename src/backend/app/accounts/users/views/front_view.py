#from rest_framework.permissions import IsAuthenticated

from rest_framework.exceptions import NotAcceptable
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin


from ..serializers.front_serializer import (
    UserRegisterSerializer,
    UserVerifySerializer,
    UserLoginOtpSerializer,
    UserLoginEmailSerializer
 )
from accounts.users.mixins.front_mixin import (
    RegisterUserMixin,
    VerifyUserMixin,
    LoginOtpUserMixin,
    LoginEmailUserMixin
)



class UserRegisterApiView(RegisterUserMixin, GenericViewSet):

    serializer_class = UserRegisterSerializer


class UserVerifyApiView(VerifyUserMixin, GenericViewSet):

    serializer_class = UserVerifySerializer


    
class UserLoginOtpApiView(LoginOtpUserMixin, GenericViewSet):

    serializer_class = UserLoginOtpSerializer


class UserLoginEmailApiView(LoginEmailUserMixin, GenericViewSet):

    serializer_class = UserLoginEmailSerializer
