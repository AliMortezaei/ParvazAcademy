from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from accounts.users.models import User, UserType
from accounts.users.serializers.admin_serializer import AdminUserSeialiser, AdminUserCreateSeialiser


class AdminUserViewSet(ModelViewSet):

    queryset = User.objects.all()
    
    permission_classes = [IsAdminUser]


    def  get_serializer_class(self):
        if self.action == 'create':
            return AdminUserCreateSeialiser
        else:
            return AdminUserSeialiser
    
    def perform_create(self, serializer):
        data = serializer.create_validate(serializer.data)
        self.get_queryset().model.objects.create_user(
                password=data['password'],
                email=data['email'],
                phone_number=data['phone_number'],
                full_name=data['full_name'],
                user_type=data['user_type']
        )
        
