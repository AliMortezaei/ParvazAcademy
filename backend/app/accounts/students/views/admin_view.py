
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from accounts.students.models import StudentProfile
from accounts.students.serializers.admin_serializer import AdminProfileSerialiser
from apps.courses.models import Course


        

class AdminProfileApiView(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):

    queryset = StudentProfile.objects.all()
    serializer_class = AdminProfileSerialiser
    lookup_field = 'pk'
    lookup_url_kwarg = 'user_id'
