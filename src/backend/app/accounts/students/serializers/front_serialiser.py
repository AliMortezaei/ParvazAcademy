
from rest_framework import serializers

from accounts.students.models import StudentProfile
from accounts.users.models import User


class UserSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'phone_number', 'user_type']
        read_only_fields = ['id' ,'phone_number', 'user_type', 'email']

class ProfileStudentSerialiser(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = StudentProfile
        fields = '__all__'

    def get_user(self, obj):
        return UserSerialiser(obj.user).data



class ProfileModificationSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name', required=False)
    
    class Meta:
        model = StudentProfile
        fields = ['full_name', 'city', 'gender', 'birthday', 'image']


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['old_password', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context.get('request').user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance