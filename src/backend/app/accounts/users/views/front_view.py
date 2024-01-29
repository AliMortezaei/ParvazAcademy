from rest_framework.exceptions import NotAcceptable
from rest_framework.viewsets import GenericViewSet


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



class UserLoginApiView(LoginOtpUserMixin, LoginEmailUserMixin, GenericViewSet):

    def get_serializer_class(self):
        match self.action:
            case 'login_otp':
                return UserLoginOtpSerializer
            case 'login_email':
                return UserLoginEmailSerializer
            case _:
                return super().get_serializer_class()
             
