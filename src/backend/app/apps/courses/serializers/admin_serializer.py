

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from accounts.users.serializers.admin_serializer import AdminUserSeialiser
from accounts.users.models import User
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
        exclude = ("date_end", "students")

    def create(self, validated_data):
        category_slug = validated_data.get('category')['slug']
        validated_data['category'] = get_object_or_404(Category, slug=category_slug)
        return super().create(validated_data)



# student serializer

class AdminCourseStudentListSerialiser(serializers.ModelSerializer):
    students = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['title', 'students'] 

    # TODO: moust model serializer change for user students after user image set
    def get_students(self, obj):
        return [
            AdminUserSeialiser(student).data
            for student in obj.students.all()
        ]



class AdminCourseSectionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Section
        fields = ['id', 'title', 'slug', 'link', 'date_start', 'is_passed']
