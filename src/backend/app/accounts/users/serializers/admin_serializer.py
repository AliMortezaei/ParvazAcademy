
from attr import field
from rest_framework.serializers import ModelSerializer

from accounts.users.models import User



class AdminUserSeialiser(ModelSerializer):
    class Meta:
        model = User
        #fields = '__all__'
        exclude = ('password', 'groups', 'user_permissions')


class AdminUserCreateSeialiser(ModelSerializer):
    class Meta:
        model = User
        exclude = ('groups', 'user_permissions', 'user_type')