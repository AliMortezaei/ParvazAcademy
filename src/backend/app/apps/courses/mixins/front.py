
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404

from apps.courses.models import Course



class JoinStudentCourseMixin:

    @action(methods=['post'], detail=True, url_path='join')
    def join_student_in_course(self, request, course_slug, *args, **kwargs):
        course = get_object_or_404(Course, slug=course_slug)
        self.perform_join(course, request.user)
        return Response(data={"detail": "student joined course"}, status=status.HTTP_200_OK)

    def perform_join(self, course, user):
        if course.is_start:
            try:
                course.students.add(user)
                course.numbers += 1
                course.save()
                return True
            except Exception:
                return Response(data={"detail": "course not started"}, status=status.HTTP_400_BAD_REQUEST)

        
        