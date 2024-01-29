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


    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        match request.data['user_type']:
            case 'teacher':
                user_type = UserType.objects.get(user_type="teacher")
                request.data['user_type'] = user_type
            case 'student':
                user_type = UserType.objects.get(user_type="student")
                request.data['user_type'] = user_type
        return self.update(request, *args, **kwargs)
        
    
    def perform_create(self, serializer):
        self.get_queryset().model.objects.create_user(
                password=serializer.data['password'],
                email=serializer.data['email'],
                phone_number=serializer.data['phone_number'],
                full_name=serializer.data['full_name']
        )
        
