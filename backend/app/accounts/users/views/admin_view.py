from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters

from accounts.users.models import User, UserType
from accounts.users.serializers.admin_serializer import AdminUserSeialiser, AdminUserCreateSeialiser
from accounts.users.filters import AdminUserFilter


        
        
class AdminUserViewSet(ModelViewSet):
    
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AdminUserFilter

    lookup_field = 'pk'
    lookup_url_kwarg = 'user_id'


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
        
