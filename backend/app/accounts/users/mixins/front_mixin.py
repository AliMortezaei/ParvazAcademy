from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from jalali_date import datetime2jalali

from ..documents.front import login_otp_doc
from .base import UserAuthBaseMixin
from utils.exception import InvaliedCodeVrify
from accounts.users.models import User, UserType
from accounts.users import tasks

class RegisterUserMixin(UserAuthBaseMixin):
    """
    The `register` function in this Python code is used to handle a POST request for user registration,
    where it validates the serializer, saves the data, adds the phone number to Redis, and sends an OTP
    code asynchronously.
    User Register user save informations and send otp code in phone number user
    length 5 code and pass user must redirect endpoint verify phone number 

    `Args`:
        phone_number(str) => must startwith 09 and 11 length 
        full_name(str) => full name user
        email(Email) => email user
        password(Password) => must 8 length 
 
    `Returns`:
        phone_number: pass redirect verify must phone_number and code receipt
    """
    @action(methods=['post'], detail=False)
    def register(self, request, *args, **kwargs):
        serializer = self.valiedate_serializer(request)
        self.perform_save(serializer)
        return Response(
            data= {"phone_number": serializer.data['phone_number']},
            status=status.HTTP_202_ACCEPTED,
        )

    def perform_save(self, serializer):
        data = serializer.data
        phone_number = self.redis.add_to_redis(code=self.code, **data)
        tasks.send_otp_code.delay(phone_number, self.code, 'register')
        return True



class VerifyUserMixin(UserAuthBaseMixin):
    """
    The above function is a view in a Django REST framework API that verifies a phone number and code,
    creates a user if they don't exist, and returns a token and user type.
    the code must recerive a phone number sms
    the action verify (endpoing) is userd for a `register` acction verify and `login` otp code verify 
    Args:
        phone_number(str) => 11 length 09124726243
        code(str) => 5 length 20102
    `Raises`:
        if phone_number given not register and login old raise status code 404 not found account
        
    `Returns`:
        if sucessfull phone number and code otp  `Created Account` and `Login`
    """
    @action(methods=['post'], detail=False)
    def verify(self, request, *args, **kwargs):
        serializer = self.valiedate_serializer(request)
        verify_data = self.redis.get_by_redis(serializer.data['phone_number'])
        code = self.valied_code(serializer.data['code'], verify_data['code'])
        del verify_data['code']
        user = self.perform_create(
            phone_number=serializer.data['phone_number'], **verify_data
        )
        token = self.get_tokens_for_user(user)
        return Response(data={'token': token, 'user_type': str(user.user_type)}, status=status.HTTP_201_CREATED)


    def valied_code(self, current_code, save_code):
        if (current_code and save_code) and ( current_code != save_code):
             raise InvaliedCodeVrify()
        return current_code


    def perform_create(self, *args, **kwargs):
        kwargs['user_type'] = UserType.objects.get(user_type='student')
        user, is_created = User.objects.get_or_create(**kwargs)
        return user
        
class LoginOtpUserMixin(UserAuthBaseMixin):
    """
    the function login with phone_number in method `Post` and save to redis database 
    end redirect to verify endpoint 
    must account `register old` and `send sms otp code` in phone number 
    
    Args:
        phone_number(str) = 09211342325
    Returns:
        `status code 202` , `phone_number`    
    """
    @action(methods=['post'], detail=False, url_path='otp')
    def login_otp(self, request,*args, **kwargs):
        serializer = self.valiedate_login(request)
        self.perform_save(serializer)
        return Response(
            data= {"phone_number": serializer['phone_number']},
            status=status.HTTP_202_ACCEPTED,
        )
                  
    def valiedate_login(self, request):
        serializer = super().valiedate_serializer(request)
        return serializer.login_validate(serializer.data)

    def perform_save(self, data):
        phone_number = self.redis.add_to_redis(code=self.code, **data)
        tasks.send_otp_code.delay(phone_number, self.code, 'login')
        return True



class LoginEmailUserMixin(UserAuthBaseMixin):
    """
    The above function is a login function that authenticates a user based on their email and password,
    updates their last login time, generates a token for the user, and returns the token and user type
    in the response.

    `raise`:
        if user not register 
    `Returns`:
        if sucessfull phone number and code otp  `Created Account` and `Login` `status code 201`
    """
    @action(methods=['post'], detail=False, url_path='email')
    def login_email(self, request,*args, **kwargs):
        serializer = self.valiedate_serializer(request)
        user = authenticate(
            email=serializer.data['email'],
            password=serializer.data['password']
        )
        user.last_login = str(datetime2jalali(timezone.now()))
        user.save()
        token = self.get_tokens_for_user(user)
        return Response(data={'token': token, 'user_type': str(user.user_type)}, status=status.HTTP_201_CREATED)
    
        
