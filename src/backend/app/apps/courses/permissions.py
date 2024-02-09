

from rest_framework.permissions import BasePermission
from rest_framework.generics import get_object_or_404

from apps.courses.models import Course

class StudentCoursePermission(BasePermission):
    """
    StudentCoursePermission 
    
    This is for users who want to access any part of the course,
    they must be in the list of students of the course, IsAuthenticated
    """
    message = "شما نمیتوانید به این بخش دسترسی داشته باشید"
    
    def has_permission(self, request, view):
        course_slug = view.kwargs.get('course_slug')
        self.get_course_valied(course_slug)
        user_course = request.user.courses.filter(slug=course_slug).exists()
        if user_course:
            return True
        elif str(request.user.user_type) == "teacher":
            return True
        return False

    def get_course_valied(self, slug):
        return get_object_or_404(Course, slug=slug)