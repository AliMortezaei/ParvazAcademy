
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, extend_schema_serializer, extend_schema_field
from drf_spectacular.types import OpenApiTypes

from accounts.students.models import StudentProfile 


@extend_schema_field({
    'request':OpenApiTypes.BINARY,
})
class AdminProfileSerialiser(serializers.ModelSerializer):
    user = serializers.CharField(source='user.full_name', read_only=True)
    class Meta:
        model = StudentProfile
        fields = '__all__'
        