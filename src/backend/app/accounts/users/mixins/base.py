
from rest_framework_simplejwt.tokens import RefreshToken

from utils.redis import RedisManager
from utils.otp import OtpManager, OtpMassageTemplate


class UserAuthBaseMixin:

    code = OtpManager().generate_otp_code()
    redis = RedisManager()

    def valiedate_serializer(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return serializer

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

