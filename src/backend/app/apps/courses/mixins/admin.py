from requests import delete
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from accounts.users.models import User
from utils.exception import NotFoundException
from apps.courses.models import Course, Section


from drf_spectacular.utils import OpenApiParameter, extend_schema





class StudentMixin:

    @action(methods=['get'], detail=True, url_path='students')
    def student_list(self, request, slug: str = None):
        course = get_object_or_404(Course, slug__icontains=slug)
        serializer = self.get_serializer(course)
        return Response(serializer.data)


    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="student_id",
                description=(
                    "Added a student to the course"
                ),
                type=int,
                required=True,
                
            )
        ],
        request=None,
    )
    @student_list.mapping.post
    def add_student(self, request, slug: str = None, *args, **kwargs):
        user_id = request.query_params.get('student_id')
        student = get_object_or_404(User, id=user_id)
        course = get_object_or_404(Course, slug__icontains=slug)
        self.perform_save(course, student)
        return Response(data={"detail":"accepted"}, status=status.HTTP_202_ACCEPTED)


    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="student_id",
                description=(
                    "remove a student to the course"
                ),
                type=int,
                required=True,
                
            )
        ],
        request=None,
    )
    @student_list.mapping.delete
    def delete_student(self, request, slug: str = None, *args, **kwargs):
        user_id = request.query_params.get('student_id')
        student = get_object_or_404(User, id=user_id)
        course = get_object_or_404(Course, slug__icontains=slug)
        self.perform_delete(course, student)
        return Response(data={"detail":"accepted"}, status=status.HTTP_202_ACCEPTED)


    def perform_save(self, course, student):
        course.students.add(student)
    
    def perform_delete(self, course, student):
        course.students.remove(student)



class SectionMixin:
    
    @action(methods=['get'], detail=True, url_path='sections')
    def sections(self, request, slug: str = None):
        course = get_object_or_404(Course, slug__icontains=slug)
        sections = course.sections.all()
        serializer = self.get_serializer(sections, many=True)
        return Response(serializer.data)
    
    
    @sections.mapping.post
    def add_section(self, request, slug: str = None):
        course = get_object_or_404(Course, slug__icontains=slug)
        serializer = self.valiedate_serializer(request)
        self.perform_create(course, **serializer.data)
        return Response(data={"detail": "created section"}, status=status.HTTP_201_CREATED)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="section_id",
                description=(
                    "remove a section to the course"
                ),
                type=int,
                required=True,
                
            )
        ],
        request=None,
    )
    @sections.mapping.delete
    def delete_section(self, request, slug: str = None):
        section_id = request.query_params.get('section_id')
        section = get_object_or_404(Section, id=section_id)
        course = get_object_or_404(Course, slug__icontains=slug)
        self.perform_delete(course, section)
        return Response(data={"detail":"accepted"}, status=status.HTTP_202_ACCEPTED)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="section_id",
                description=(
                    "update a section to the course"
                ),
                type=int,
                required=True,
                
            )
        ],
    )
    @sections.mapping.patch
    def update_section(self, request, slug: str = None):
        section_id = request.query_params.get('section_id')
        instance = get_object_or_404(Section, id=section_id)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        return Response(data={"detail":"accepted"}, status=status.HTTP_202_ACCEPTED)

    def perform_update(self, serializer, instance):
        serializer.save()

    
    def perform_delete(self, course, section):
        if section.course == course:
            section.delete()
        else:
            raise NotFoundException()
    def perform_create(self, course, **data):
        section = Section(**data)
        section.course = course
        section.save()

    def valiedate_serializer(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return serializer