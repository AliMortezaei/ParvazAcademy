
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from accounts.users.models import User,UserType



class AdminUserSeialiser(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)
    class Meta:
        model = User
        #fields = '__all__'
        exclude = ('password', 'groups', 'user_permissions', 'user_type')


class AdminUserCreateSeialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('groups', 'user_permissions', 'last_login')

    def create_validate(self, attrs):
        user_type = attrs.get('user_type')
        match str(user_type):
            case 'teacher':
                user_type = UserType.objects.get(user_type="teacher")
            case 'student':
                user_type = UserType.objects.get(user_type="student")
            case _:
                msg = _('invalied user type')
                raise serializers.ValidationError(msg, code='invalied user type')

        attrs.update({'user_type': user_type})
        return attrs








                    
    