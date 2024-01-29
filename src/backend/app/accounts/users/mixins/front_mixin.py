from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth import authenticate



from .base import UserAuthBaseMixin
from utils.exception import InvaliedCodeVrify
from accounts.users.models import User


class RegisterUserMixin(UserAuthBaseMixin):
    
    @action(methods=['post'], detail=False)
    def register(self, request, *args, **kwargs):
        serializer = self.valiedate_serializer(request)
        self.perform_save(serializer)
        return Response(
            data= {"phone_number": serializer.data['phone_number']},
            status=status.HTTP_202_ACCEPTED,
        )

    def perform_save(self, serializer):
        code = self.otp.generate_otp_code()
        data = serializer.data
        phone_number = self.redis.add_to_redis(code=code, **data)
        message = self.otp_message_template.regster(message=code)
        #self.otp.send_sms(receptor=phone_number, message=message)
        return True



class VerifyUserMixin(UserAuthBaseMixin):

    @action(methods=['post'], detail=False)
    def verify(self, request, *args, **kwargs):
        serializer = self.valiedate_serializer(request)
        verify_data = self.redis.get_by_redis(serializer.data['phone_number'])
        #code = self.valied_code(serializer.data['code'], verify_data['code'])
        del verify_data['code']
        user = self.perform_create(
            phone_number=serializer.data['phone_number'], **verify_data
        )
        token = self.get_tokens_for_user(user)
        return Response(data=token, status=status.HTTP_201_CREATED)


    def valied_code(self, current_code, save_code):
        if (current_code and save_code) and ( current_code != save_code):
             raise InvaliedCodeVrify()
        return current_code


    def perform_create(self, *args, **kwargs):#phone_number, code, full_name, email, password):
        user, is_created = User.objects.get_or_create(**kwargs)
        return user
        

class LoginOtpUserMixin(UserAuthBaseMixin):

    @action(methods=['post'], detail=False)
    def login(self, request,*args, **kwargs):
        serializer = self.valiedate_serializer(request)
        self.perform_save(serializer)
        return Response(
            data= {"phone_number": serializer['phone_number']},
            status=status.HTTP_202_ACCEPTED,
        )
                  
    def valiedate_serializer(self, request):
        serializer = super().valiedate_serializer(request)
        return serializer.login_validate(serializer.data)

    def perform_save(self, data):
        code = self.otp.generate_otp_code()
        phone_number = self.redis.add_to_redis(code=code, **data)
        message = self.otp_message_template.login(message=code)
        #self.otp.send_sms(receptor=phone_number, message=message)
        return True



class LoginEmailUserMixin(UserAuthBaseMixin):
    
    @action(methods=['post'], detail=False)
    def email(self, request,*args, **kwargs):
        serializer = self.valiedate_serializer(request)
        user = authenticate(
            email=serializer.data['email'],
            password=serializer.data['password']
        )
        token = self.get_tokens_for_user(user)
        return Response(data=token, status=status.HTTP_201_CREATED)
    
        