from requests import delete
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from accounts.users.models import User
from utils.exception import NotFoundException
from apps.courses.models import Course, Section

from drf_spectacular.utils import OpenApiParameter, extend_schema_view,extend_schema




 
class StudentsJoinMixin:
    
    def join_student(self, request, *args, **kwargs):
        course = self.get_object()
        student = get_object_or_404(User, id=kwargs.get('student_id'))
        self.perform_join_student(course, student)
        return Response(data={"detail":"accepted"}, status=status.HTTP_202_ACCEPTED)

    def perform_join_student(self, course, student):
        if course.is_start:
            try:
                course.students.add(student)
                course.numbers += 1
                course.save()
                return True
            except Exception:
                return Response(data={"error": "course not started"}, status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        student = get_object_or_404(instance.students, id=self.kwargs.get('student_id'))
        try:
            instance.students.remove(student)
            instance.numbers -= 1
            instance.save()
        except Exception:
                return Response(data={"error": "error"}, status=status.HTTP_400_BAD_REQUEST)




