from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

from utils.exception import UserNotFoundException



class EmailAuthBackend(BaseBackend):
    
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
    
        except UserModel.DoesNotExist:
            raise UserNotFoundException
        else:
            if user.check_password(password):
                return user
            else: 
                raise UserNotFoundException


    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

