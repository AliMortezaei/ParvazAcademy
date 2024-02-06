
from rest_framework import serializers
from accounts.teachers.models import TeacherProfile

from apps.courses.models import Course, Section, Category



class CourseListSerialiser(serializers.ModelSerializer):
    teacher = serializers.CharField(source='teacher.full_name')    
    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'is_start', 'date_start', 'numbers', 'image', 'teacher']


class ProfileTeacherCourseSerialiser(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name')
    class Meta:
        model = TeacherProfile
        fields = ['full_name', 'image', 'description']
class CourseRetrieveSerialiser(serializers.ModelSerializer):
    teacher = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'is_start', 'date_start', 'numbers', 'image', 'teacher']

    def get_teacher(self, obj):
        user = obj.teacher
        teacher_profile = user.teacher_profile
        return ProfileTeacherCourseSerialiser(teacher_profile).data


class SectionRetriveSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'
        #exclude = ("course",)

class CategoryListSerialiser(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ("description",)

class CategoryRetrieveSerialiser(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = '__all__'

    def get_courses(self, obj):
        courses = obj.courses.all()
        return CourseListSerialiser(courses, many=True).data