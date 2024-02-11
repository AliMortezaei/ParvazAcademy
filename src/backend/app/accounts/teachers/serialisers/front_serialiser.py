
from urllib import request
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from accounts.teachers.models import TeacherProfile
from accounts.students.serializers.front_serialiser import UserSerialiser
from apps.courses.models import Category, Course


class ProfileTeacherSerialiser(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = TeacherProfile
        fields = '__all__'

    def get_user(self, obj):
        return UserSerialiser(obj.user).data

class ProfileModificationSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name', required=False)
    
    class Meta:
        model = TeacherProfile
        fields = ['full_name', 'city', 'gender', 'birthday', 'image', 'description', 'resume']

class TeacherCourseSerialiser(serializers.ModelSerializer):
    category = serializers.CharField()
    teacher = serializers.CharField(read_only=True)    
    #title = serializers.CharField(required=False)
    class Meta:
        model = Course
        #fields = '__all__'
        exclude = ('students', 'numbers')

    def validate_category(self, value):
        return get_object_or_404(Category, slug=value)

 
class TeacherCourseModificationSerialiser(serializers.ModelSerializer):
    title = serializers.CharField(required=False)
    category = serializers.CharField(required=False)
    teacher = serializers.CharField(source='teacher.full_name', read_only=True)
    date_start = serializers.DateTimeField(format='%y/%m/%d')
    class Meta:
        model = Course
        exclude = ('students',)
        

    def validate_category(self, value):
        return get_object_or_404(Category, slug=value)