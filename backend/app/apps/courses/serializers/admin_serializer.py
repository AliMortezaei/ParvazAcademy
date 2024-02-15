

from urllib import request
from attr import field
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from accounts.users.serializers.admin_serializer import AdminUserSeialiser
from accounts.users.models import User
from accounts.students.serializers.admin_serializer import AdminProfileSerialiser
from apps.courses.models import Category, Course, Section
from accounts.users.serializers.front_serializer import validate_phone_number




class AdminCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AdminCourseSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.slug')
    teacher = serializers.CharField(source='teacher.full_name')
    class Meta:
        model = Course
        #fields = '__all__'
        exclude = ("students", 'numbers')

    
    def create(self, validated_data):
        category_slug = validated_data.get('category')['slug']
        teacher_full_name = validated_data.get('teacher')['full_name']
        validated_data['category'] = get_object_or_404(Category, slug=category_slug)
        validated_data['teacher'] = get_object_or_404(User, full_name=teacher_full_name)

        return super().create(validated_data)

class AdminCourseModificationSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=False)
    category = serializers.SerializerMethodField()
    teacher = serializers.CharField(required=False)
    class Meta:
        model = Course
        exclude = ("students",)
        
    def get_category(self, obj):
        return obj.category.title




class AdminCourseSectionListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Section
        fields = ['id', 'title', 'slug', 'date_start', 'is_passed']

class AdminSectionSeialiser(serializers.ModelSerializer):
    course = serializers.CharField(source='course.title', read_only=True)
    title = serializers.CharField(required=False)

    class Meta:
        model = Section
        fields = '__all__'

    def validate(self, attrs):
        course_slug = self.context.get('view').kwargs.get("course_slug")
        course = get_object_or_404(Course, slug=course_slug)
        attrs['course'] = course
        return attrs

