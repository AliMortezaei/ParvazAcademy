
from rest_framework import serializers

from accounts.students.models import StudentProfile 



class AdminProfileSerialiser(serializers.ModelSerializer):
    user = serializers.CharField(source='user.full_name')
    
    
    class Meta:
        model = StudentProfile
        fields = '__all__'
        