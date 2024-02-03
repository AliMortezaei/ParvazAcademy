
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

    def validate(self, attrs):
        return super().validate(attrs)
  
    