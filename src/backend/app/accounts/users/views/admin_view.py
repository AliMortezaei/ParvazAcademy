from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from accounts.users.models import User
from accounts.users.serializers.admin_serializer import AdminUserSeialiser, AdminUserCreateSeialiser


class AdminUserViewSet(ModelViewSet):

    serializer_class = AdminUserSeialiser
    queryset = User.objects.all()
    
    permission_classes = [IsAdminUser]

    def  get_serializer_class(self):
        if self.action == 'create':
            return AdminUserCreateSeialiser
        else:
            return AdminUserSeialiser

    
    def perform_create(self, serializer):
        self.get_queryset().model.objects.create_user(
                password=serializer.data['password'],
                email=serializer.data['email'],
                phone_number=serializer.data['phone_number'],
                full_name=serializer.data['full_name']
        )
        
