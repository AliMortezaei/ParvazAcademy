
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from jalali_date import datetime2jalali, date2jalali

from accounts.teachers.models import TeacherProfile
from accounts.users.models import User
from accounts.students.serializers.admin_serializer import AdminProfileSerialiser

from apps.courses.models import Course, Section, Category
from apps.courses.documents.front import course_list_doc


@course_list_doc()
class CourseListSerialiser(serializers.ModelSerializer):
    teacher = serializers.CharField(source='teacher.full_name')
    category = serializers.CharField(source='category.title')    
    class Meta:
        model = Course
        exclude = ('students', "description", "date_end")


class ProfileTeacherCourseSerialiser(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name')
    email = serializers.CharField(source='user.email')
    class Meta:
        model = TeacherProfile
        fields = ['user_id','full_name', 'image', 'description', 'email', 'resume']
class CourseRetrieveSerialiser(serializers.ModelSerializer):
    teacher = serializers.SerializerMethodField()
    category = serializers.CharField(source='category.title')    
    class Meta:
        model = Course
       # fields = ['id', 'title', 'slug', 'is_start', 'date_start', 'numbers', 'image', 'teacher']
        exclude = ('students',)
    def get_teacher(self, obj):
        user = obj.teacher
        teacher_profile = user.teacher_profile
        return ProfileTeacherCourseSerialiser(teacher_profile).data

class SectionListSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Section
        exclude = ("course", "link", "description", "date_start")

class SectionSerialiser(serializers.ModelSerializer):
    title = serializers.CharField(required=False)

    class Meta:
        model = Section
        exclude = ("course",)
        
    def validate(self, attrs):
        course_slug = self.context.get('view').kwargs.get("course_slug")
        course = get_object_or_404(Course, slug=course_slug)
        attrs['course'] = course
        return attrs

class CategoryListSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Category        
        fields = '__all__'


class CourseStudentSerialiser(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField(read_only=True)
    data_joined_course = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number', 'profile', 'data_joined_course']

    def get_profile(self, obj):
        profile = obj.student_profile
        return AdminProfileSerialiser(profile).data

    def get_data_joined_course(self, obj):
        course_slug = self.context.get('view').kwargs.get("course_slug")
        course = get_object_or_404(Course, slug=course_slug)
        date = obj.course_student.get(course=course)
        return str(date2jalali(date.join_date))
        


    
    