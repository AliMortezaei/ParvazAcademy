
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import DestroyModelMixin

from apps.courses.models import Course



class JoinStudentCourseMixin:

    @action(methods=['post'], detail=True, url_path='join')
    def join_student_in_course(self, request, course_slug, *args, **kwargs):
        """
        this endpoint used for `join` to course and only con use `teacher` (user that user_type teacher) 
        yours send patch parameter course slug
        Note that the user type `student` ond must is `authenticated`
        Args:
            course_slug(str): example => `learn-django`
        """
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

        
class StudentDestroMixin(DestroyModelMixin):

    def perform_destroy(self, instance):
        student = get_object_or_404(instance.students, id=self.kwargs.get('student_id'))
        try:
            instance.students.remove(student)
            instance.numbers -= 1
            instance.save()
        except Exception:
                return Response(data={"error": "error"}, status=status.HTTP_400_BAD_REQUEST)
    