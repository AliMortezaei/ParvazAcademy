
from rest_framework.permissions import BasePermission
from rest_framework.generics import get_object_or_404

from apps.courses.models import Course


class IsTeacher(BasePermission):
    """
    TeacherPermission
    request in user to teacher type 
    """
    message = "شما نمیتوانید به این بخش دسترسی داشته باشید"
    def has_permission(self, request, view):
        is_authenticated = bool(request.user and request.user.is_authenticated)
        if is_authenticated and str(request.user.user_type) == "teacher":
            return True
        return False

class IsTeacherCourse(BasePermission):
    """
    TeacherCoursePermission 
    request in user to check user type teacher and 
    request course slug for self teacher 

    """
    message = "شما نمیتوانید به این بخش دسترسی داشته باشید"

    def has_permission(self, request, view):
        course_slig = view.kwargs.get('course_slug')
        course = get_object_or_404(Course, slug=course_slig)
        if request.user == course.teacher:
            return True
        return False
